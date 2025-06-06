import base64
import json
import math
import secrets
from datetime import datetime, timedelta
from io import BytesIO

import pyotp
import qrcode
from flask import current_app
from flask_login import UserMixin
from sqlalchemy import event
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from app import db
import uuid
from datetime import datetime

bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)  # Renamed to password_hash
    role = db.Column(db.String(20), default='user')  # 'user' or 'admin'
    level = db.Column(db.Integer, default=1)
    xp = db.Column(db.Float, default=0.0)
    rewards = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def add_xp(self, xp_gained):
        self.xp += xp_gained
        while self.xp >= 100:  # Level up when XP reaches 100
            self.level += 1
            self.xp -= 100

    def __repr__(self):
        return f"<User {self.username}>"
from app import db

class User(UserMixin, db.Model):
    """User model for Palace of Quests – handles authentication, progression, and economy."""

    __tablename__ = 'users'

    # Identification
    id = db.Column(db.String(36), primary_key=True, default=lambda: secrets.token_urlsafe(24))
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)

    # Authentication & Security
    password_hash = db.Column(db.String(255), nullable=False)
    email_verified = db.Column(db.Boolean, default=False)
    email_verification_token = db.Column(db.String(100), unique=True)
    email_verification_expires = db.Column(db.DateTime)
    two_factor_enabled = db.Column(db.Boolean, default=False)
    two_factor_secret = db.Column(db.String(64))
    backup_codes = db.Column(db.Text)  # Comma-separated, consider encryption for production
    is_active = db.Column(db.Boolean, default=True, index=True)
    is_locked = db.Column(db.Boolean, default=False)
    lock_reason = db.Column(db.String(255))
    locked_until = db.Column(db.DateTime)
    failed_login_attempts = db.Column(db.Integer, default=0)
    last_failed_login = db.Column(db.DateTime)

    # Login tracking
    last_login = db.Column(db.DateTime)
    login_count = db.Column(db.Integer, default=0)
    last_ip_address = db.Column(db.String(45))  # IPv4/IPv6
    registration_ip = db.Column(db.String(45))

    # Game progression
    level = db.Column(db.Integer, default=1, index=True)
    experience_points = db.Column(db.BigInteger, default=0)
    total_quests_completed = db.Column(db.Integer, default=0)
    achievement_points = db.Column(db.Integer, default=0)

    # Economy and rewards
    pi_balance = db.Column(db.Numeric(18, 8), default=0)
    total_pi_earned = db.Column(db.Numeric(18, 8), default=0)
    total_pi_spent = db.Column(db.Numeric(18, 8), default=0)

    # Profile and personalization
    display_name = db.Column(db.String(100))
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(255))
    timezone = db.Column(db.String(50), default='UTC')
    preferred_language = db.Column(db.String(10), default='en')

    # Privacy and preferences
    profile_visibility = db.Column(db.String(20), default='public')
    allow_friend_requests = db.Column(db.Boolean, default=True)
    email_notifications = db.Column(db.Boolean, default=True)
    push_notifications = db.Column(db.Boolean, default=True)

    # Premium features
    is_premium = db.Column(db.Boolean, default=False)
    premium_expires = db.Column(db.DateTime)
    subscription_type = db.Column(db.String(20))

    # Administrative
    role = db.Column(db.String(20), default='player', index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Soft deletion
    deleted_at = db.Column(db.DateTime)
    deletion_reason = db.Column(db.String(255))

    # Relationships
    user_quests = db.relationship('UserQuest', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    transactions_sent = db.relationship('Transaction', foreign_keys='Transaction.sender_id', backref='sender', lazy='dynamic')
    transactions_received = db.relationship('Transaction', foreign_keys='Transaction.recipient_id', backref='recipient', lazy='dynamic')
    marketplace_items = db.relationship('MarketplaceItem', backref='owner', lazy='dynamic')
    achievements = db.relationship('UserAchievement', backref='user', lazy='dynamic')

    def __repr__(self):
        return f"<User {self.username}>"

    # Password management
    def set_password(self, password: str) -> None:
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(
            password,
            method='pbkdf2:sha256:200000'
        )

    def verify_password(self, password: str) -> bool:
        """Check a plaintext password against the stored hash."""
        return self.password_hash and check_password_hash(self.password_hash, password)

    # Two-factor authentication
    def enable_two_factor(self) -> str:
        """Enable 2FA and generate a QR code. Returns base64-encoded PNG."""
        if not self.two_factor_secret:
            self.two_factor_secret = pyotp.random_base32()

        # Generate backup codes
        codes = [secrets.token_hex(4) for _ in range(10)]
        self.backup_codes = ','.join(codes)

        totp_uri = pyotp.totp.TOTP(self.two_factor_secret).provisioning_uri(
            name=self.email,
            issuer_name=current_app.config.get('APP_NAME', 'Palace of Quests')
        )

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        return base64.b64encode(buffer.getvalue()).decode()

    def verify_totp(self, token: str) -> bool:
        """Verify a TOTP token or backup code."""
        if not self.two_factor_secret:
            return False
        totp = pyotp.TOTP(self.two_factor_secret)
        if totp.verify(token, valid_window=1):
            return True
        if self.backup_codes:
            codes = self.backup_codes.split(',')
            if token in codes:
                codes.remove(token)
                self.backup_codes = ','.join(codes)
                return True
        return False

    # Game progression
    def add_experience(self, xp_amount: int) -> dict:
        """Add experience and handle level-ups. Returns a summary dict."""
        old_level = self.level
        self.experience_points += xp_amount
        new_level = self.calculate_level_from_xp(self.experience_points)
        level_up_rewards = []
        if new_level > old_level:
            self.level = new_level
            level_up_rewards = self.process_level_up(old_level, new_level)
        return {
            'xp_gained': xp_amount,
            'total_xp': self.experience_points,
            'old_level': old_level,
            'new_level': self.level,
            'level_up_rewards': level_up_rewards
        }

    @staticmethod
    def calculate_level_from_xp(xp: int) -> int:
        """Calculate level using a smooth progression curve."""
        if xp < 100:
            return 1
        return min(250, int(math.log(xp / 100) / math.log(1.5)) + 1)

    def process_level_up(self, old_level: int, new_level: int) -> list:
        """Handle rewards/unlocks for each level-up."""
        rewards = []
        for level in range(old_level + 1, new_level + 1):
            pi_reward = level * 0.1
            self.pi_balance += pi_reward
            rewards.append({'type': 'pi', 'amount': float(pi_reward)})
            if level % 10 == 0:
                achievement = level * 5
                self.achievement_points += achievement
                rewards.append({'type': 'achievement_points', 'amount': achievement})
            # Feature unlocks
            if level == 5:
                rewards.append({'type': 'feature_unlock', 'feature': 'marketplace'})
            elif level == 10:
                rewards.append({'type': 'feature_unlock', 'feature': 'guild_system'})
            elif level == 25:
                rewards.append({'type': 'feature_unlock', 'feature': 'advanced_quests'})
        return rewards

    # Economic methods
    def can_afford(self, amount: float) -> bool:
        """Check if user has enough Pi."""
        try:
            return float(self.pi_balance) >= amount
        except Exception:
            return False

    def deduct_pi(self, amount: float, reason: str = None) -> bool:
        """Deduct Pi if possible; returns True if successful."""
        if not self.can_afford(amount):
            return False
        self.pi_balance -= amount
        self.total_pi_spent += amount
        # Optionally log deduction reason here
        return True

    def add_pi(self, amount: float, reason: str = None) -> None:
        """Add Pi to user."""
        self.pi_balance += amount
        self.total_pi_earned += amount
        # Optionally log addition reason here

    # Premium subscription
    @hybrid_property
    def is_premium_active(self) -> bool:
        """True if user currently has premium."""
        return bool(self.is_premium and self.premium_expires and self.premium_expires > datetime.utcnow())

    # Quest utilities
    def has_active_quests(self) -> bool:
        """Check for any in-progress quests."""
        return self.user_quests.filter_by(status='in_progress').count() > 0

    @property
    def is_admin(self) -> bool:
        """True if user is admin or super_admin."""
        return self.role in ('admin', 'super_admin')

    @property
    def is_moderator(self) -> bool:
        """True if user is moderator or above."""
        return self.role in ('moderator', 'admin', 'super_admin')

    def initialize_profile(self) -> None:
        """Initialize new user profile with defaults and tutorial quest."""
        self.display_name = self.username.title()
        self.created_at = datetime.utcnow()
        # Assign tutorial quest if available
        from app.models.quest import Quest
        tutorial_quest = Quest.query.filter_by(quest_type='tutorial').first()
        if tutorial_quest:
            self.start_quest(tutorial_quest.id)

    def start_quest(self, quest_id: int) -> bool:
        """Start a quest for the user if eligible."""
        from app.models.user_quest import UserQuest
        from app.models.quest import Quest

        quest = Quest.query.get(quest_id)
        if not quest or self.level < getattr(quest, 'minimum_level', 1):
            return False

        exists = UserQuest.query.filter_by(
            user_id=self.id,
            quest_id=quest_id,
            status='in_progress'
        ).first()
        if exists:
            return False

        user_quest = UserQuest(
            user_id=self.id,
            quest_id=quest_id,
            status='in_progress',
            started_at=datetime.utcnow()
        )
        db.session.add(user_quest)
        return True

    def to_dict(self, include_private: bool = False) -> dict:
        """Serialize user for API output."""
        data = {
            'id': self.id,
            'username': self.username,
            'display_name': self.display_name,
            'level': self.level,
            'achievement_points': self.achievement_points,
            'total_quests_completed': self.total_quests_completed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'avatar_url': self.avatar_url,
            'is_premium': self.is_premium_active
        }
        if include_private:
            data.update({
                'email': self.email,
                'pi_balance': float(self.pi_balance),
                'experience_points': self.experience_points,
                'email_verified': self.email_verified,
                'two_factor_enabled': self.two_factor_enabled,
                'last_login': self.last_login.isoformat() if self.last_login else None,
                'timezone': self.timezone,
                'preferred_language': self.preferred_language
            })
        return data

# Auto-update timestamps
@event.listens_for(User, 'before_update')
def update_timestamp(mapper, connection, target):
    target.updated_at = datetime.utcnow()
