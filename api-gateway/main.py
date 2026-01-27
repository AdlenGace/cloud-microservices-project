from fastapi import FastAPI, HTTPException, Header
import requests
from security import create_access_token, verify_token

app = FastAPI(title="API Gateway")

USER_SERVICE_URL = "http://user-service:8001"
TASK_SERVICE_URL = "http://task-service:8002"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/login")
def login(username: str, password: str):
    response = requests.post(
        f"{USER_SERVICE_URL}/login",
        params={"username": username, "password": password}
    )

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Login failed")

    token = create_access_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}

def authenticate(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = authorization.split(" ")[1]
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload

@app.post("/tasks")
def create_task(title: str, user=authenticate):
    response = requests.post(
        f"{TASK_SERVICE_URL}/tasks",
        params={"title": title}
    )
    return response.json()
