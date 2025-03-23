import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Configuration class to hold all the necessary environment variables.
    """

    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///default.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-secret")
    API_BASE_URL: str = os.getenv("API_BASE_URL", "https://api.minepi.com/v2")

    def __init__(self):
        """
        Initialize any additional configurations if necessary.
        """
        pass

# Example usage:
# config = Config()
# print(config.DEBUG)
# print(config.DATABASE_URL)
# print(config.SECRET_KEY)
# print(config.API_BASE_URL)
