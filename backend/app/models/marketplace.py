"""
Marketplace Models for Pi Network Integration

A robust, efficient, and extensible marketplace engine for digital and physical assets,
with auction, ratings, categories, and transaction tracking, tailored for the Pi Network metaverse.
"""

import uuid
import enum
import json
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, Any, List, Optional, Tuple

from sqlalchemy import event, func, Index, CheckConstraint, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref

from app.extensions import db
from app.core.exceptions import ValidationError

# --- Enums ---

class ItemCondition(enum.Enum):
    NEW = "new"
    LIKE_NEW = "like_new"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"

class ItemRarity(enum.Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    MYTHIC = "mythic"

class ItemType(enum.Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    ACCESSORY = "accessory"
    CONSUMABLE = "consumable"
    QUEST_ITEM = "quest_item"
    COSMETIC = "cosmetic"
    BLUEPRINT = "blueprint"
    RESOURCE = "resource"
    COLLECTIBLE = "collectible"
    PREMIUM = "premium"

class ListingStatus(enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    SOLD = "sold"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    RESERVED = "reserved"
    UNDER_REVIEW = "under_review"
    FLAGGED = "flagged"

# --- Marketplace Category ---

class ItemCategory(db.Model):
    """
    Marketplace item categories, supporting sub-categories and commission rates.
    """
    __tablename__ = 'item_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('item_categories.id'), nullable=True)
    icon = db.Column(db.String(100), nullable=True)
    commission_rate = db.Column(db.Float, default=0.05, nullable=False)  # 5% default
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    subcategories = relationship(
        'ItemCategory',
        backref=backref('parent', remote_side=[id]),
        lazy='joined'
    )
    items = relationship('MarketplaceItem', backref='category', lazy='dynamic')

    def to_dict(self, include_subcategories: bool = False) -> Dict[str, Any]:
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'commission_rate': self.commission_rate,
            'item_count': self.items.filter_by(status=ListingStatus.ACTIVE).count()
        }
        if include_subcategories:
            data['subcategories'] = [sub.to_dict() for sub in self.subcategories if sub.is_active]
        return data

    def __repr__(self) -> str:
        return f"<ItemCategory {self.name}>"

# --- Marketplace Item ---

class MarketplaceItem(db.Model):
    """
    Marketplace Item model, supporting auction, direct sale, ratings, analytics, and ownership transfer.
    """

    __tablename__ = 'marketplace_items'
    __table_args__ = (
        CheckConstraint('current_price > 0', name='valid_price'),
        CheckConstraint('view_count >= 0', name='valid_view_count'),
        Index('idx_item_status_category', 'status', 'category_id'),
        Index('idx_item_price_condition', 'current_price', 'condition'),
        Index('idx_item_seller_status', 'seller_id', 'status'),
        Index('idx_item_featured_listed', 'featured', 'listed_at'),
    )

    # IDs and Classification
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    item_key = db.Column(db.String(100), nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    short_description = db.Column(db.String(500), nullable=True)
    item_type = db.Column(db.Enum(ItemType), nullable=True, index=True)
    rarity = db.Column(db.Enum(ItemRarity), default=ItemRarity.COMMON, index=True)
    condition = db.Column(db.Enum(ItemCondition), default=ItemCondition.NEW, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('item_categories.id'), nullable=False)
    tags = db.Column(db.Text)  # JSON list

    # Media
    image_url = db.Column(db.String(500))
    thumbnail_url = db.Column(db.String(500))
    images = db.Column(db.JSON, nullable=True)
    primary_image = db.Column(db.String(500), nullable=True)
    video_url = db.Column(db.String(500), nullable=True)
    attributes = db.Column(db.Text)  # JSON attributes

    # Pricing & Auction
    original_price = db.Column(db.Numeric(precision=20, scale=8), nullable=False)
    current_price = db.Column(db.Numeric(precision=20, scale=8), nullable=False)
    reserve_price = db.Column(db.Numeric(precision=20, scale=8))
    is_auction = db.Column(db.Boolean, default=False)
    auction_end_time = db.Column(db.DateTime)
    highest_bid = db.Column(db.Numeric(precision=20, scale=8))
    highest_bidder_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    bid_count = db.Column(db.Integer, default=0)

    # Seller & Buyer
    seller_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    buyer_id = db.Column(db.String(36), db.ForeignKey('users.id'), index=True)
    seller_notes = db.Column(db.Text, nullable=True)

    # Status & Analytics
    status = db.Column(db.Enum(ListingStatus), default=ListingStatus.DRAFT, index=True)
    featured = db.Column(db.Boolean, default=False, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    is_digital = db.Column(db.Boolean, default=False, nullable=False)
    quantity_available = db.Column(db.Integer, default=1, nullable=False)
    listed_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    expires_at = db.Column(db.DateTime, index=True)
    sold_at = db.Column(db.DateTime)
    view_count = db.Column(db.Integer, default=0, nullable=False)
    favorite_count = db.Column(db.Integer, default=0, nullable=False)
    inquiry_count = db.Column(db.Integer, default=0, nullable=False)
    shipping_included = db.Column(db.Boolean, default=False, nullable=False)
    shipping_cost = db.Column(db.Numeric(precision=10, scale=2), default=0, nullable=False)
    ships_from = db.Column(db.String(100), nullable=True)
    ships_to = db.Column(db.JSON, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    dimensions = db.Column(db.JSON, nullable=True)

    # Quality and authenticity
    condition_rating = db.Column(db.Float)
    authenticity_verified = db.Column(db.Boolean, default=False)
    verification_notes = db.Column(db.Text)

    # Seller reputation impact
    seller_rating_at_listing = db.Column(db.Float)

    # Transaction details
    sale_price = db.Column(db.Numeric(precision=20, scale=8))
    transaction_id = db.Column(db.String(36), db.ForeignKey('transactions.id'))
    platform_fee = db.Column(db.Numeric(precision=20, scale=8))

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    category_path = db.Column(db.String(255), index=True)

    # Relationships
    seller = relationship('User', foreign_keys=[seller_id], backref='marketplace_listings')
    buyer = relationship('User', foreign_keys=[buyer_id])
    highest_bidder = relationship('User', foreign_keys=[highest_bidder_id])
    transaction = relationship('Transaction', backref='marketplace_item')
    bids = relationship('MarketplaceBid', backref='item', cascade='all, delete-orphan')
    reviews = relationship('ItemReview', backref='item', lazy='dynamic', cascade='all, delete-orphan')
    favorites = relationship('ItemFavorite', backref='item', lazy='dynamic', cascade='all, delete-orphan')

    # --- Properties and Methods ---

    @hybrid_property
    def time_remaining(self) -> timedelta:
        now = datetime.utcnow()
        if self.is_auction and self.auction_end_time:
            return max(timedelta(0), self.auction_end_time - now)
        elif self.expires_at:
            return max(timedelta(0), self.expires_at - now)
        return timedelta(0)

    @hybrid_property
    def is_expired(self) -> bool:
        now = datetime.utcnow()
        if self.is_auction:
            return now > self.auction_end_time if self.auction_end_time else False
        return now > self.expires_at if self.expires_at else False

    @hybrid_property
    def is_available(self) -> bool:
        return (
            self.status == ListingStatus.ACTIVE
            and self.quantity_available > 0
            and not self.is_expired
        )

    @hybrid_property
    def discount_percentage(self) -> float:
        if not self.original_price or self.original_price <= self.current_price:
            return 0.0
        return float(((self.original_price - self.current_price) / self.original_price) * 100)

    @hybrid_property
    def commission_amount(self) -> Decimal:
        rate = self.category.commission_rate if self.category and self.category.commission_rate else 0.05
        return self.current_price * Decimal(str(rate))

    def can_purchase(self, user, quantity: int = 1) -> Tuple[bool, str]:
        if not self.is_available:
            return False, "Item is not available"
        if user.id == self.seller_id:
            return False, "Cannot purchase your own item"
        if quantity > self.quantity_available:
            return False, f"Only {self.quantity_available} available"
        if getattr(user, 'total_rewards', 0) < self.current_price * quantity:
            return False, "Insufficient balance"
        return True, "Eligible"

    def purchase(self, buyer, quantity: int = 1) -> 'Purchase':
        from app.models.user import User  # Avoid circular import
        from app.models.transaction import Transaction, TransactionType

        can_purchase, reason = self.can_purchase(buyer, quantity)
        if not can_purchase:
            raise ValidationError(f"Cannot purchase item: {reason}")

        # Calculate cost
        item_cost = self.current_price * quantity
        commission = self.commission_amount * quantity
        shipping_cost = self.shipping_cost if not self.shipping_included else 0
        total_cost = item_cost + shipping_cost
        seller_receives = item_cost - commission

        # Create transaction
        transaction = Transaction(
            sender_id=buyer.id,
            recipient_id=self.seller_id,
            amount=item_cost,
            net_amount=seller_receives,
            fee=commission,
            transaction_type=TransactionType.MARKETPLACE_PURCHASE,
            description=f"Purchase of {self.name}",
            reference_id=self.id,
            reference_type='marketplace_item'
        )
        success, error = transaction.process_transaction()
        if not success:
            raise ValidationError(f"Transaction failed: {error}")

        # Update item state
        self.quantity_available -= quantity
        if self.quantity_available == 0:
            self.status = ListingStatus.SOLD
            self.sold_at = datetime.utcnow()
        self.buyer_id = buyer.id
        self.sale_price = self.current_price
        self.transaction_id = transaction.id
        self.platform_fee = commission
        db.session.add(transaction)
        db.session.flush()  # Ensure transaction ID is set

        # Create purchase record
        purchase = Purchase(
            item_id=self.id,
            buyer_id=buyer.id,
            seller_id=self.seller_id,
            quantity=quantity,
            unit_price=self.current_price,
            shipping_cost=shipping_cost,
            commission_amount=commission,
            total_amount=total_cost,
            transaction_id=transaction.id
        )
        db.session.add(purchase)
        return purchase

    def add_view(self) -> None:
        self.view_count += 1

    def add_to_favorites(self, user) -> bool:
        if self.favorites.filter_by(user_id=user.id).first():
            return False
        favorite = ItemFavorite(item_id=self.id, user_id=user.id)
        db.session.add(favorite)
        self.favorite_count += 1
        return True

    def remove_from_favorites(self, user) -> bool:
        favorite = self.favorites.filter_by(user_id=user.id).first()
        if not favorite:
            return False
        db.session.delete(favorite)
        self.favorite_count = max(0, self.favorite_count - 1)
        return True

    def publish(self) -> None:
        if self.status == ListingStatus.DRAFT:
            self.status = ListingStatus.ACTIVE
            self.listed_at = datetime.utcnow()
            if not self.expires_at:
                self.expires_at = datetime.utcnow() + timedelta(days=30)

    @hybrid_property
    def average_rating(self) -> float:
        result = db.session.query(func.avg(ItemReview.rating)).filter(
            ItemReview.item_id == self.id,
            ItemReview.is_approved == True
        ).scalar()
        return round(result or 0.0, 2)

    def get_attributes(self) -> Dict[str, Any]:
        if not self.attributes:
            return {}
        try:
            return json.loads(self.attributes)
        except (json.JSONDecodeError, TypeError):
            return {}

    def get_tags(self) -> List[str]:
        if not self.tags:
            return []
        try:
            return json.loads(self.tags)
        except (json.JSONDecodeError, TypeError):
            return []

    def to_dict(self, user=None, include_analytics: bool = False) -> Dict[str, Any]:
        data = {
            'id': self.id,
            'item_key': self.item_key,
            'name': self.name,
            'description': self.description,
            'short_description': self.short_description,
            'item_type': self.item_type.value if self.item_type else None,
            'rarity': self.rarity.value if self.rarity else None,
            'condition': self.condition.value if self.condition else None,
            'current_price': float(self.current_price),
            'original_price': float(self.original_price),
            'is_auction': self.is_auction,
            'status': self.status.value,
            'featured': self.featured,
            'is_verified': self.is_verified,
            'is_digital': self.is_digital,
            'quantity_available': self.quantity_available,
            'primary_image': self.primary_image,
            'images': self.images or [],
            'video_url': self.video_url,
            'discount_percentage': round(self.discount_percentage, 2),
            'average_rating': self.average_rating,
            'review_count': self.reviews.filter_by(is_approved=True).count(),
            'shipping_included': self.shipping_included,
            'shipping_cost': float(self.shipping_cost),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'category': self.category.to_dict() if self.category else None,
            'tags': self.get_tags(),
            'attributes': self.get_attributes(),
            'seller': {
                'id': self.seller.id,
                'username': self.seller.username,
                'display_name': getattr(self.seller, 'display_name', None) or self.seller.username,
                'level': getattr(self.seller, 'level', None),
                'reputation': self.seller_rating_at_listing or 0.0
            } if self.seller else None
        }
        if self.is_auction:
            data.update({
                'auction_end_time': self.auction_end_time.isoformat() if self.auction_end_time else None,
                'highest_bid': float(self.highest_bid) if self.highest_bid else None,
                'bid_count': self.bid_count,
                'reserve_price': float(self.reserve_price) if self.reserve_price else None,
                'time_remaining_seconds': int(self.time_remaining.total_seconds())
            })
        if user:
            is_favorited = self.favorites.filter_by(user_id=user.id).first() is not None
            can_purchase, reason = self.can_purchase(user)
            data.update({
                'is_favorited': is_favorited,
                'can_purchase': can_purchase,
                'purchase_reason': reason
            })
        if include_analytics:
            data.update({
                'view_count': self.view_count,
                'favorite_count': self.favorite_count,
                'inquiry_count': self.inquiry_count
            })
        return data

    def __repr__(self) -> str:
        return f'<MarketplaceItem {self.name} ({self.status.value})>'

# --- Purchase ---

class Purchase(db.Model):
    """
    Purchase transaction record with full audit trail.
    """
    __tablename__ = 'marketplace_purchases'
    __table_args__ = (
        CheckConstraint('quantity > 0', name='valid_purchase_quantity'),
        CheckConstraint('unit_price > 0', name='valid_unit_price'),
        CheckConstraint('total_amount > 0', name='valid_total_amount'),
        Index('idx_purchase_status_date', 'status', 'purchased_at'),
        Index('idx_purchase_buyer_date', 'buyer_id', 'purchased_at'),
        Index('idx_purchase_seller_date', 'seller_id', 'purchased_at'),
    )

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    item_id = db.Column(db.String(36), db.ForeignKey('marketplace_items.id'), nullable=False)
    buyer_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    seller_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    transaction_id = db.Column(db.String(36), db.ForeignKey('transactions.id'))

    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(precision=20, scale=8), nullable=False)
    shipping_cost = db.Column(db.Numeric(precision=10, scale=2), default=0, nullable=False)
    commission_amount = db.Column(db.Numeric(precision=20, scale=8), default=0, nullable=False)
    total_amount = db.Column(db.Numeric(precision=20, scale=8), nullable=False)

    status = db.Column(db.String(20), default='pending', nullable=False)
    payment_status = db.Column(db.String(20), default='pending', nullable=False)
    fulfillment_status = db.Column(db.String(20), default='pending', nullable=False)

    tracking_number = db.Column(db.String(100), nullable=True)
    shipping_provider = db.Column(db.String(50), nullable=True)
    estimated_delivery = db.Column(db.DateTime, nullable=True)

    buyer_notes = db.Column(db.Text, nullable=True)
    seller_notes = db.Column(db.Text, nullable=True)
    admin_notes = db.Column(db.Text, nullable=True)

    purchased_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    paid_at = db.Column(db.DateTime, nullable=True)
    shipped_at = db.Column(db.DateTime, nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)

    buyer = relationship('User', foreign_keys=[buyer_id], backref='purchases')
    seller = relationship('User', foreign_keys=[seller_id], backref='sales')

    def mark_paid(self) -> None:
        self.payment_status = 'completed'
        self.paid_at = datetime.utcnow()
        if self.status == 'pending':
            self.status = 'confirmed'

    def mark_shipped(self, tracking_number: Optional[str] = None, provider: Optional[str] = None) -> None:
        self.fulfillment_status = 'shipped'
        self.shipped_at = datetime.utcnow()
        if tracking_number:
            self.tracking_number = tracking_number
        if provider:
            self.shipping_provider = provider
