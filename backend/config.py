class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@db:5432/palace_of_quests"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "your-secret-key"
