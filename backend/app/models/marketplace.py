"""
Marketplace Models for Pi Network Integration
Professional marketplace with categories, ratings, and transaction management.
"""

import uuid
import enum
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from decimal import Decimal
from sqlalchemy import event
from sqlalchemy.ext.hybrid import hybrid_property

from app.extensions import db
from app.core.exceptions import ValidationError


class ItemCondition(enum.Enum):
    """Item condition enumeration."""
    NEW = "new"
    LIKE_NEW = "like_new"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


class ItemStatus(enum.Enum):
    """Item listing status."""
    DRAFT = "draft"
    ACTIVE = "active"
    SOLD = "sold"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    FLAGGED = "flagged"


class ItemCategory(db.Model):
    """Marketplace item categories."""
    
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
    
    # Self-referential relationship for subcategories
    subcategories = db.relationship('ItemCategory', backref=db.backref('parent', remote_side=[id]))
    items = db.relationship('Item', backref='category', lazy='dynamic')
    
    def to_dict(self, include_subcategories: bool = False) -> Dict[str, Any]:
        """Convert category to dictionary."""
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'commission_rate': self.commission_rate,
            'item_count': self.items.filter_by(status=ItemStatus.ACTIVE).count()
        }
        
        if include_subcategories:
            data['subcategories'] = [sub.to_dict() for sub in self.subcategories if sub.is_active]
        
        return data


