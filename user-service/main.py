from fastapi import FastAPI, HTTPException

app = FastAPI(title="User Service")

fake_users = {
    "admin": "password123"
}

@app.post("/login")
def login(username: str, password: str):
    if username not in fake_users or fake_users[username] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"username": username}
