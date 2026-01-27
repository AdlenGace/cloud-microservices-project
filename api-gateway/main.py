from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import requests
from security import create_access_token, verify_token

app = FastAPI(title="API Gateway")

# ---------------------------
# Internal service URLs
# ---------------------------
# Use the mapped container ports (host port mapping)
USER_SERVICE_URL = "http://user-service:8002"
TASK_SERVICE_URL = "http://task-service:8001"

# ---------------------------
# Request Models
# ---------------------------
class UserLogin(BaseModel):
    username: str
    password: str

class TaskCreate(BaseModel):
    title: str

# ---------------------------
# Healthcheck
# ---------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# ---------------------------
# Login Endpoint
# ---------------------------
@app.post("/login")
def login(user: UserLogin):
    response = requests.post(
        f"{USER_SERVICE_URL}/login",
        json={"username": user.username, "password": user.password}
    )

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Login failed")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

# ---------------------------
# Authentication dependency
# ---------------------------
def authenticate(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = authorization.split(" ")[1]
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload

# ---------------------------
# Task Creation Endpoint
# ---------------------------
@app.post("/tasks")
def create_task(task: TaskCreate, user=authenticate):
    response = requests.post(
        f"{TASK_SERVICE_URL}/tasks",
        json={"title": task.title}  # <--- send JSON, not params
    )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()
