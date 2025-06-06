"""UserQuest model for tracking a user's progress and completion status for quests."""

from datetime import datetime
from enum import Enum

from app import db
from sqlalchemy import Index
from sqlalchemy.orm import validates


class QuestStatus(Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class UserQuest(db.Model):
    __tablename__ = "user_quests"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False, index=True)
    quest_id = db.Column(db.Integer, db.ForeignKey("quests.id"), nullable=False, index=True)
    progress = db.Column(db.Float, default=0.0)
    status = db.Column(
        db.Enum(QuestStatus, name="quest_status_enum"),
        default=QuestStatus.IN_PROGRESS.value,
        nullable=False,
        index=True,
    )
    started_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    __table_args__ = (
        Index("ix_user_quests_user_id_quest_id", "user_id", "quest_id"),
    )

    @validates("progress")
    def validate_progress(self, key, value):
        if not (0.0 <= value <= 100.0):
            raise ValueError("Progress must be between 0 and 100.")
        return float(value)

    def to_dict(self):
        """Serialize the UserQuest object to a dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "quest_id": self.quest_id,
            "progress": round(self.progress, 2),
            "status": self.status.value if isinstance(self.status, QuestStatus) else self.status,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

    def update_progress(self, value: float):
        """Update progress and mark as completed if necessary."""
        self.progress = value
        if self.progress >= 100.0:
            self.progress = 100.0
            self.status = QuestStatus.COMPLETED.value
            self.completed_at = datetime.utcnow()

    def mark_completed(self):
        """Explicitly complete the quest."""
        self.progress = 100.0
        self.status = QuestStatus.COMPLETED.value
        self.completed_at = datetime.utcnow()

    def __repr__(self):
        return (
            f"<UserQuest user_id={self.user_id} quest_id={self.quest_id} "
            f"status={self.status} progress={self.progress}>"
        )
