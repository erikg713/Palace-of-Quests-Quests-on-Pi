from app import db

class LevelReward(db.Model):
    __tablename__ = 'level_rewards'

    level = db.Column(db.Integer, primary_key=True)
    reward_name = db.Column(db.String(100), nullable=False)
    reward_description = db.Column(db.String(255), nullable=False)
    stat_boost = db.Column(db.Integer, default=0)
    item_unlock = db.Column(db.String(100), nullable=True)
    quest_difficulty = db.Column(db.Integer, default=1)

    def to_dict(self):
        return {
            "level": self.level,
            "reward_name": self.reward_name,
            "reward_description": self.reward_description,
            "stat_boost": self.stat_boost,
            "item_unlock": self.item_unlock,
            "quest_difficulty": self.quest_difficulty
        }