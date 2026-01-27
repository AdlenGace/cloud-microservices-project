from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Task Service")

tasks = []

# Model for request body
class TaskCreate(BaseModel):
    title: str

@app.get("/health")
def health():
    return {"status": "Task Service is running"}

@app.post("/tasks")
def create_task(task: TaskCreate):
    # Add simple task creation logic
    task_id = len(tasks) + 1
    task_data = {"id": task_id, "title": task.title}
    tasks.append(task_data)
    return task_data
