"""
Quest System Models with Advanced Game Mechanics
Comprehensive quest management with categories, rewards, and progress tracking.
"""

import uuid
import enum
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy import event
from sqlalchemy.ext.hybrid import hybrid_property

from app.extensions import db
from app.core.exceptions import ValidationError


class QuestType(enum.Enum):
    """Quest type enumeration."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    SPECIAL = "special"
    STORY = "story"
    ACHIEVEMENT = "achievement"


class QuestStatus(enum.Enum):
    """Quest status enumeration."""
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class QuestDifficulty(enum.Enum):
    """Quest difficulty levels."""
    BEGINNER = "beginner"
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"
    LEGENDARY = "legendary"


class QuestCategory(db.Model):
    """Quest categories for organization and filtering."""
    
    __tablename__ = 'quest_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(100), nullable=True)
    color = db.Column(db.String(7), nullable=True)  # Hex color
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    quests = db.relationship('Quest', backref='category', lazy='dynamic')
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'color': self.color,
            'quest_count': self.quests.filter_by(status=QuestStatus.ACTIVE).count()
        }


class Quest(db.Model):
    """
    Enhanced quest model with comprehensive game mechanics.
    Supports various quest types, difficulty levels, and reward systems.
    """
    
    __tablename__ = 'quests'
    
    # Primary identification
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(500), nullable=True)
    
    # Quest classification
    quest_type = db.Column(db.Enum(QuestType), default=QuestType.DAILY, nullable=False)
    difficulty = db.Column(db.Enum(QuestDifficulty), default=QuestDifficulty.EASY, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('quest_categories.id'), nullable=True)
    
    # Requirements and constraints
    level_required = db.Column(db.Integer, default=1, nullable=False)
    max_participants = db.Column(db.Integer, nullable=True)  # Null = unlimited
    prerequisites = db.Column(db.JSON, nullable=True)  # List of quest IDs
    
    # Rewards
    pi_reward = db.Column(db.Numeric(precision=20, scale=8), default=0, nullable=False)
    xp_reward = db.Column(db.Integer, default=0, nullable=False)
    bonus_rewards = db.Column(db.JSON, nullable=True)  # Additional rewards
    
    # Quest mechanics
    objective_type = db.Column(db.String(50), nullable=False, default='simple')  # simple, progressive, collection
    objective_target = db.Column(db.Integer, nullable=True)  # Target for progressive quests
    objective_data = db.Column(db.JSON, nullable=True)  # Additional objective data
    
    # Status and timing
    status = db.Column(db.Enum(QuestStatus), default=QuestStatus.DRAFT, nullable=False)
    starts_at = db.Column(db.DateTime, nullable=True)
    expires_at = db.Column(db.DateTime, nullable=True)
    estimated_duration = db.Column(db.Integer, nullable=True)  # Minutes
    
    # Metadata
    creator_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    tags = db.Column(db.JSON, nullable=True)  # List of tags
    instructions = db.Column(db.Text, nullable=True)
    success_criteria = db.Column(db.Text, nullable=True)
    
    # Analytics
    total_participants = db.Column(db.Integer, default=0, nullable=False)
    total_completions = db.Column(db.Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    progress_records = db.relationship('QuestProgress', backref='quest', lazy='dynamic', cascade='all, delete-orphan')
    creator = db.relationship('User', backref='created_quests', foreign_keys=[creator_id])
    
    # Constraints
    __table_args__ = (
        db.CheckConstraint('level_required >= 1', name='valid_level_requirement'),
        db.CheckConstraint('pi_reward >= 0', name='valid_pi_reward'),
        db.CheckConstraint('xp_reward >= 0', name='valid_xp_reward'),
        db.CheckConstraint('total_participants >= 0', name='valid_participants'),
        db.CheckConstraint('total_completions >= 0', name='valid_completions'),
        db.Index('idx_quest_status_type', 'status', 'quest_type'),
        db.Index('idx_quest_difficulty_level', 'difficulty', 'level_required'),
        db.Index('idx_quest_timing', 'starts_at', 'expires_at'),
    )
    
    @hybrid_property
    def is_active(self) -> bool:
        """Check if quest is currently active."""
        now = datetime.utcnow()
        return (self.status == QuestStatus.ACTIVE and
                (self.starts_at is None or self.starts_at <= now) and
                (self.expires_at is None or self.expires_at > now))
    
    @hybrid_property
    def is_expired(self) -> bool:
        """Check if quest has expired."""
        return (self.expires_at is not None and 
                self.expires_at <= datetime.utcnow())
    
    @hybrid_property
    def completion_rate(self) -> float:
        """Calculate quest completion rate."""
        if self.total_participants == 0:
            return 0.0
        return (self.total_completions / self.total_participants) * 100
    
    @hybrid_property
    def difficulty_multiplier(self) -> float:
        """Get reward multiplier based on difficulty."""
        multipliers = {
            QuestDifficulty.BEGINNER: 0.5,
            QuestDifficulty.EASY: 1.0,
            QuestDifficulty.MEDIUM: 1.5,
            QuestDifficulty.HARD: 2.0,
            QuestDifficulty.EXPERT: 3.0,
            QuestDifficulty.LEGENDARY: 5.0
        }
        return multipliers.get(self.difficulty, 1.0)
    
    def can_participate(self, user) -> tuple[bool, str]:
        """
        Check if user can participate in this quest.
        
        Returns:
            Tuple of (can_participate, reason)
        """
        if not self.is_active:
            return False, "Quest is not active"
        
        if user.level < self.level_required:
            return False, f"Level {self.level_required} required"
        
        if self.max_participants and self.total_participants >= self.max_participants:
            return False, "Quest is full"
        
        # Check if user already has progress on this quest
        existing_progress = self.progress_records.filter_by(user_id=user.id).first()
        if existing_progress and existing_progress.status == 'completed':
            return False, "Quest already completed"
        
        # Check prerequisites
        if self.prerequisites:
            for prereq_id in self.prerequisites:
                prereq_progress = QuestProgress.query.filter_by(
                    user_id=user.id,
                    quest_id=prereq_id,
                    status='completed'
                ).first()
                if not prereq_progress:
                    return False, "Prerequisites not met"
        
        return True, "Eligible"
    
    def start_for_user(self, user) -> 'QuestProgress':
        """Start quest for a user."""
        can_participate, reason = self.can_participate(user)
        if not can_participate:
            raise ValidationError(f"Cannot start quest: {reason}")
        
        # Check for existing progress
        progress = self.progress_records.filter_by(user_id=user.id).first()
        if not progress:
            progress = QuestProgress(
                user_id=user.id,
                quest_id=self.id,
                status='in_progress'
            )
            db.session.add(progress)
            self.total_participants += 1
        
        return progress
    
    def complete_for_user(self, user) -> Dict[str, Any]:
        """Complete quest for a user and award rewards."""
        progress = self.progress_records.filter_by(
            user_id=user.id,
            status='in_progress'
        ).first()
        
        if not progress:
            raise ValidationError("No active progress found for this quest")
        
        # Mark as completed
        progress.complete()
        self.total_completions += 1
        
        # Calculate and award rewards
        total_pi_reward = float(self.pi_reward * self.difficulty_multiplier)
        total_xp_reward = int(self.xp_reward * self.difficulty_multiplier)
        
        # Award XP
        xp_result = user.add_experience(total_xp_reward, f"Quest: {self.title}")
        
        # Award Pi rewards
        user.total_rewards += total_pi_reward
        
        return {
            'quest_completed': True,
            'pi_reward': total_pi_reward,
            'xp_reward': total_xp_reward,
            'xp_result': xp_result,
            'bonus_rewards': self.bonus_rewards or {}
        }
    
    def to_dict(self, user=None) -> Dict[str, Any]:
        """Convert quest to dictionary representation."""
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'short_description': self.short_description,
            'quest_type': self.quest_type.value,
            'difficulty': self.difficulty.value,
            'level_required': self.level_required,
            'pi_reward': float(self.pi_reward),
            'xp_reward': self.xp_reward,
            'status': self.status.value,
            'completion_rate': round(self.completion_rate, 2),
            'total_participants': self.total_participants,
            'total_completions': self.total_completions,
            'estimated_duration': self.estimated_duration,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'category': self.category.to_dict() if self.category else None,
            'tags': self.tags or []
        }
        
        if user:
            progress = self.progress_records.filter_by(user_id=user.id).first()
            can_participate, reason = self.can_participate(user)
            
            data.update({
                'user_progress': progress.to_dict() if progress else None,
                'can_participate': can_participate,
                'participation_reason': reason
            })
        
        return data
    
    def __repr__(self) -> str:
        return f"<Quest {self.title} ({self.difficulty.value})>"


class QuestProgress(db.Model):
    """
    Tracks individual user progress on quests.
    Supports various progress types and detailed tracking.
    """
    
    __tablename__ = 'quest_progress'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    quest_id = db.Column(db.String(36), db.ForeignKey('quests.id'), nullable=False)
    
    # Progress tracking
    status = db.Column(db.String(20), default='in_progress', nullable=False)
    progress_value = db.Column(db.Integer, default=0, nullable=False)
    progress_data = db.Column(db.JSON, nullable=True)  # Additional progress data
    
    # Timing
    started_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Constraints
    __table_args__ = (
        db.UniqueConstraint('user_id', 'quest_id', name='unique_user_quest'),
        db.CheckConstraint('progress_value >= 0', name='valid_progress'),
        db.Index('idx_progress_status_updated', 'status', 'last_updated'),
    )
    
    @hybrid_property
    def progress_percentage(self) -> float:
        """Calculate progress percentage."""
        if not self.quest.objective_target:
            return 100.0 if self.status == 'completed' else 0.0
        
        return min(100.0, (self.progress_value / self.quest.objective_target) * 100)
    
    def update_progress(self, value: int, data: Dict[str, Any] = None) -> bool:
        """
        Update quest progress.
        
        Args:
            value: New progress value
            data: Additional progress data
            
        Returns:
            True if quest was completed
        """
        if self.status == 'completed':
            return False
        
        self.progress_value = max(0, value)
        if data:
            self.progress_data = {**(self.progress_data or {}), **data}
        
        # Check for completion
        if (self.quest.objective_target and 
            self.progress_value >= self.quest.objective_target):
            self.complete()
            return True
        
        return False
    
    def complete(self) -> None:
        """Mark quest progress as completed."""
        self.status = 'completed'
        self.completed_at = datetime.utcnow()
        
        if self.quest.objective_target:
            self.progress_value = self.quest.objective_target
    
    def abandon(self) -> None:
        """Abandon quest progress."""
        self.status = 'abandoned'
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert progress to dictionary representation."""
        return {
            'id': self.id,
            'status': self.status,
            'progress_value': self.progress_value,
            'progress_percentage': round(self.progress_percentage, 2),
            'progress_data': self.progress_data or {},
            'started_at': self.started_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'last_updated': self.last_updated.isoformat()
        }
    
    def __repr__(self) -> str:
        return f"<QuestProgress {self.user_id}:{self.quest_id} ({self.status})>"


