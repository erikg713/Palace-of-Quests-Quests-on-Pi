import random
from faker import Faker
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, DateTime, MetaData, ForeignKey, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Initialize Faker and database connection
faker = Faker()
engine = create_engine("mysql+pymysql://username:password@localhost/database_name")
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()

# Define tables
users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(100), nullable=False),
    Column('email', String(200), nullable=False),
    Column('password', String(100), nullable=False),
    Column('created_at', DateTime, default=datetime.utcnow),
)

level_rewards = Table(
    'level_rewards', metadata,
    Column('level_id', Integer, primary_key=True),
    Column('level_name', String(100), nullable=False),
    Column('reward_type', String(50), nullable=False),
    Column('reward_amount', Float, nullable=False),
    Column('created_at', DateTime, default=datetime.utcnow),
)

user_rewards = Table(
    'user_rewards', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('level_id', Integer, ForeignKey('level_rewards.level_id'), nullable=False),
    Column('claimed_at', DateTime, nullable=True),
)

# Create tables if they don't exist
metadata.create_all(engine)

# Seed users
def seed_users(num_users):
    user_data = [
        {
            'username': f"player{i}",
            'email': f"player{i}@example.com",
            'password': "password123",
            'created_at': faker.date_time_this_year()
        }
        for i in range(1, num_users + 1)
    ]
    session.execute(users.insert(), user_data)
    session.commit()
    print(f"Inserted {num_users} users.")

# Seed levels
def seed_levels(num_levels):
    level_data = [
        {
            'level_name': f"Level {i}",
            'reward_type': random.choice(['Coins', 'Item', 'Gems', 'Bonus']),
            'reward_amount': round(random.uniform(50, 500), 2),
            'created_at': faker.date_time_this_year()
        }
        for i in range(1, num_levels + 1)
    ]
    session.execute(level_rewards.insert(), level_data)
    session.commit()
    print(f"Inserted {num_levels} levels.")

# Seed user_rewards
def seed_user_rewards(user_ids, level_ids, claim_probability=0.7):
    reward_data = []
    for user_id in user_ids:
        for level_id in random.sample(level_ids, random.randint(1, len(level_ids))):
            reward_data.append({
                'user_id': user_id,
                'level_id': level_id,
                'claimed_at': faker.date_time_this_year() if random.random() < claim_probability else None
            })
    session.execute(user_rewards.insert(), reward_data)
    session.commit()
    print(f"Inserted {len(reward_data)} user rewards.")

# Execute seeding
def main():
    num_users = 1000
    num_levels = 500

    seed_users(num_users)
    seed_levels(num_levels)

    user_ids = [row.id for row in session.query(users.c.id).all()]
    level_ids = [row.level_id for row in session.query(level_rewards.c.level_id).all()]
    seed_user_rewards(user_ids, level_ids)

if __name__ == "__main__":
    main()
SELECT 
    u.username AS user_name,
    COUNT(ur.id) AS total_claimed_rewards,
    COALESCE(SUM(lr.reward_amount), 0) AS total_reward_value
FROM users u
LEFT JOIN user_rewards ur ON u.id = ur.user_id
LEFT JOIN level_rewards lr ON ur.level_id = lr.level_id
WHERE ur.claimed_at IS NOT NULL
GROUP BY u.id
ORDER BY total_claimed_rewards DESC;
SELECT 
    lr.level_name AS level_name,
    lr.reward_type AS reward_type,
    COUNT(ur.id) AS total_claims,
    COALESCE(SUM(lr.reward_amount), 0) AS total_reward_distributed
FROM level_rewards lr
LEFT JOIN user_rewards ur ON lr.level_id = ur.level_id
WHERE ur.claimed_at IS NOT NULL
GROUP BY lr.level_id
ORDER BY total_claims DESC;
SELECT 
    COUNT(ur.id) AS total_claims,
    COALESCE(SUM(lr.reward_amount), 0) AS total_rewards_distributed,
    AVG(lr.reward_amount) AS average_reward_value
FROM user_rewards ur
INNER JOIN level_rewards lr ON ur.level_id = lr.level_id
WHERE ur.claimed_at IS NOT NULL;
SELECT 
    u.username AS user_name,
    u.email AS user_email
FROM users u
LEFT JOIN user_rewards ur ON u.id = ur.user_id AND ur.claimed_at IS NOT NULL
WHERE ur.id IS NULL;
SELECT 
    lr.reward_type AS reward_type,
    COUNT(ur.id) AS total_claims,
    COALESCE(SUM(lr.reward_amount), 0) AS total_rewards
FROM level_rewards lr
LEFT JOIN user_rewards ur ON lr.level_id = ur.level_id
WHERE ur.claimed_at IS NOT NULL
GROUP BY lr.reward_type
ORDER BY total_rewards DESC;
SELECT 
    lr.level_name AS level_name,
    COUNT(ur.id) AS total_claims
FROM level_rewards lr
LEFT JOIN user_rewards ur ON lr.level_id = ur.level_id
WHERE ur.claimed_at IS NOT NULL
GROUP BY lr.level_id
ORDER BY total_claims DESC
LIMIT 5;
SELECT 
    AVG(total_rewards) AS avg_rewards_per_user,
    AVG(total_claimed) AS avg_claims_per_user
FROM (
    SELECT 
        u.id AS user_id,
        COALESCE(SUM(lr.reward_amount), 0) AS total_rewards,
        COUNT(ur.id) AS total_claimed
    FROM users u
    LEFT JOIN user_rewards ur ON u.id = ur.user_id
    LEFT JOIN level_rewards lr ON ur.level_id = lr.level_id
    WHERE ur.claimed_at IS NOT NULL
    GROUP BY u.id
) user_summary;
