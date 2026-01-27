from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="User Service")

# Simple in-memory store
fake_users = {
    "admin": "password123"
}

class User(BaseModel):
    username: str
    password: str

# Register endpoint
@app.post("/register")
def register(user: User):
    if user.username in fake_users:
        raise HTTPException(status_code=400, detail="User already exists")
    fake_users[user.username] = user.password
    return {"msg": "User registered successfully"}

# Login endpoint
@app.post("/login")
def login(user: User):
    if user.username not in fake_users or fake_users[user.username] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"username": user.username}
