from fastapi import FastAPI

app = FastAPI(title="Task Service")

@app.get("/health")
def health():
    return {"status": "Task Service is running"}

@app.post("/tasks")
def create_task(title: str):
    return {"message": f"Task '{title}' created"}
