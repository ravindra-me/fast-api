from fastapi import FastAPI
from app.routers import tasks

app = FastAPI(title="Tasks API")

app.include_router(tasks.router,prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}