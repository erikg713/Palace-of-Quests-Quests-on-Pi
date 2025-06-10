# seed.py
import os
import bcrypt
from app import create_app, db
from app.models.user import User

app = create_app()

def seed_admin():
    with app.app_context():
        admin_email = "admin@example.com"
        admin_username = "admin"
        raw_password = "ChangeThisPassword123!"  # Use a strong password!
        wallet_address = "pi_wallet_address_123456789012345"

        # Check if user already exists
        existing = User.query.filter_by(email=admin_email).first()
        if existing:
            print("Admin user already exists.")
            return

        # Hash password
        hashed = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
        hashed = hashed.decode('utf-8')

        admin_user = User(
            username=admin_username,
            email=admin_email,
            password_hash=hashed,
            pi_wallet_address=wallet_address
        )

        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user '{admin_username}' created successfully.")

if __name__ == "__main__":
    seed_admin()