class Item(db.Model):
    """
    Marketplace item model with comprehensive features.
    Supports digital and physical items with detailed tracking.
    """
    
    __tablename__ = 'marketplace_items'
    
    # Primary identification
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(500), nullable=True)
    
    # Categorization
    category_id = db.Column(db.Integer, db.ForeignKey('item_categories.id'), nullable=False)
    tags = db.Column(db.JSON, nullable=True)  # List of tags
    
    # Pricing and commerce
    price = db.Column(db.Numeric(precision=20, scale=8), nullable=False)
    original_price = db.Column(db.Numeric(precision=20, scale=8), nullable=True)
    currency = db.Column(db.String(10), default='PI', nullable=False)
    is_negotiable = db.Column(db.Boolean, default=False, nullable=False)
    
    # Item details
    condition = db.Column(db.Enum(ItemCondition), default=ItemCondition.NEW, nullable=False)
    quantity_available = db.Column(db.Integer, default=1, nullable=False)
    is_digital = db.Column(db.Boolean, default=False, nullable=False)
    weight = db.Column(db.Float, nullable=True)  # For shipping calculations
    dimensions = db.Column(db.JSON, nullable=True)  # {length, width, height}
    
    # Media and presentation
    images = db.Column(db.JSON, nullable=True)  # List of image URLs
    primary_image = db.Column(db.String(500), nullable=True)
    video_url = db.Column(db.String(500), nullable=True)
    
    # Seller information
    seller_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    seller_notes = db.Column(db.Text, nullable=True)
    
    # Status and availability
    status = db.Column(db.Enum(ItemStatus), default=ItemStatus.DRAFT, nullable=False)
    featured = db.Column(db.Boolean, default=False, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    
    # Timing
    listed_at = db.Column(db.DateTime, nullable=True)
    expires_at = db.Column(db.DateTime, nullable=True)
    
    # Analytics and engagement
    view_count = db.Column(db.Integer, default=0, nullable=False)
    favorite_count = db.Column(db.Integer, default=0, nullable=False)
    inquiry_count = db.Column(db.Integer, default=0, nullable=False)
    
    # Shipping and logistics
    shipping_included = db.Column(db.Boolean, default=False, nullable=False)
    shipping_cost = db.Column(db.Numeric(precision=10, scale=2), default=0, nullable=False)
    ships_from = db.Column(db.String(100), nullable=True)  # Location
    ships_to = db.Column(db.JSON, nullable=True)  # List of regions/countries
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    seller = db.relationship('User', backref='marketplace_listings', foreign_keys=[seller_id])
    purchases = db.relationship('Purchase', backref='item', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('ItemReview', backref='item', lazy='dynamic', cascade='all, delete-orphan')
    favorites = db.relationship('ItemFavorite', backref='item', lazy='dynamic', cascade='all, delete-orphan')
    
    # Constraints
    __table_args__ = (
        db.CheckConstraint('price > 0', name='valid_price'),
        db.CheckConstraint('quantity_available >= 0', name='valid_quantity'),
        db.CheckConstraint('view_count >= 0', name='valid_view_count'),
        db.CheckConstraint('shipping_cost >= 0', name='valid_shipping_cost'),
        db.Index('idx_item_status_category', 'status', 'category_id'),
        db.Index('idx_item_price_condition', 'price', 'condition'),
        db.Index('idx_item_seller_status', 'seller_id', 'status'),
        db.Index('idx_item_featured_listed', 'featured', 'listed_at'),
    )
    
    @hybrid_property
    def is_available(self) -> bool:
        """Check if item is available for purchase."""
        return (self.status == ItemStatus.ACTIVE and
                self.quantity_available > 0 and
                (self.expires_at is None or self.expires_at > datetime.utcnow()))
    
    @hybrid_property
    def total_price(self) -> Decimal:
        """Calculate total price including shipping."""
        return self.price + (self.shipping_cost if not self.shipping_included else 0)
    
    @hybrid_property
    def discount_percentage(self) -> float:
        """Calculate discount percentage if original price exists."""
        if not self.original_price or self.original_price <= self.price:
            return 0.0
        return float(((self.original_price - self.price) / self.original_price) * 100)
    
    @hybrid_property
    def average_rating(self) -> float:
        """Calculate average rating from reviews."""
        reviews = self.reviews.filter_by(is_approved=True).all()
        if not reviews:
            return 0.0
        return sum(review.rating for review in reviews) / len(reviews)
    
    @hybrid_property
    def commission_amount(self) -> Decimal:
        """Calculate marketplace commission."""
        return self.price * Decimal(str(self.category.commission_rate))
    
    def can_purchase(self, user, quantity: int = 1) -> tuple[bool, str]:
        """
        Check if user can purchase this item.
        
        Args:
            user: User attempting to purchase
            quantity: Quantity to purchase
            
        Returns:
            Tuple of (can_purchase, reason)
        """
        if not self.is_available:
            return False, "Item is not available"
        
        if user.id == self.seller_id:
            return False, "Cannot purchase your own item"
        
        if quantity > self.quantity_available:
            return False, f"Only {self.quantity_available} available"
        
        total_cost = self.total_price * quantity
        if user.total_rewards < total_cost:
            return False, "Insufficient balance"
        
        return True, "Eligible"
    
    def purchase(self, buyer, quantity: int = 1) -> 'Purchase':
        """
        Process item purchase.
        
        Args:
            buyer: User making the purchase
            quantity: Quantity to purchase
            
        Returns:
            Purchase record
        """
        can_purchase, reason = self.can_purchase(buyer, quantity)
        if not can_purchase:
            raise ValidationError(f"Cannot purchase item: {reason}")
        
        # Calculate costs
        item_cost = self.price * quantity
        shipping_cost = self.shipping_cost if not self.shipping_included else 0
        commission = self.commission_amount * quantity
        total_cost = item_cost + shipping_cost
        seller_receives = item_cost - commission
        
        # Create purchase record
        purchase = Purchase(
            item_id=self.id,
            buyer_id=buyer.id,
            seller_id=self.seller_id,
            quantity=quantity,
            unit_price=self.price,
            shipping_cost=shipping_cost,
            commission_amount=commission,
            total_amount=total_cost
        )
        
        # Update quantities
        self.quantity_available -= quantity
        if self.quantity_available == 0:
            self.status = ItemStatus.SOLD
        
        # Process payments (simplified - would integrate with Pi Network)
        buyer.total_rewards -= total_cost
        self.seller.total_rewards += seller_receives
        
        db.session.add(purchase)
        return purchase
    
    def add_view(self) -> None:
        """Increment view count."""
        self.view_count += 1
    
    def add_to_favorites(self, user) -> bool:
        """Add item to user's favorites."""
        existing = self.favorites.filter_by(user_id=user.id).first()
        if existing:
            return False
        
        favorite = ItemFavorite(item_id=self.id, user_id=user.id)
        db.session.add(favorite)
        self.favorite_count += 1
        return True
    
    def remove_from_favorites(self, user) -> bool:
        """Remove item from user's favorites."""
        favorite = self.favorites.filter_by(user_id=user.id).first()
        if not favorite:
            return False
        
        db.session.delete(favorite)
        self.favorite_count = max(0, self.favorite_count - 1)
        return True
    
    def publish(self) -> None:
        """Publish item to marketplace."""
        if self.status == ItemStatus.DRAFT:
            self.status = ItemStatus.ACTIVE
            self.listed_at = datetime.utcnow()
            
            # Set expiration if not set (default 30 days)
            if not self.expires_at:
                self.expires_at = datetime.utcnow() + timedelta(days=30)
    
    def to_dict(self, user=None, include_analytics: bool = False) -> Dict[str, Any]:
        """Convert item to dictionary representation."""
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'short_description': self.short_description,
            'price': float(self.price),
            'currency': self.currency,
            'condition': self.condition.value,
            'quantity_available': self.quantity_available,
            'is_digital': self.is_digital,
            'status': self.status.value,
            'featured': self.featured,
            'is_verified': self.is_verified,
            'primary_image': self.primary_image,
            'images': self.images or [],
            'total_price': float(self.total_price),
            'discount_percentage': round(self.discount_percentage, 2),
            'average_rating': round(self.average_rating, 2),
            'review_count': self.reviews.filter_by(is_approved=True).count(),
            'shipping_included': self.shipping_included,
            'shipping_cost': float(self.shipping_cost),
            'created_at': self.created_at.isoformat(),
            'category': self.category.to_dict(),
            'tags': self.tags or [],
            'seller': {
                'id': self.seller.id,
                'username': self.seller.username,
                'display_name': self.seller.display_name or self.seller.username,
                'level': self.seller.level
            }
        }
        
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
        return f"<Item {self.title} ({self.status.value})>"


class Purchase(db.Model):
    """
    Purchase transaction record with comprehensive tracking.
    Maintains full audit trail for marketplace transactions.
    """
    
    __tablename__ = 'marketplace_purchases'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    item_id = db.Column(db.String(36), db.ForeignKey('marketplace_items.id'), nullable=False)
    buyer_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    seller_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Purchase details
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(precision=20, scale=8), nullable=False)
    shipping_cost = db.Column(db.Numeric(precision=10, scale=2), default=0, nullable=False)
    commission_amount = db.Column(db.Numeric(precision=20, scale=8), default=0, nullable=False)
    total_amount = db.Column(db.Numeric(precision=20, scale=8), nullable=False)
    
    # Transaction status
    status = db.Column(db.String(20), default='pending', nullable=False)
    payment_status = db.Column(db.String(20), default='pending', nullable=False)
    fulfillment_status = db.Column(db.String(20), default='pending', nullable=False)
    
    # Tracking information
    tracking_number = db.Column(db.String(100), nullable=True)
    shipping_provider = db.Column(db.String(50), nullable=True)
    estimated_delivery = db.Column(db.DateTime, nullable=True)
    
    # Notes and communication
    buyer_notes = db.Column(db.Text, nullable=True)
    seller_notes = db.Column(db.Text, nullable=True)
    admin_notes = db.Column(db.Text, nullable=True)
    
    # Timestamps
    purchased_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    paid_at = db.Column(db.DateTime, nullable=True)
    shipped_at = db.Column(db.DateTime, nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    buyer = db.relationship('User', backref='purchases', foreign_keys=[buyer_id])
    seller = db.relationship('User', backref='sales', foreign_keys=[seller_id])
    
    # Constraints
    __table_args__ = (
        db.CheckConstraint('quantity > 0', name='valid_purchase_quantity'),
        db.CheckConstraint('unit_price > 0', name='valid_unit_price'),
        db.CheckConstraint('total_amount > 0', name='valid_total_amount'),
        db.Index('idx_purchase_status_date', 'status', 'purchased_at'),
        db.Index('idx_purchase_buyer_date', 'buyer_id', 'purchased_at'),
        db.Index('idx_purchase_seller_date', 'seller_id', 'purchased_at'),
    )
    
    def mark_paid(self) -> None:
        """Mark purchase as paid."""
        self.payment_status = 'completed'
        self.paid_at = datetime.utcnow()
        if self.status == 'pending':
            self.status = 'confirmed'
    
    def mark_shipped(self, tracking_number: str = None, provider: str = None) -> None:
        """Mark purchase as shipped."""
        self.fulfillment_status = 'shipped'
        self.shipped_at = datetime.utcnow()
        if tracking_number:
            self.tracking_number = tracking_number
        if provider:
            self.shipping_provider = provider
    
    def mark_delivered(self) -> None:
        """Mark purchase as delivered."""
        self.fulfillment_status = 'delivered'
        self.delivered_at = datetime.utcnow()
        self.status = 'completed'
        self.completed_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert purchase to dictionary representation."""
        return {
            'id': self.id,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price),
            'shipping_cost': float(self.shipping_cost),
            'total_amount': float(self.total_amount),
            'status': self.status,
            'payment_status': self.payment_status,
            'fulfillment_status': self.fulfillment_status,
            'tracking_number': self.tracking_number,
            'shipping_provider': self.shipping_provider,
            'purchased_at': self.purchased_at.isoformat(),
            'estimated_delivery': self.estimated_delivery.isoformat() if self.estimated_delivery else None,
            'item': {
                'id': self.item.id,
                'title': self.item.title,
                'primary_image': self.item.primary_image
            },
            'seller': {
                'id': self.seller.id,
                'username': self.seller.username,
                'display_name': self.seller.display_name or self.seller.username
            }
        }


class ItemReview(db.Model):
    """Item reviews and ratings system."""
    
    __tablename__ = 'item_reviews'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    item_id = db.Column(db.String(36), db.ForeignKey('marketplace_items.id'), nullable=False)
    reviewer_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    purchase_id = db.Column(db.String(36), db.ForeignKey('marketplace_purchases.id'), nullable=True)
    
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    title = db.Column(db.String(200), nullable=True)
    review_text = db.Column(db.Text, nullable=True)
    
    is_approved = db.Column(db.Boolean, default=True, nullable=False)
    is_verified_purchase = db.Column(db.Boolean, default=False, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    reviewer = db.relationship('User', backref='item_reviews')
    purchase = db.relationship('Purchase', backref='review')
    
    # Constraints
    __table_args__ = (
        db.CheckConstraint('rating >= 1 AND rating <= 5', name='valid_rating'),
        db.UniqueConstraint('item_id', 'reviewer_id', name='unique_item_review'),
    )


class ItemFavorite(db.Model):
    """User favorites/wishlist for marketplace items."""
    
    __tablename__ = 'item_favorites'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    item_id = db.Column(db.String(36), db.ForeignKey('marketplace_items.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    

from datetime import datetime, timedelta
from enum import Enum
from decimal import Decimal
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import event, func
from app import db
import json
import uuid

class ItemType(Enum):
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

class ItemRarity(Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    MYTHIC = "mythic"

class ListingStatus(Enum):
    ACTIVE = "active"
    SOLD = "sold"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    RESERVED = "reserved"
    UNDER_REVIEW = "under_review"

class MarketplaceItem(db.Model):
    """
    Sophisticated marketplace system for in-game items with dynamic pricing.
    """
    __tablename__ = 'marketplace_items'
    
    # Core identification
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    item_key = db.Column(db.String(100), nullable=False, index=True)
    
    # Item details
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    item_type = db.Column(db.Enum(ItemType), nullable=False, index=True)
    rarity = db.Column(db.Enum(ItemRarity), default=ItemRarity.COMMON, index=True)
    
    # Visual and metadata
    image_url = db.Column(db.String(500))
    thumbnail_url = db.Column(db.String(500))
    attributes = db.Column(db.Text)  # JSON of item attributes/stats
    
    # Listing information
    seller_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    buyer_id = db.Column(db.String(36), db.ForeignKey('users.id'), index=True)
    
    # Pricing
    original_price = db.Column(db.Numeric(precision=18, scale=8), nullable=False)
    current_price = db.Column(db.Numeric(precision=18, scale=8), nullable=False)
    reserve_price = db.Column(db.Numeric(precision=18, scale=8))  # Minimum acceptable price
    
    # Auction features
    is_auction = db.Column(db.Boolean, default=False)
    auction_end_time = db.Column(db.DateTime)
    highest_bid = db.Column(db.Numeric(precision=18, scale=8))
    highest_bidder_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    bid_count = db.Column(db.Integer, default=0)
    
    # Status and timing
    status = db.Column(db.Enum(ListingStatus), default=ListingStatus.ACTIVE, index=True)
    listed_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    expires_at = db.Column(db.DateTime, index=True)
    sold_at = db.Column(db.DateTime)
    
    # Market analytics
    view_count = db.Column(db.Integer, default=0)
    favorite_count = db.Column(db.Integer, default=0)
    inquiry_count = db.Column(db.Integer, default=0)
    
    # Quality and authenticity
    condition_rating = db.Column(db.Float)  # 1-10 scale
    authenticity_verified = db.Column(db.Boolean, default=False)
    verification_notes = db.Column(db.Text)
    
    # Seller reputation impact
    seller_rating_at_listing = db.Column(db.Float)
    
    # Transaction details
    sale_price = db.Column(db.Numeric(precision=18, scale=8))
    transaction_id = db.Column(db.String(36), db.ForeignKey('transactions.id'))
    platform_fee = db.Column(db.Numeric(precision=18, scale=8))
    
    # Search and categorization
    tags = db.Column(db.Text)  # JSON array of searchable tags
    category_path = db.Column(db.String(255), index=True)  # hierarchical category
    
    # Relationships
    seller = db.relationship('User', foreign_keys=[seller_id], backref='marketplace_listings')
    buyer = db.relationship('User', foreign_keys=[buyer_id])
    highest_bidder = db.relationship('User', foreign_keys=[highest_bidder_id])
    transaction = db.relationship('Transaction', backref='marketplace_item')
    bids = db.relationship('MarketplaceBid', backref='item', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<MarketplaceItem {self.name} - {self.current_price} Pi>'
    
    @classmethod
    def create_listing(cls, seller_id: str, item_data: dict) -> 'MarketplaceItem':
        """Create a new marketplace listing with validation."""
        # Set expiration based on item type and price
        days_to_expire = cls._calculate_listing_duration(
            item_data.get('item_type'), 
            item_data.get('price')
        )
        
        expires_at = datetime.utcnow() + timedelta(days=days_to_expire)
        
        listing = cls(
            seller_id=seller_id,
            item_key=item_data['item_key'],
            name=item_data['name'],
            description=item_data.get('description'),
            item_type=ItemType(item_data['item_type']),
            rarity=ItemRarity(item_data.get('rarity', 'common')),
            original_price=Decimal(str(item_data['price'])),
            current_price=Decimal(str(item_data['price'])),
            is_auction=item_data.get('is_auction', False),
            expires_at=expires_at,
            attributes=json.dumps(item_data.get('attributes', {})),
            tags=json.dumps(item_data.get('tags', []))
        )
        
        # Set auction end time if it's an auction
        if listing.is_auction:
            auction_duration = item_data.get('auction_duration_hours', 72)
            listing.auction_end_time = datetime.utcnow() + timedelta(hours=auction_duration)
            listing.reserve_price = item_data.get('reserve_price')
        
        return listing
    
    @staticmethod
    def _calculate_listing_duration(item_type: str, price: Decimal) -> int:
        """Calculate optimal listing duration based on item characteristics."""
        base_days = 7
        
        # Premium items get longer listings
        if item_type in ['legendary', 'mythic']:
            base_days = 14
        elif price > Decimal('100.0'):
            base_days = 10
        
        return base_days
    
    def place_bid(self, bidder_id: str, bid_amount: Decimal) -> tuple[bool, str]:
        """Place a bid on an auction item."""
        if not self.is_auction:
            return False, "Item is not an auction"
        
        if self.status != ListingStatus.ACTIVE:
            return False, "Auction is not active"
        
        if datetime.utcnow() > self.auction_end_time:
            return False, "Auction has ended"
        
        if bidder_id == self.seller_id:
            return False, "Seller cannot bid on their own item"
        
        # Check minimum bid requirements
        min_bid = self._calculate_minimum_bid()
        if bid_amount < min_bid:
            return False, f"Bid must be at least {min_bid} Pi"
        
        # Create bid record
        bid = MarketplaceBid(
            item_id=self.id,
            bidder_id=bidder_id,
            bid_amount=bid_amount,
            placed_at=datetime.utcnow()
        )
        
        # Update highest bid
        self.highest_bid = bid_amount
        self.highest_bidder_id = bidder_id
        self.bid_count += 1
        
        # Extend auction if bid placed in last 5 minutes
        time_remaining = self.auction_end_time - datetime.utcnow()
        if time_remaining < timedelta(minutes=5):
            self.auction_end_time += timedelta(minutes=5)
        
        db.session.add(bid)
        return True, "Bid placed successfully"
    
    def _calculate_minimum_bid(self) -> Decimal:
        """Calculate minimum bid amount."""
        if not self.highest_bid:
            return self.reserve_price or self.current_price
        
        # Minimum increment based on current highest bid
        if self.highest_bid < Decimal('10.0'):
            increment = Decimal('0.5')
        elif self.highest_bid < Decimal('100.0'):
            increment = Decimal('1.0')
        else:
            increment = self.highest_bid * Decimal('0.05')  # 5% increment
        
        return self.highest_bid + increment
    
    def buy_now(self, buyer_id: str) -> tuple[bool, str]:
        """Process immediate purchase of an item."""
        if self.status != ListingStatus.ACTIVE:
            return False, "Item is not available for purchase"
        
        if self.is_auction and datetime.utcnow() < self.auction_end_time:
            return False, "Item is in auction - place a bid instead"
        
        if buyer_id == self.seller_id:
            return False, "Cannot purchase your own item"
        
        # Check buyer funds
        from app.models.user import User
        buyer = db.session.get(User, buyer_id)
        if not buyer or not buyer.can_afford(float(self.current_price)):
            return False, "Insufficient funds"
        
        # Create transaction
        from app.models.transaction import Transaction, TransactionType
        
        # Calculate platform fee (5% of sale price)
        platform_fee = self.current_price * Decimal('0.05')
        seller_amount = self.current_price - platform_fee
        
        transaction = Transaction(
            sender_id=buyer_id,
            recipient_id=self.seller_id,
            amount=self.current_price,
            net_amount=seller_amount,
            fee=platform_fee,
            transaction_type=TransactionType.MARKETPLACE_PURCHASE,
            description=f"Purchase of {self.name}",
            reference_id=self.id,
            reference_type='marketplace_item'
        )
        
        # Process the transaction
        success, error = transaction.process_transaction()
        if not success:
            return False, f"Transaction failed: {error}"
        
        # Update item status
        self.buyer_id = buyer_id
        self.status = ListingStatus.SOLD
        self.sold_at = datetime.utcnow()
        self.sale_price = self.current_price
        self.transaction_id = transaction.id
        self.platform_fee = platform_fee
        
        # Transfer item ownership
        self._transfer_item_ownership(buyer_id)
        
        return True, "Purchase completed successfully"
    
    def _transfer_item_ownership(self, new_owner_id: str) -> None:
        """Transfer item ownership in user inventory."""
        # This would integrate with an inventory system
        # For now, we'll create a record in user_items table
        from app.models.user_item import UserItem
        
        user_item = UserItem(
            user_id=new_owner_id,
            item_key=self.item_key,
            item_name=self.name,
            item_type=self.item_type.value,
            rarity=self.rarity.value,
            attributes=self.attributes,
            acquired_at=datetime.utcnow(),
            acquired_method='marketplace_purchase',
            source_transaction_id=self.transaction_id
        )
        
        db.session.add(user_item)
    
    def end_auction(self) -> tuple[bool, str]:
        """End an auction and process the sale."""
        if not self.is_auction:
            return False, "Item is not an auction"
        
        if datetime.utcnow() < self.auction_end_time:
            return False, "Auction has not ended yet"
        
        if not self.highest_bidder_id:
            self.status = ListingStatus.EXPIRED
            return False, "No bids received"
        
        if self.reserve_price and self.highest_bid < self.reserve_price:
            self.status = ListingStatus.EXPIRED
            return False, "Reserve price not met"
        
        # Process sale to highest bidder
        self.current_price = self.highest_bid
        return self.buy_now(self.highest_bidder_id)
    
    def cancel_listing(self, reason: str = None) -> bool:
        """Cancel an active listing."""
        if self.status != ListingStatus.ACTIVE:
            return False
        
        # Can't cancel auction with bids
        if self.is_auction and self.bid_count > 0:
            return False
        
        self.status = ListingStatus.CANCELLED
        if reason:
            self.verification_notes = f"Cancelled: {reason}"
        
        return True
    
    def update_price(self, new_price: Decimal) -> bool:
        """Update item price (only for non-auction items)."""
        if self.is_auction:
            return False
        
        if self.status != ListingStatus.ACTIVE:
            return False
        
        # Add price history tracking
        self._add_price_history(self.current_price, new_price)
        self.current_price = new_price
        
        return True
    
    def _add_price_history(self, old_price: Decimal, new_price: Decimal) -> None:
        """Track price changes for market analysis."""
        price_change = {
            'timestamp': datetime.utcnow().isoformat(),
            'old_price': str(old_price),
            'new_price': str(new_price),
            'change_percentage': float((new_price - old_price) / old_price * 100)
        }
        
        # This would be stored in a separate price_history table in production
        pass
    
    def get_attributes(self) -> dict:
        """Get parsed item attributes."""
        if not self.attributes:
            return {}
        try:
            return json.loads(self.attributes)
        except (json.JSONDecodeError, TypeError):
            return {}
    
    def get_tags(self) -> list:
        """Get list of item tags."""
        if not self.tags:
            return []
        try:
            return json.loads(self.tags)
        except (json.JSONDecodeError, TypeError):
            return []
    
    @hybrid_property
    def time_remaining(self) -> timedelta:
        """Calculate time remaining for listing."""
        if self.is_auction and self.auction_end_time:
            return max(timedelta(0), self.auction_end_time - datetime.utcnow())
        elif self.expires_at:
            return max(timedelta(0), self.expires_at - datetime.utcnow())
        return timedelta(0)
    
    @hybrid_property
    def is_expired(self) -> bool:
        """Check if listing has expired."""
        now = datetime.utcnow()
        if self.is_auction:
            return now > self.auction_end_time if self.auction_end_time else False
        return now > self.expires_at if self.expires_at else False
    
    def calculate_market_value(self) -> Decimal:
        """Calculate estimated market value based on similar items."""
        # This would use ML algorithms in production
        # For now, simple calculation based on rarity and attributes
        base_value = self.current_price
        
        # Rarity multiplier
        rarity_multipliers = {
            ItemRarity.COMMON: 1.0,
            ItemRarity.UNCOMMON: 1.5,
            ItemRarity.RARE: 2.5,
            ItemRarity.EPIC: 4.0,
            ItemRarity.LEGENDARY: 7.0,
            ItemRarity.MYTHIC: 12.0
        }
        
        return base_value * Decimal(str(rarity_multipliers.get(self.rarity, 1.0)))
    
    def to_dict(self, include_seller_info: bool = False) -> dict:
        """Convert item to dictionary for API responses."""
        item_data = {
            'id': self.id,
            'item_key': self.item_key,
            'name': self.name,
            'description': self.description,
            'item_type': self.item_type.value,
            'rarity': self.rarity.value,
            'current_price': str(self.current_price),
            'original_price': str(self.original_price),
            'is_auction': self.is_auction,
            'status': self.status.value,
            'listed_at': self.listed_at.isoformat(),
            'view_count': self.view_count,
            'favorite_count': self.favorite_count,
            'attributes': self.get_attributes(),
            'tags': self.get_tags(),
            'image_url': self.image_url,
            'thumbnail_url': self.thumbnail_url
        }
        
        if self.is_auction:
            item_data.update({
                'auction_end_time': self.auction_end_time.isoformat() if self.auction_end_time else None,
                'highest_bid': str(self.highest_bid) if self.highest_bid else None,
                'bid_count': self.bid_count,
                'reserve_price': str(self.reserve_price) if self.reserve_price else None,
                'time_remaining_seconds': int(self.time_remaining.total_seconds())
            })
        
        if include_seller_info and self.seller:
            item_data['seller'] = {
                'id': self.seller.id,
                'username': self.seller.username,
                'rating': self.seller_rating_at_listing or 0.0
            }
        
        return item_data

class MarketplaceBid(db.Model):
    """Auction bid tracking."""
    __tablename__ = 'marketplace_bids'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    item_id = db.Column(db.String(36), db.ForeignKey('marketplace_items.id'), nullable=False)
    bidder_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    bid_amount = db.Column(db.Numeric(precision=18, scale=8), nullable=False)
    placed_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    bidder = db.relationship('User', backref='marketplace_bids')

# Event listeners for automatic expiration handling
@event.listens_for(MarketplaceItem, 'after_update')
def check_item_expiration(mapper, connection, target):
    """Automatically expire listings that have passed their expiration date."""
    if target.is_expired and target.status == ListingStatus.ACTIVE:
        if target.is_auction:
            target.end_auction()
        else:
            target.status = ListingStatus.EXPIRED
