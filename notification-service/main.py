from fastapi import FastAPI

app = FastAPI(title="Notification Service")

@app.get("/health")
def health():
    return {"status": "Notification Service is running"}

@app.post("/notify")
def notify(message: str):
    return {"notification": message}
