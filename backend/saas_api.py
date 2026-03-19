# SaaS API (FastAPI) - Auth + Users + Plans
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

app = FastAPI()

# ===== MOCK DB =====
USERS = {}

class User(BaseModel):
    username: str
    password: str

# ===== AUTH =====
@app.post("/register")
def register(user: User):
    if user.username in USERS:
        raise HTTPException(400, "User exists")
    USERS[user.username] = {"password": user.password, "plan": "free"}
    return {"status": "created"}

@app.post("/login")
def login(user: User):
    if user.username not in USERS:
        raise HTTPException(404, "Not found")
    if USERS[user.username]["password"] != user.password:
        raise HTTPException(401, "Invalid")
    return {"status": "ok", "user": user.username}

# ===== PLANOS =====
@app.get("/plan/{username}")
def get_plan(username: str):
    return {"plan": USERS.get(username, {}).get("plan", "free")}

@app.post("/upgrade/{username}")
def upgrade(username: str):
    if username not in USERS:
        raise HTTPException(404, "Not found")
    USERS[username]["plan"] = "pro"
    return {"status": "upgraded"}
