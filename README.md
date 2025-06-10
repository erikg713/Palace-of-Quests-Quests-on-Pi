```markdown
# Palace of Quests - Quests-for-Pi

**Palace of Quests (Pi Quest)** is a Web3-powered metaverse game built on the Pi Network. This engaging platform offers players the chance to explore, level up, and earn rewards in an immersive virtual world.

## 🚀 Features

- **Metaverse Gameplay**: Engage in a dynamic world with levels ranging from 1 to 250.
- **Rewards and Experience**: Gain in-game rewards and experience points to unlock avatar upgrades.
- **Premium Subscription**: Enjoy all unlocked upgrades with a $9.99/year subscription.
- **Blockchain Integration**: Secure peer-to-peer payments using the Pi Network SDK.
- **Cross-Chain Compatibility**: Planned integration with Ethereum and Tide networks for cross-chain bridging.
- **Database**: Powered by PostgreSQL for reliable data storage and management.
- **Clean Codebase**: Secure, structured backend and frontend for scalability and maintainability.

## 🛠️ Tech Stack

### Dependencies
- **Backend**
pip install flask flask-cors flask-sqlalchemy requests
- **Frontend**
npm install @pi-network/pi-sdk axios

### Frontend
- **React**: Interactive and scalable user interfaces.
- **React Native** *(Future Plan)*: Mobile-first design for cross-platform support.
- **Three.js / Babylon.js**: Rendering the game world and character interactions.
- **Web3.js / Pi Network SDK**: Handling blockchain transactions.
- **Redux / Zustand**: State management for inventory, quests, and economy.

### Backend
- **Flask**: Lightweight and secure backend framework.
- **Node.js**: Real-time functions and APIs.
- **PostgreSQL**: Database for storing user progress, game data, and transactions.
- **WebSockets**: For real-time interactions in quests, battles, or trades.
- **IPFS / Decentralized Storage**: Storing in-game assets securely.
- **Docker**: Containerization for consistent environments.

## 📖 How It Works

1. **Create an Account**: Sign up using your Pi Network credentials.
2. **Start Your Quest**: Begin at level 1 and complete challenges to gain rewards.
3. **Upgrade Your Avatar**: Use earned rewards to enhance your avatar's capabilities.
4. **Go Premium**: Unlock all upgrades with a $9.99 yearly subscription.
5. **Transact Securely**: Utilize the Pi Network SDK for safe, peer-to-peer payments.

## 📂 Project Structure

```plaintext
backend/
│── flask_app/             # Flask backend for structured logic
│   ├── routes/            # API endpoints
│   │   ├── auth.py        # Pi Network authentication
│   │   ├── quests.py      # Quest system API
│   │   ├── marketplace.py # Marketplace API (buy/sell/trade)
│   │   ├── economy.py     # Pi transactions and balance tracking
│   │   ├── users.py       # Player profiles & inventory
│   ├── services/          # Core game logic & processing
│   ├── models.py          # Database models (PostgreSQL)
│   ├── config.py          # App settings & security configs
│   ├── __init__.py        # Flask app initialization
│── node_server/           # Node.js for real-time interactions
│   ├── index.js           # WebSockets for real-time trading and updates
│── database/              # PostgreSQL database setup
│   ├── migrations/        # DB migrations
│   ├── schema.sql         # Database schema
│── .env                   # Environment variables (secure keys, API URLs)
│── Dockerfile             # Containerized deployment
│── requirements.txt       # Flask dependencies
│── package.json           # Node.js dependencies

palace-of-quests/
├── backend/
│   ├── app/
│   │   ├── __init__.py                 # Initializes Flask app and extensions
│   │   ├── config.py                   # Configuration settings (e.g., database URI)
│   │   ├── extensions.py               # Defines Flask extensions (e.g., SQLAlchemy, JWT)
│   │   ├── models/                     # Database models
│   │   │   ├── __init__.py             # Imports all models
│   │   │   ├── user.py                 # User model with enhancements
│   │   │   ├── quest.py                # Quest model
│   │   │   ├── quest_progress.py       # QuestProgress model
│   │   │   ├── user_quest.py           # UserQuest model
│   │   │   ├── item.py                 # Item model for marketplace
│   │   │   └── transaction.py          # Transaction model
│   │   ├── api/                        # API blueprints for endpoints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py                 # Authentication endpoints (register, login)
│   │   │   ├── users.py                # User-related endpoints
│   │   │   ├── quests.py               # Quest-related endpoints
│   │   │   ├── marketplace.py          # Marketplace endpoints
│   │   │   └── transactions.py         # Transaction endpoints
│   │   ├── utils/                      # Utility functions
│   │   │   ├── __init__.py
│   │   │   ├── validation.py           # Input validation helpers
│   │   │   ├── serialization.py        # Serialization for API responses
│   │   │   └── errors.py               # Custom error handlers
│   │   └── templates/                  # Optional: Templates for emails or admin UI
│   ├── migrations/                     # Database migrations (via Flask-Migrate)
│   │   ├── env.py
│   │   └── versions/
│   ├── tests/                         # Unit and integration tests
│   │   ├── __init__.py
│   │   ├── test_auth.py
│   │   ├── test_users.py
│   │   ├── test_quests.py
│   │   ├── test_marketplace.py
│   │   └── test_transactions.py
│   ├── .env                           # Environment variables (e.g., SECRET_KEY)
│   ├── requirements.txt               # Python dependencies
│   ├── run.py                         # Entry point to run the Flask app
│   ├── Dockerfile                     # Docker configuration (optional)
│   └── docker-compose.yml             # Docker Compose for local development (optional)
```

## 🚀 API Endpoints Breakdown

| Feature       | Endpoint               | Method | Description                         |
|---------------|------------------------|--------|-------------------------------------|
| Auth          | `/auth/login`          | POST   | Logs in with Pi Network             |
|               | `/auth/register`       | POST   | Registers a new player              |
| Quests        | `/quests`              | GET    | Fetch all available quests          |
|               | `/quests/start`        | POST   | Start a new quest                   |
|               | `/quests/progress`     | POST   | Update quest progress               |
| Marketplace   | `/marketplace/list`    | POST   | List an item for sale               |
|               | `/marketplace/buy`     | POST   | Buy an item from a player           |
|               | `/marketplace/trade`   | POST   | Secure trade via escrow             |
| Economy       | `/economy/balance`     | GET    | Fetch player's Pi balance           |
|               | `/economy/earnings`    | GET    | Track game revenue                  |
| Users         | `/users/inventory`     | GET    | Fetch user inventory                |

## 📦 Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 15+
- Docker (optional)

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/palace-of-quests.git
   ```

