class Avatar(db.Model):
    __tablename__ = 'avatars'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    level = db.Column(db.Integer, default=1)
    stat_points = db.Column(db.Integer, default=0)

    # A list of items that the avatar owns
    items = db.relationship('Item', backref='avatar', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "level": self.level,
            "stat_points": self.stat_points
        }