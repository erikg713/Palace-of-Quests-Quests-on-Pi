"""
User Model with Enhanced Security and Game Mechanics
Professional implementation with proper validation and business logic.
"""

import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy import event
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.core.exceptions import ValidationError
from app.utils.validators import validate_email, validate_username


class User(db.Model):
    """
    User model with comprehensive game mechanics and security features.
    Implements level progression, achievement tracking, and secure authentication.
    """
    
    __tablename__ = 'users'
    
    # Primary identification
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(30), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Pi Network integration
    pi_user_id = db.Column(db.String(100), unique=True, nullable=True, index=True)
    pi_username = db.Column(db.String(50), nullable=True)
    
    # Profile information
    display_name = db.Column(db.String(50), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    avatar_url = db.Column(db.String(500), nullable=True)
    
    # Game progression
    level = db.Column(db.Integer, default=1, nullable=False)
    experience_points = db.Column(db.BigInteger, default=0, nullable=False)
    total_rewards = db.Column(db.Numeric(precision=20, scale=8), default=0, nullable=False)
    
    # Account status and security
    role = db.Column(db.String(20), default='player', nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    email_verified_at = db.Column(db.DateTime, nullable=True)
    last_login_at = db.Column(db.DateTime, nullable=True)
    failed_login_attempts = db.Column(db.Integer, default=0, nullable=False)
    locked_until = db.Column(db.DateTime, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    quest_progress = db.relationship('QuestProgress', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    transactions_sent = db.relationship('Transaction', foreign_keys='Transaction.sender_id', backref='sender', lazy='dynamic')
    transactions_received = db.relationship('Transaction', foreign_keys='Transaction.receiver_id', backref='receiver', lazy='dynamic')
    marketplace_items = db.relationship('Item', backref='seller', lazy='dynamic')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    # Constraints
    __table_args__ = (
        db.CheckConstraint('level >= 1', name='valid_level'),
        db.CheckConstraint('experience_points >= 0', name='valid_experience'),
        db.CheckConstraint('total_rewards >= 0', name='valid_rewards'),
        db.CheckConstraint('failed_login_attempts >= 0', name='valid_failed_attempts'),
        db.Index('idx_user_level_xp', 'level', 'experience_points'),
        db.Index('idx_user_pi_integration', 'pi_user_id', 'pi_username'),
    )
    
    def __init__(self, **kwargs):
        """Initialize user with validation."""
        if 'username' in kwargs:
            if not validate_username(kwargs['username']):
                raise ValidationError("Invalid username format")
        
        if 'email' in kwargs:
            if not validate_email(kwargs['email']):
                raise ValidationError("Invalid email format")
        
        super().__init__(**kwargs)
    
    @property
    def is_admin(self) -> bool:
        """Check if user has admin privileges."""
        return self.role in ['admin', 'super_admin']
    
    @property
    def is_locked(self) -> bool:
        """Check if account is temporarily locked."""
        return (self.locked_until and 
                self.locked_until > datetime.utcnow())
    
    @hybrid_property
    def experience_to_next_level(self) -> int:
        """Calculate XP needed for next level."""
        return self._calculate_xp_for_level(self.level + 1) - self.experience_points
    
    @hybrid_property
    def level_progress_percentage(self) -> float:
        """Calculate percentage progress to next level."""
        current_level_xp = self._calculate_xp_for_level(self.level)
        next_level_xp = self._calculate_xp_for_level(self.level + 1)
        level_xp_range = next_level_xp - current_level_xp
        current_progress = self.experience_points - current_level_xp
        return min(100.0, (current_progress / level_xp_range) * 100)
    
    def set_password(self, password: str) -> None:
        """Set user password with proper hashing."""
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    
    def verify_password(self, password: str) -> bool:
        """Verify password against stored hash."""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def add_experience(self, xp_amount: int, source: str = None) -> Dict[str, Any]:
        """
        Add experience points and handle level progression.
        
        Args:
            xp_amount: Amount of XP to add
            source: Source of XP gain for tracking
            
        Returns:
            Dictionary with level up information
        """
        if xp_amount <= 0:
            raise ValidationError("Experience amount must be positive")
        
        old_level = self.level
        self.experience_points += xp_amount
        
        # Check for level ups
        new_level = self._calculate_level_from_xp(self.experience_points)
        levels_gained = max(0, new_level - self.level)
        
        if levels_gained > 0:
            self.level = new_level
            # Award level-up rewards
            level_rewards = self._calculate_level_rewards(old_level, new_level)
            self.total_rewards += level_rewards
            
            return {
                'xp_gained': xp_amount,
                'levels_gained': levels_gained,
                'new_level': new_level,
                'level_rewards': float(level_rewards),
                'leveled_up': True
            }
        
        return {
            'xp_gained': xp_amount,
            'levels_gained': 0,
            'new_level': self.level,
            'level_rewards': 0,
            'leveled_up': False
        }
    
    def record_login_attempt(self, successful: bool, ip_address: str = None) -> None:
        """Record login attempt and handle account locking."""
        if successful:
            self.last_login_at = datetime.utcnow()
            self.failed_login_attempts = 0
            self.locked_until = None
        else:
            self.failed_login_attempts += 1
            
            # Lock account after 5 failed attempts
            if self.failed_login_attempts >= 5:
                self.locked_until = datetime.utcnow() + timedelta(minutes=30)
    
    def unlock_account(self) -> None:
        """Manually unlock user account."""
        self.failed_login_attempts = 0
        self.locked_until = None
    
    def verify_email(self) -> None:
        """Mark email as verified."""
        self.is_verified = True
        self.email_verified_at = datetime.utcnow()
    
    def deactivate(self) -> None:
        """Deactivate user account."""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def activate(self) -> None:
        """Activate user account."""
        self.is_active = True
        self.updated_at = datetime.utcnow()
    
    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """Convert user to dictionary representation."""
        data = {
            'id': self.id,
            'username': self.username,
            'display_name': self.display_name or self.username,
            'level': self.level,
            'experience_points': self.experience_points,
            'experience_to_next_level': self.experience_to_next_level,
            'level_progress_percentage': round(self.level_progress_percentage, 2),
            'total_rewards': float(self.total_rewards),
            'role': self.role,
            'is_verified': self.is_verified,
            'avatar_url': self.avatar_url,
            'created_at': self.created_at.isoformat(),
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None
        }
        
        if include_sensitive:
            data.update({
                'email': self.email,
                'is_active': self.is_active,
                'is_locked': self.is_locked,
                'failed_login_attempts': self.failed_login_attempts
            })
        
        return data
    
    @staticmethod
    def _calculate_xp_for_level(level: int) -> int:
        """Calculate total XP required for a specific level."""
        if level <= 1:
            return 0
        # Exponential XP curve: XP = 100 * level^1.5
        return int(100 * (level ** 1.5))
    
    @staticmethod
    def _calculate_level_from_xp(total_xp: int) -> int:
        """Calculate level based on total XP."""
        level = 1
        while User._calculate_xp_for_level(level + 1) <= total_xp:
            level += 1
        return level
    
    @staticmethod
    def _calculate_level_rewards(old_level: int, new_level: int) -> float:
        """Calculate Pi rewards for leveling up."""
        total_rewards = 0.0
        for level in range(old_level + 1, new_level + 1):
            # Base reward increases with level
            base_reward = 0.1 * (1 + (level - 1) * 0.1)
            total_rewards += base_reward
        return total_rewards
    
    def __repr__(self) -> str:
        return f"<User {self.username} (Level {self.level})>"


# Event listeners for automatic updates
@event.listens_for(User, 'before_update')
def update_modified_timestamp(mapper, connection, target):
    """Update timestamp on model changes."""
    target.updated_at = datetime.utcnow()


@event.listens_for(User.username, 'set')
def validate_username_change(target, value, old_value, initiator):
    """Validate username on change."""
    if value and not validate_username(value):
        raise ValidationError("Invalid username format")


@event.listens_for(User.email, 'set')
def validate_email_change(target, value, old_value, initiator):
    """Validate email on change."""
    if value and not validate_email(value):
        raise ValidationError("Invalid email format")