class QuestReward(db.Model):
    """
    Tracks quest reward distribution and history.
    Maintains audit trail for all quest-related rewards.
    """
    
    __tablename__ = 'quest_rewards'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    quest_id = db.Column(db.String(36), db.ForeignKey('quests.id'), nullable=False)
    progress_id = db.Column(db.String(36), db.ForeignKey('quest_progress.id'), nullable=False)
    
    # Reward details
    pi_amount = db.Column(db.Numeric(precision=20, scale=8), default=0, nullable=False)
    xp_amount = db.Column(db.Integer, default=0, nullable=False)
    bonus_rewards = db.Column(db.JSON, nullable=True)
    
    # Metadata
    awarded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    difficulty_multiplier = db.Column(db.Float, default=1.0, nullable=False)
    
    # Relationships
    user = db.relationship('User', backref='quest_rewards')
    quest = db.relationship('Quest', backref='reward_history')
    progress = db.relationship('QuestProgress', backref='reward')
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert reward to dictionary representation."""
        return {
            'id': self.id,
            'pi_amount': float(self.pi_amount),
            'xp_amount': self.xp_amount,
            'bonus_rewards': self.bonus_rewards or {},
            'difficulty_multiplier': self.difficulty_multiplier,
            'awarded_at': self.awarded_at.isoformat(),
            'quest': {
                'id': self.quest.id,
                'title': self.quest.title,
                'difficulty': self.quest.difficulty.value
            }
        }


# Event listeners for automatic updates
@event.listens_for(Quest, 'before_update')
def update_quest_timestamp(mapper, connection, target):
    """Update timestamp on quest changes."""
    target.updated_at = datetime.utcnow()


@event.listens_for(Quest.status, 'set')
def handle_quest_status_change(target, value, old_value, initiator):
    """Handle quest status changes."""
    if value == QuestStatus.ACTIVE and target.starts_at is None:
        target.starts_at = datetime.utcnow()


@event.listens_for(QuestProgress, 'after_update')
def handle_progress_completion(mapper, connection, target):
    """Handle quest completion events."""
    if target.status == 'completed' and target.completed_at:
        # Create reward record
        reward = QuestReward(
            user_id=target.user_id,
            quest_id=target.quest_id,
            progress_id=target.id,
            pi_amount=target.quest.pi_reward,
            xp_amount=target.quest.xp_reward,
            bonus_rewards=target.quest.bonus_rewards,
            difficulty_multiplier=target.quest.difficulty_multiplier
        )
        db.session.add(reward)

from app.extensions import db

class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Quest {self.name}>"
