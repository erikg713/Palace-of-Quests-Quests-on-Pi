import secrets
from datetime import datetime, timedelta
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import event
from app import db
import pyotp
import qrcode
from io import BytesIO
import base64

class User(UserMixin, db.Model):
    """
    Enhanced User model with comprehensive features for a professional game platform.
    """
    __tablename__ = 'users'
    
    # Core identification
    id = db.Column(db.String(36), primary_key=True, default=lambda: secrets.token_urlsafe(24))
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    
    # Enhanced authentication
    password_hash = db.Column(db.String(255), nullable=False)
    email_verified = db.Column(db.Boolean, default=False)
    email_verification_token = db.Column(db.String(100), unique=True)
    email_verification_expires = db.Column(db.DateTime)
    
    # Two-factor authentication
    two_factor_enabled = db.Column(db.Boolean, default=False)
    two_factor_secret = db.Column(db.String(32))
    backup_codes = db.Column(db.Text)  # JSON array of backup codes
    
    # Security and account management
    is_active = db.Column(db.Boolean, default=True, index=True)
    is_locked = db.Column(db.Boolean, default=False)
    lock_reason = db.Column(db.String(255))
    locked_until = db.Column(db.DateTime)
    failed_login_attempts = db.Column(db.Integer, default=0)
    last_failed_login = db.Column(db.DateTime)
    
    # Login tracking
    last_login = db.Column(db.DateTime)
    login_count = db.Column(db.Integer, default=0)
    last_ip_address = db.Column(db.String(45))  # Supports IPv6
    registration_ip = db.Column(db.String(45))
    
    # Game progression
    level = db.Column(db.Integer, default=1, index=True)
    experience_points = db.Column(db.BigInteger, default=0)
    total_quests_completed = db.Column(db.Integer, default=0)
    achievement_points = db.Column(db.Integer, default=0)
    
    # Economy and rewards
    pi_balance = db.Column(db.Numeric(precision=18, scale=8), default=0.0)
    total_pi_earned = db.Column(db.Numeric(precision=18, scale=8), default=0.0)
    total_pi_spent = db.Column(db.Numeric(precision=18, scale=8), default=0.0)
    
    # Profile and personalization
    display_name = db.Column(db.String(100))
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(255))
    timezone = db.Column(db.String(50), default='UTC')
    preferred_language = db.Column(db.String(10), default='en')
    
    # Privacy and preferences
    profile_visibility = db.Column(db.String(20), default='public')  # public, friends, private
    allow_friend_requests = db.Column(db.Boolean, default=True)
    email_notifications = db.Column(db.Boolean, default=True)
    push_notifications = db.Column(db.Boolean, default=True)
    
    # Premium features
    is_premium = db.Column(db.Boolean, default=False)
    premium_expires = db.Column(db.DateTime)
    subscription_type = db.Column(db.String(20))  # basic, premium, vip
    
    # Administrative
    role = db.Column(db.String(20), default='player', index=True)  # player, moderator, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Soft deletion
    deleted_at = db.Column(db.DateTime)
    deletion_reason = db.Column(db.String(255))
    
    # Relationships with proper lazy loading
    user_quests = db.relationship('UserQuest', backref='user', lazy='dynamic', 
                                 cascade='all, delete-orphan')
    transactions_sent = db.relationship('Transaction', foreign_keys='Transaction.sender_id', 
                                      backref='sender', lazy='dynamic')
    transactions_received = db.relationship('Transaction', foreign_keys='Transaction.recipient_id', 
                                          backref='recipient', lazy='dynamic')
    marketplace_items = db.relationship('MarketplaceItem', backref='owner', lazy='dynamic')
    achievements = db.relationship('UserAchievement', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    # Password management
    def set_password(self, password: str) -> None:
        """Set password with enhanced security options."""
        self.password_hash = generate_password_hash(
            password, 
            method='pbkdf2:sha256:150000'  # Increased iterations for better security
        )
    
    def verify_password(self, password: str) -> bool:
        """Verify password with timing attack protection."""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    # Two-factor authentication
    def enable_two_factor(self) -> str:
        """Enable 2FA and return QR code for TOTP setup."""
        if not self.two_factor_secret:
            self.two_factor_secret = pyotp.random_base32()
        
        # Generate backup codes
        backup_codes = [secrets.token_hex(4) for _ in range(10)]
        self.backup_codes = ','.join(backup_codes)
        
        # Create TOTP URI for QR code
        totp_uri = pyotp.totp.TOTP(self.two_factor_secret).provisioning_uri(
            name=self.email,
            issuer_name="Palace of Quests"
        )
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        qr_code_data = base64.b64encode(buffer.getvalue()).decode()
        
        return qr_code_data
    
    def verify_totp(self, token: str) -> bool:
        """Verify TOTP token with backup code support."""
        if not self.two_factor_secret:
            return False
        
        # Check TOTP token
        totp = pyotp.TOTP(self.two_factor_secret)
        if totp.verify(token, valid_window=1):
            return True
        
        # Check backup codes
        if self.backup_codes:
            backup_codes = self.backup_codes.split(',')
            if token in backup_codes:
                # Remove used backup code
                backup_codes.remove(token)
                self.backup_codes = ','.join(backup_codes)
                return True
        
        return False
    
    # Game progression methods
    def add_experience(self, xp_amount: int) -> dict:
        """Add experience points with level progression calculation."""
        old_level = self.level
        self.experience_points += xp_amount
        
        # Calculate new level using exponential formula
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
        """Calculate level from experience points using balanced formula."""
        import math
        if xp < 100:
            return 1
        return min(250, int(math.log(xp / 100) / math.log(1.5)) + 1)
    
    def process_level_up(self, old_level: int, new_level: int) -> list:
        """Process level up rewards and unlocks."""
        rewards = []
        
        for level in range(old_level + 1, new_level + 1):
            # Pi rewards
            pi_reward = level * 0.1
            self.pi_balance += pi_reward
            rewards.append({'type': 'pi', 'amount': pi_reward})
            
            # Special milestone rewards
            if level % 10 == 0:
                achievement_points = level * 5
                self.achievement_points += achievement_points
                rewards.append({'type': 'achievement_points', 'amount': achievement_points})
            
            # Unlock new features at specific levels
            if level == 5:
                rewards.append({'type': 'feature_unlock', 'feature': 'marketplace'})
            elif level == 10:
                rewards.append({'type': 'feature_unlock', 'feature': 'guild_system'})
            elif level == 25:
                rewards.append({'type': 'feature_unlock', 'feature': 'advanced_quests'})
        
        return rewards
    
    # Economic methods
    def can_afford(self, amount: float) -> bool:
        """Check if user can afford a transaction."""
        return float(self.pi_balance) >= amount
    
    def deduct_pi(self, amount: float, reason: str = None) -> bool:
        """Safely deduct Pi from user balance."""
        if not self.can_afford(amount):
            return False
        
        self.pi_balance -= amount
        self.total_pi_spent += amount
        return True
    
    def add_pi(self, amount: float, reason: str = None) -> None:
        """Add Pi to user balance."""
        self.pi_balance += amount
        self.total_pi_earned += amount
    
    # Utility methods
    @hybrid_property
    def is_premium_active(self) -> bool:
        """Check if premium subscription is active."""
        return (self.is_premium and 
                self.premium_expires and 
                self.premium_expires > datetime.utcnow())
    
    def has_active_quests(self) -> bool:
        """Check if user has any active quests."""
        return self.user_quests.filter_by(status='in_progress').count() > 0
    
    @property
    def is_admin(self) -> bool:
        """Check if user has admin privileges."""
        return self.role in ['admin', 'super_admin']
    
    @property
    def is_moderator(self) -> bool:
        """Check if user has moderator privileges."""
        return self.role in ['moderator', 'admin', 'super_admin']
    
    def initialize_profile(self) -> None:
        """Initialize new user profile with smart defaults."""
        self.display_name = self.username.title()
        self.registration_date = datetime.utcnow()
        
        # Start with tutorial quest
        from app.models.quest import Quest
        tutorial_quest = Quest.query.filter_by(quest_type='tutorial').first()
        if tutorial_quest:
            self.start_quest(tutorial_quest.id)
    
    def start_quest(self, quest_id: int) -> bool:
        """Start a new quest for the user."""
        from app.models.user_quest import UserQuest
        from app.models.quest import Quest
        
        quest = Quest.query.get(quest_id)
        if not quest or self.level < quest.minimum_level:
            return False
        
        # Check if already started
        existing = UserQuest.query.filter_by(
            user_id=self.id, 
            quest_id=quest_id,
            status='in_progress'
        ).first()
        
        if existing:
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
        """Convert user to dictionary for API responses."""
        public_data = {
            'id': self.id,
            'username': self.username,
            'display_name': self.display_name,
            'level': self.level,
            'achievement_points': self.achievement_points,
            'total_quests_completed': self.total_quests_completed,
            'created_at': self.created_at.isoformat(),
            'avatar_url': self.avatar_url,
            'is_premium': self.is_premium_active
        }
        
        if include_private:
            public_data.update({
                'email': self.email,
                'pi_balance': float(self.pi_balance),
                'experience_points': self.experience_points,
                'email_verified': self.email_verified,
                'two_factor_enabled': self.two_factor_enabled,
                'last_login': self.last_login.isoformat() if self.last_login else None,
                'timezone': self.timezone,
                'preferred_language': self.preferred_language
            })
        
        return public_data

# Event listeners for automatic updates
@event.listens_for(User, 'before_update')
def update_timestamp(mapper, connection, target):
    target.updated_at = datetime.utcnow()
