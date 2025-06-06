"""
Database Models Package
Organized model definitions with proper relationships and validation.
"""

from .user import User
from .quest import Quest, QuestProgress, QuestReward, QuestCategory
from .marketplace import Item, ItemCategory, Purchase
from .transaction import Transaction, TransactionType
from .notification import Notification
from .audit import AuditLog

__all__ = [
    'User',
    'Quest', 'QuestProgress', 'QuestReward', 'QuestCategory',
    'Item', 'ItemCategory', 'Purchase',
    'Transaction', 'TransactionType',
    'Notification',
    'AuditLog'
]

"""
app.models

This package defines the ORM models for the Palace of Quests (Pi Quest) application,
representing core entities and their relationships in the virtual metaverse.

Models:
    - User:         Player accounts and profile management
    - Quest:        Adventure and challenge definitions
    - Item:         Virtual assets and collectibles
    - Transaction:  In-game transactions and reward tracking
    - UserQuest:    Player progress and quest participation
"""

from app.models.user import User
from app.models.quest import Quest
from app.models.item import Item
from app.models.transaction import Transaction
from app.models.user_quest import UserQuest

__all__ = (
    "User",
    "Quest",
    "Item",
    "Transaction",
    "UserQuest",
)
