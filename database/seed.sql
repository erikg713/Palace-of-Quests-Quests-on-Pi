import os
import random
from faker import Faker
from sqlalchemy import (
    create_engine, Table, Column, Integer, String, Float, DateTime, MetaData, ForeignKey
)
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# --- Configuration ---
DB_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:pass@localhost/dbname")

# --- Initialization ---
faker = Faker()
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()

# --- Table Definitions ---
users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(100), nullable=False, unique=True),
    Column('email', String(200), nullable=False, unique=True),
    Column('password', String(100), nullable=False),
    Column('created_at', DateTime, default=datetime.utcnow)
)

level_rewards = Table(
    'level_rewards', metadata,
    Column('level_id', Integer, primary_key=True),
    Column('level_name', String(100), nullable=False, unique=True),
    Column('reward_type', String(50), nullable=False),
    Column('reward_amount', Float, nullable=False),
    Column('created_at', DateTime, default=datetime.utcnow)
)

user_rewards = Table(
    'user_rewards', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('level_id', Integer, ForeignKey('level_rewards.level_id'), nullable=False),
    Column('claimed_at', DateTime, nullable=True)
)

# --- Create Tables ---
metadata.create_all(engine)

# --- Seeding Functions ---
def seed_users(n):
    users_list = [
        {
            "username": f"player{i}",
            "email": f"player{i}@example.com",
            "password": "password123",
            "created_at": faker.date_time_this_year()
        }
        for i in range(1, n + 1)
    ]
    session.execute(users.insert(), users_list)
    session.commit()
    print(f"Created {n} users.")

def seed_levels(n):
    reward_types = ['Coins', 'Item', 'Gems', 'Bonus']
    levels_list = [
        {
            "level_name": f"Level {i}",
            "reward_type": random.choice(reward_types),
            "reward_amount": round(random.uniform(50, 500), 2),
            "created_at": faker.date_time_this_year()
        }
        for i in range(1, n + 1)
    ]
    session.execute(level_rewards.insert(), levels_list)
    session.commit()
    print(f"Created {n} levels.")

def seed_user_rewards(user_ids, level_ids, claim_chance=0.7):
    rewards = []
    for user_id in user_ids:
        for level_id in random.sample(level_ids, random.randint(1, len(level_ids))):
            rewards.append({
                "user_id": user_id,
                "level_id": level_id,
                "claimed_at": faker.date_time_this_year() if random.random() < claim_chance else None
            })
    session.execute(user_rewards.insert(), rewards)
    session.commit()
    print(f"Assigned {len(rewards)} rewards.")

# --- Main Execution ---
def main():
    try:
        NUM_USERS = 1000
        NUM_LEVELS = 500

        seed_users(NUM_USERS)
        seed_levels(NUM_LEVELS)

        user_ids = [row[0] for row in session.query(users.c.id).all()]
        level_ids = [row[0] for row in session.query(level_rewards.c.level_id).all()]

        seed_user_rewards(user_ids, level_ids)

        print("Seeding completed successfully.")

    except Exception as exc:
        print(f"[ERROR] Seeding failed: {exc}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    main()
