from fastapi import FastAPI, APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Palace of Quests - Quests on Pi",
    description="Optimized API for Palace of Quests metaverse game — Pi Network Ecosystem Web3 app.",
    version="1.0.0"
)

router = APIRouter()


# ----------------
# Models & Schemas
# ----------------

class PiUser(BaseModel):
    id: int
    pi_username: str
    pi_wallet: str
    level: int
    experience: int

class PiUserCreate(BaseModel):
    pi_username: str
    pi_wallet: str

class PiReward(BaseModel):
    id: int
    name: str
    value: int
    description: Optional[str] = None

class PiTransaction(BaseModel):
    id: int
    user_id: int
    amount: float
    tx_hash: str
    timestamp: str

class PiAuthRequest(BaseModel):
    pi_username: str
    pi_wallet: str

class PiAuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class PiLeaderboardEntry(BaseModel):
    pi_username: str
    level: int
    experience: int


# ----------------------
# Dummy Data for Example
# ----------------------

# In production, replace these with DB integrations
pi_users_db: List[PiUser] = []
pi_rewards_db: List[PiReward] = []
pi_transactions_db: List[PiTransaction] = []


# ------------------
# Pi Network Endpoints
# ------------------

@router.get("/", tags=["Root"])
def health_check():
    return {"message": "Palace of Quests Metaverse is live!"}


@router.post("/auth/login", response_model=PiAuthResponse, tags=["Auth"])
def pi_login(auth: PiAuthRequest):
    # Replace with real Pi Network authentication and JWT
    return PiAuthResponse(access_token="pi_demo_token")


@router.get("/users", response_model=List[PiUser], tags=["Users"])
def get_users():
    return pi_users_db

@router.post("/users", response_model=PiUser, status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(user: PiUserCreate):
    user_id = len(pi_users_db) + 1
    pi_user = PiUser(id=user_id, level=1, experience=0, **user.dict())
    pi_users_db.append(pi_user)
    return pi_user

@router.get("/users/{user_id}", response_model=PiUser, tags=["Users"])
def get_user(user_id: int):
    user = next((u for u in pi_users_db if u.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="Pi User not found")
    return user

@router.put("/users/{user_id}", response_model=PiUser, tags=["Users"])
def update_user(user_id: int, user: PiUserCreate):
    idx = next((i for i, u in enumerate(pi_users_db) if u.id == user_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Pi User not found")
    updated = pi_users_db[idx].copy(update=user.dict())
    pi_users_db[idx] = updated
    return updated


@router.get("/rewards", response_model=List[PiReward], tags=["Rewards"])
def get_rewards():
    return pi_rewards_db

@router.post("/rewards", response_model=PiReward, status_code=status.HTTP_201_CREATED, tags=["Rewards"])
def create_reward(reward: PiReward):
    reward_id = len(pi_rewards_db) + 1
    pi_reward = PiReward(id=reward_id, **reward.dict())
    pi_rewards_db.append(pi_reward)
    return pi_reward


@router.get("/transactions", response_model=List[PiTransaction], tags=["Transactions"])
def get_transactions():
    return pi_transactions_db

@router.post("/transactions", response_model=PiTransaction, status_code=status.HTTP_201_CREATED, tags=["Transactions"])
def create_transaction(tx: PiTransaction):
    tx_id = len(pi_transactions_db) + 1
    pi_tx = PiTransaction(id=tx_id, **tx.dict())
    pi_transactions_db.append(pi_tx)
    return pi_tx


@router.get("/leaderboard", response_model=List[PiLeaderboardEntry], tags=["Leaderboard"])
def leaderboard():
    data = sorted(pi_users_db, key=lambda u: (u.level, u.experience), reverse=True)
    return [PiLeaderboardEntry(pi_username=u.pi_username, level=u.level, experience=u.experience) for u in data]


# ------------------
# Error Handling
# ------------------

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


# ------------------
# Register Router
# ------------------

app.include_router(router, prefix="/api/pi")
