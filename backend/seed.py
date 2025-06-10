"""
Seed script for Palace of Quests (Pi Quest) backend.
Creates an admin user if not already present.
"""

import os
import logging
import argparse
from dotenv import load_dotenv
import bcrypt
from app import create_app, db
from app.models.user import User

# Load environment variables from .env file if present
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

app = create_app()

def create_admin_user(username: str, email: str, raw_password: str, wallet_address: str) -> bool:
    """Create admin user if not exists."""
    existing = User.query.filter_by(email=email).first()
    if existing:
        logger.warning("Admin user already exists.")
        return False

    hashed = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    admin_user = User(
        username=username,
        email=email,
        password_hash=hashed,
        pi_wallet_address=wallet_address
    )
    try:
        db.session.add(admin_user)
        db.session.commit()
        logger.info(f"Admin user '{username}' created successfully.")
        return True
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to create admin user: {e}")
        return False

def parse_args():
    parser = argparse.ArgumentParser(description="Seed admin user for Palace of Quests (Pi Quest).")
    parser.add_argument("--email", default=os.getenv("ADMIN_EMAIL", "admin@example.com"))
    parser.add_argument("--username", default=os.getenv("ADMIN_USERNAME", "admin"))
    parser.add_argument("--password", default=os.getenv("ADMIN_PASSWORD", "ChangeThisPassword123!"))
    parser.add_argument("--wallet", default=os.getenv("ADMIN_WALLET_ADDRESS", "pi_wallet_address_123456789012345"))
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    with app.app_context():
        create_admin_user(args.username, args.email, args.password, args.wallet)
