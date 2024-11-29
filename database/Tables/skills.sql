CREATE TABLE skills (
    id SERIAL PRIMARY KEY,
    skill_name VARCHAR(100) NOT NULL,
    description TEXT,
    max_level INT DEFAULT 5, -- Maximum upgrade level
    base_cost DECIMAL(10, 2) NOT NULL, -- Cost for level 1
    xp_required INT NOT NULL, -- XP needed to unlock/upgrade
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO skills (id, skill_name, description, max_level, base_cost, xp_required)
VALUES
    (1, 'Sword Mastery', 'Increase damage with swords by 10%', 5, 50.0, 100),
    (2, 'Shield Defense', 'Increase block rate by 15%', 5, 75.0, 150);
SELECT * FROM skills;
import json
import mysql.connector

# Load JSON data
skills_json = [
    {
        "id": 1,
        "skill_name": "Sword Mastery",
        "description": "Increase damage with swords by 10%",
        "max_level": 5,
        "base_cost": 50.0,
        "xp_required": 100
    },
    {
        "id": 2,
        "skill_name": "Shield Defense",
        "description": "Increase block rate by 15%",
        "max_level": 5,
        "base_cost": 75.0,
        "xp_required": 150
    }
]

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="your_database"
)

cursor = connection.cursor()

# Create the table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS skills (
    id INT PRIMARY KEY,
    skill_name VARCHAR(100),
    description TEXT,
    max_level INT,
    base_cost DECIMAL(10, 2),
    xp_required INT
)
""")

# Insert data
for skill in skills_json:
    cursor.execute("""
    INSERT INTO skills (id, skill_name, description, max_level, base_cost, xp_required)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (skill['id'], skill['skill_name'], skill['description'], skill['max_level'], skill['base_cost'], skill['xp_required']))

# Commit and close
connection.commit()
cursor.close()
connection.close()