2. Navigate to the backend directory:
   ```bash
   cd palace-of-quests/backend
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the development server:
   ```bash
   flask run
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd palace-of-quests/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the React app:
   ```bash
   npm start
   ```

### Using Docker

1. Build the Docker image:
   ```bash
   docker-compose build
   ```

2. Run the application:
   ```bash
   docker-compose up
   ```

   flask db migrate -m "Add role to User model"
flask db upgrade
pip install flask-limiter

## 📅 Roadmap

- [ ] Launch MVP with Pi Network payment integration.
- [ ] Expand levels and features in the metaverse.
- [ ] Add React Native for mobile platforms.
- [ ] Integrate cross-chain functionality with Ethereum.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a Pull Request.

## 🛡️ License

This project is licensed under the Pi Network License. See the LICENSE file for details.

## 📧 Contact

For questions or support, please email: dev713@protonmail.com

## 🧪 Tests

### Test Cases

#### Registration Success
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "player1", "pi_wallet": "pi_wallet_123"}'
```
**Expected Response:**
```json
{"message": "User registered successfully", "user_id": "<generated_id>"}
```

#### Registration Missing Fields
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "player1"}'
```
**Expected Response:**
```json
{"error": "Missing required fields: username and pi_wallet"}
```

#### Login Success (After registration, use the same pi_wallet to log in)
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"pi_wallet": "pi_wallet_123"}'
```
**Expected Response:**
```json
{"message": "Login successful", "token": "<JWT token>"}
```

#### Login Missing Field
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{}'
```
**Expected Response:**
```json
{"error": "Missing required field: pi_wallet"}
```

#### Login User Not Found
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"pi_wallet": "non_existent_wallet"}'
```
**Expected Response:**
```json
{"error": "User not found"}
```

#### Start a User Quest
```bash
curl -X POST http://localhost:5000/user_quests/start \
  -H "Content-Type: application/json" \
  -d '{"user_id": "some-user-id", "quest_id": 1}'
```
**Expected Response**
```json
{"message": "User quest started", "user_quest_id": <generated_id>}
```

#### Update Quest Progress
```bash
curl -X POST http://localhost:5000/user_quests/update \
  -H "Content-Type: application/json" \
  -d '{"user_quest_id": 1, "progress": 50}'
```
**Expected Response**
```json
{"message": "User quest progress updated", "user_quest_id": 1}
```

#### Mark Quest as Completed
```bash
curl -X POST http://localhost:5000/user_quests/update \
  -H "Content-Type: application/json" \
  -d '{"user_quest_id": 1, "progress": 100}'
```
**Expected Response:**
```json
{"message": "User quest progress updated", "user_quest_id": 1}
```

Retrieve All User Quests
```bash
curl -X GET "http://localhost:5000/user_quests/?user_id=some-user-id"
```
**Expected Response:**
```json
{
  "user_id": "some-user-id",
  "quests": [
    {
      "user_quest_id": 1,
      "quest_id": 1,
      "progress": 100,
      "status": "completed",
      "started_at": "2025-03-21T12:34:56.789123",
      "completed_at": "2025-03-21T12:45:00.123456"
    },
    ...
  ]
}
```

#### Create a new Quest
```bash
curl -X POST http://localhost:5000/admin/quest/create \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Defeat the Goblin King",
    "description": "Venture into the dark forest and defeat the Goblin King.",
    "reward": 75,
    "level_required": 3
  }'
```
**Expected Response:**
```json
{
  "message": "Quest created successfully",
  "quest_id": <newly_generated_quest_id>
}
```

Update an Existing Quest
```bash
curl -X PUT http://localhost:5000/admin/quest/update \
  -H "Content-Type: application/json" \
  -d '{
    "quest_id": 1,
    "title": "Defeat the Mighty Goblin King",
    "reward": 80
  }'
```
**Expected Response:**
```json
{
  "message": "Quest updated successfully",
  "quest_id": 1
}
```

Delete a Quest
```bash
curl -X DELETE http://localhost:5000/admin/quest/delete \
  -H "Content-Type: application/json" \
  -d '{"quest_id": 1}'
```
**Expected Response:**
```json
{
  "message": "Quest deleted successfully",
  "quest_id": 1
}
```
