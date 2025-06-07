# tests/mock_data.py

"""Mock data objects for unit tests in Palace of Quests."""

from typing import TypedDict, List


class Player(TypedDict):
    username: str
    level: int
    experience: int


class Quest(TypedDict):
    title: str
    level_required: int
    description: str
    reward: str


class Reward(TypedDict):
    name: str
    level_required: int
    rarity: str


MOCK_PLAYER: Player = {
    "username": "mock_user",
    "level": 10,
    "experience": 1200,
}

MOCK_QUEST: Quest = {
    "title": "The Dark Cave",
    "level_required": 7,
    "description": "A perilous journey through an uncharted cavern rumored to hold ancient secrets.",
    "reward": "Silver Shield",
}

MOCK_REWARDS: List[Reward] = [
    {"name": "Golden Sword", "level_required": 50, "rarity": "legendary"},
    {"name": "Silver Shield", "level_required": 30, "rarity": "rare"},
    {"name": "Healing Potion", "level_required": 5, "rarity": "common"},
]
