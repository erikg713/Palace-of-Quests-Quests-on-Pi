"""Quest model for Palace of Quests."""

from datetime import datetime, timedelta
from enum import Enum
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import event, text
from app import db
import json

class QuestType(Enum):
    TUTORIAL = "tutorial"
    MAIN_STORY = "main_story"
    SIDE_QUEST = "side_quest"
    DAILY = "daily"
    WEEKLY = "weekly"
    SPECIAL_EVENT = "special_event"
    GUILD = "guild"
    PVP = "pvp"
    COLLECTION = "collection"
    ACHIEVEMENT = "achievement"

class QuestDifficulty(Enum):
    BEGINNER = "beginner"
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"
    EXPERT = "expert"
    LEGENDARY = "legendary"

class Quest(db.Model):
    """
    Enhanced Quest model with sophisticated game mechanics and progression systems.
    """
    __tablename__ = 'quests'
    
    # Core identification
    id = db.Column(db.Integer, primary_key=True)
    quest_key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    lore_text = db.Column(db.Text)  # Rich backstory content
    
    # Quest categorization
    quest_type = db.Column(db.Enum(QuestType), default=QuestType.SIDE_QUEST, index=True)
    difficulty = db.Column(db.Enum(QuestDifficulty), default=QuestDifficulty.NORMAL, index=True)
    category = db.Column(db.String(50), index=True)  # exploration, combat, social, economic
    tags = db.Column(db.Text)  # JSON array of searchable tags
    
    # Prerequisites and requirements
    minimum_level = db.Column(db.Integer, default=1, index=True)
    maximum_level = db.Column(db.Integer)  # Optional level cap
    prerequisite_quests = db.Column(db.Text)  # JSON array of required quest IDs
    required_achievements = db.Column(db.Text)  # JSON array of achievement IDs
    required_items = db.Column(db.Text)  # JSON array of required inventory items
    
    # Rewards and economics
    pi_reward = db.Column(db.Numeric(precision=18, scale=8), default=0.0)
    experience_reward = db.Column(db.Integer, default=100)
    achievement_points_reward = db.Column(db.Integer, default=10)
    item_rewards = db.Column(db.Text)  # JSON array of reward items
    title_rewards = db.Column(db.Text)  # JSON array of unlockable titles
    
    # Time constraints
    estimated_duration = db.Column(db.Integer)  # Estimated completion time in minutes
    time_limit = db.Column(db.Integer)  # Time limit in hours (for timed quests)
    cooldown_period = db.Column(db.Integer)  # Cooldown before repeating (hours)
    
    # Availability and scheduling
    is_active = db.Column(db.Boolean, default=True, index=True)
    is_repeatable = db.Column(db.Boolean, default=False)
    is_seasonal = db.Column(db.Boolean, default=False)
    start_date = db.Column(db.DateTime)  # When quest becomes available
    end_date = db.Column(db.DateTime)    # When quest expires
    
    # Quest mechanics
    max_participants = db.Column(db.Integer, default=1)  # For group quests
    auto_complete = db.Column(db.Boolean, default=False)  # Auto-complete when objectives met
    requires_validation = db.Column(db.Boolean, default=False)  # Admin validation needed
    
    # Objectives and progression
    objectives = db.Column(db.Text, nullable=False)  # JSON array of quest objectives
    completion_criteria = db.Column(db.Text)  # JSON object defining completion rules
    bonus_objectives = db.Column(db.Text)  # JSON array of optional bonus objectives
    
    # Narrative and immersion
    start_npc = db.Column(db.String(100))  # NPC who gives the quest
    location = db.Column(db.String(100))   # Quest location/region
    story_chapter = db.Column(db.Integer)  # For main story progression
    
    # Performance and analytics
    completion_rate = db.Column(db.Float, default=0.0)  # Percentage of users who complete
    average_completion_time = db.Column(db.Integer)     # Average time to complete (minutes)
    popularity_score = db.Column(db.Float, default=0.0) # User rating/popularity
    
    # Administrative
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_modified_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    
    # Version control for quest updates
    version = db.Column(db.Integer, default=1)
    changelog = db.Column(db.Text)  # JSON array of version changes
    
    # Relationships
    user_quests = db.relationship('UserQuest', backref='quest', lazy='dynamic', 
                                 cascade='all, delete-orphan')
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_quests')
    modifier = db.relationship('User', foreign_keys=[last_modified_by])
    
    def __repr__(self):
        return f'<Quest {self.quest_key}: {self.title}>'
    
    # Objective management
    def get_objectives(self) -> list:
        """Get parsed objectives as list of dictionaries."""
        if not self.objectives:
            return []
        try:
            return json.loads(self.objectives)
        except (json.JSONDecodeError, TypeError):
            return []
    
    def set_objectives(self, objectives_list: list) -> None:
        """Set objectives from list of dictionaries."""
        self.objectives = json.dumps(objectives_list)
    
    def get_prerequisite_quests(self) -> list:
        """Get list of prerequisite quest IDs."""
        if not self.prerequisite_quests:
            return []
        try:
            return json.loads(self.prerequisite_quests)
        except (json.JSONDecodeError, TypeError):
            return []
    
    def add_prerequisite(self, quest_id: int) -> None:
        """Add a prerequisite quest."""
        prerequisites = self.get_prerequisite_quests()
        if quest_id not in prerequisites:
            prerequisites.append(quest_id)
            self.prerequisite_quests = json.dumps(prerequisites)
    
    # Rewards management
    def get_item_rewards(self) -> list:
        """Get list of item rewards."""
        if not self.item_rewards:
            return []
        try:
            return json.loads(self.item_rewards)
        except (json.JSONDecodeError, TypeError):
            return []
    
    def calculate_total_reward_value(self) -> float:
        """Calculate total monetary value of quest rewards."""
        total_value = float(self.pi_reward) if self.pi_reward else 0.0
        
        # Add estimated value of item rewards
        item_rewards = self.get_item_rewards()
        for item in item_rewards:
            if isinstance(item, dict) and 'estimated_value' in item:
                total_value += item['estimated_value']
        
        return total_value
    
    # Availability checks
    @hybrid_property
    def is_available(self) -> bool:
        """Check if quest is currently available."""
        now = datetime.utcnow()
        
        if not self.is_active:
            return False
        
        if self.start_date and now < self.start_date:
            return False
        
        if self.end_date and now > self.end_date:
            return False
        
        return True
    
    def is_available_for_user(self, user) -> tuple[bool, str]:
        """
        Check if quest is available for a specific user.
        Returns (is_available, reason_if_not)
        """
        if not self.is_available:
            return False, "Quest is not currently available"
        
        # Level requirements
        if user.level < self.minimum_level:
            return False, f"Requires level {self.minimum_level} (you are level {user.level})"
        
        if self.maximum_level and user.level > self.maximum_level:
            return False, f"Quest is only available up to level {self.maximum_level}"
        
        # Check prerequisites
        prerequisite_quest_ids = self.get_prerequisite_quests()
        if prerequisite_quest_ids:
            from app.models.user_quest import UserQuest
            completed_quests = UserQuest.query.filter(
                UserQuest.user_id == user.id,
                UserQuest.quest_id.in_(prerequisite_quest_ids),
                UserQuest.status == 'completed'
            ).count()
            
            if completed_quests < len(prerequisite_quest_ids):
                return False, "You haven't completed all prerequisite quests"
        
        # Check if already completed (for non-repeatable quests)
        if not self.is_repeatable:
            from app.models.user_quest import UserQuest
            existing_completion = UserQuest.query.filter_by(
                user_id=user.id,
                quest_id=self.id,
                status='completed'
            ).first()
            
            if existing_completion:
                return False, "Quest already completed"
        
        # Check cooldown for repeatable quests
        if self.is_repeatable and self.cooldown_period:
            from app.models.user_quest import UserQuest
            last_completion = UserQuest.query.filter_by(
                user_id=user.id,
                quest_id=self.id,
                status='completed'
            ).order_by(UserQuest.completed_at.desc()).first()
            
            if last_completion:
                cooldown_end = last_completion.completed_at + timedelta(hours=self.cooldown_period)
                if datetime.utcnow() < cooldown_end:
                    remaining = cooldown_end - datetime.utcnow()
                    return False, f"Quest on cooldown for {remaining.total_seconds() // 3600:.0f} more hours"
        
        return True, ""
    
    # Progress tracking
    def calculate_progress_percentage(self, user_quest) -> float:
        """Calculate completion percentage for a user's quest progress."""
        objectives = self.get_objectives()
        if not objectives:
            return 0.0
        
        completed_objectives = 0
        user_progress = user_quest.get_progress_data()
        
        for objective in objectives:
            objective_id = objective.get('id')
            if objective_id in user_progress:
                current = user_progress[objective_id].get('current', 0)
                target = objective.get('target', 1)
                
                if current >= target:
                    completed_objectives += 1
        
        return (completed_objectives / len(objectives)) * 100
    
    # Statistics and analytics
    def update_completion_stats(self) -> None:
        """Update quest completion statistics."""
        from app.models.user_quest import UserQuest
        from sqlalchemy import func
        
        # Calculate completion rate
        total_attempts = UserQuest.query.filter_by(quest_id=self.id).count()
        total_completions = UserQuest.query.filter_by(
            quest_id=self.id, 
            status='completed'
        ).count()
        
        if total_attempts > 0:
            self.completion_rate = (total_completions / total_attempts) * 100
        else:
            self.completion_rate = 0.0
        
        # Calculate average completion time
        avg_time = db.session.query(func.avg(
            func.extract('epoch', UserQuest.completed_at - UserQuest.started_at) / 60
        )).filter(
            UserQuest.quest_id == self.id,
            UserQuest.status == 'completed',
            UserQuest.completed_at.isnot(None)
        ).scalar()
        
        if avg_time:
            self.average_completion_time = int(avg_time)
    
    # Validation methods
    def validate_objectives(self) -> tuple[bool, list]:
        """Validate quest objectives structure."""
        objectives = self.get_objectives()
        errors = []
        
        if not objectives:
            errors.append("Quest must have at least one objective")
            return False, errors
        
        for i, objective in enumerate(objectives):
            if not isinstance(objective, dict):
                errors.append(f"Objective {i + 1} must be a dictionary")
                continue
            
            required_fields = ['id', 'description', 'type', 'target']
            for field in required_fields:
                if field not in objective:
                    errors.append(f"Objective {i + 1} missing required field: {field}")
        
        return len(errors) == 0, errors
    
    # Utility methods
    def to_dict(self, include_admin_data: bool = False) -> dict:
        """Convert quest to dictionary for API responses."""
        quest_data = {
            'id': self.id,
            'quest_key': self.quest_key,
            'title': self.title,
            'description': self.description,
            'lore_text': self.lore_text,
            'quest_type': self.quest_type.value,
            'difficulty': self.difficulty.value,
            'category': self.category,
            'minimum_level': self.minimum_level,
            'maximum_level': self.maximum_level,
            'pi_reward': float(self.pi_reward) if self.pi_reward else 0.0,
            'experience_reward': self.experience_reward,
            'achievement_points_reward': self.achievement_points_reward,
            'estimated_duration': self.estimated_duration,
            'is_repeatable': self.is_repeatable,
            'is_active': self.is_active,
            'objectives': self.get_objectives(),
            'completion_rate': self.completion_rate,
            'popularity_score': self.popularity_score,
            'created_at': self.created_at.isoformat()
        }
        
        if include_admin_data:
            quest_data.update({
                'prerequisite_quests': self.get_prerequisite_quests(),
                'item_rewards': self.get_item_rewards(),
                'version': self.version,
                'created_by': self.created_by,
                'last_modified_by': self.last_modified_by,
                'updated_at': self.updated_at.isoformat()
            })
        
        return quest_data
    
    @classmethod
    def create_tutorial_quest(cls) -> 'Quest':
        """Create a standard tutorial quest for new users."""
        tutorial_objectives = [
            {
                'id': 'complete_profile',
                'description': 'Complete your profile setup',
                'type': 'profile_action',
                'target': 1
            },
            {
                'id': 'first_login',
                'description': 'Log into the game',
                'type': 'login',
                'target': 1
            },
            {
                'id': 'explore_dashboard',
                'description': 'Visit the main dashboard',
                'type': 'navigation',
                'target': 1
            }
        ]
        
        quest = cls(
            quest_key='tutorial_welcome',
            title='Welcome to Palace of Quests',
            description='Learn the basics of playing Palace of Quests',
            quest_type=QuestType.TUTORIAL,
            difficulty=QuestDifficulty.BEGINNER,
            minimum_level=1,
            pi_reward=1.0,
            experience_reward=50,
            objectives=json.dumps(tutorial_objectives),
            is_active=True,
            auto_complete=True
        )
        
        return quest

# Event listeners for automatic updates
@event.listens_for(Quest, 'before_update')
def update_quest_timestamp(mapper, connection, target):
    target.updated_at = datetime.utcnow()
    target.version += 1

@event.listens_for(Quest, 'after_update')
def log_quest_changes(mapper, connection, target):
    """Log quest changes for audit trail."""
    # This would integrate with a logging system in production
    pass
