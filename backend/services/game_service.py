from models.level import Level
from models.user import User, db

class GameService:
    @staticmethod
    def get_all_levels():
        levels = Level.query.all()
        return [{"id": level.id, "title": level.title, "description": level.description} for level in levels]

    @staticmethod
    def update_user_progress(user_id, progress):
        user = User.query.get(user_id)
        if user:
            user.progress = progress
            db.session.commit()
            return True
        return False
