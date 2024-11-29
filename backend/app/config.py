class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost:5432/palace_of_quests'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your-secret-key'
    JWT_SECRET_KEY = 'your-jwt-secret-key'
