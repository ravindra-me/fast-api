from fastapi import FastAPI, Depends
from app.routers import tasks
from sqlalchemy import text, select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Task

app = FastAPI(title="Tasks API")

# check the DB connection

@app.get("/db-check")
def check_db_connection(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "connected"}

@app.get('/get-tasks')
def get_all_tasks(db:Session = Depends(get_db)):
    tasks = db.scalars(select(Task)).all()
    return [{"id": t.id, "title": t.title, "done": t.done} for t in tasks]
    
app.include_router(tasks.router,prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}