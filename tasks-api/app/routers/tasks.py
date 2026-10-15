import json
from pathlib import Path
from fastapi import APIRouter, HTTPException,Depends, Query
from app.schema import TaskCreate, TaskOut, TaskListOut

# databse import
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Task

router = APIRouter(prefix='/tasks', tags=["tasks"])

DATA_FILE = Path(__file__).parent.parent / "data" / "tasks.json"
TASKS = json.loads(DATA_FILE.read_text())

def pagination(skip: int = 0, limit: int = Query(10, le=100)):
    return {"skip": skip, "limit": limit}

@router.get('', response_model=TaskListOut)
def list_tasks(done: bool | None = None, search: str | None = None, page:dict=Depends(pagination), db:Session=Depends(get_db)):
    result = select(Task)
    if done is not None:
        # result = [t for t in result if t['done'] == True]
        result = result.where(Task.done == done)
    if search:
        # result = [t for  t in result if search.lower() in t['title'].lower()]
        result = result.where(Task.title.ilike(f"%{search}%"))
    tasks = db.scalars(result.order_by(Task.created_at.desc()).limit(page['limit']).offset(page['skip'])).all()
    total = db.scalar(select(func.count()).select_from(result.subquery()))
    return {"data":tasks, 'total':total}

@router.get("/{id}", response_model=TaskOut)
def get_task(id: int, db:Session=Depends(get_db)):
    task = db.get(Task, id)
    if task is None:
         raise(HTTPException(status_code=404, detail="This Task is not found"))
    return task
   
# create
@router.post('', response_model=TaskOut, status_code=201)
async def create_task(payload:TaskCreate, db:Session = Depends(get_db)):
    new_task = Task(**payload.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# update task
@router.put('/{id}', response_model=TaskOut, status_code=200)
def update_task(id: int, payload:TaskCreate, db:Session=Depends(get_db)):
    task = db.get(Task, id)
    if task is None:
        raise(HTTPException(status_code=400, detail="Task not found"))
    task.title = payload.title
    task.done = payload.done
    db.commit()
    db.refresh(task)
    return task

# delete task

@router.delete('/{id}', status_code=204)
def delete_task(id:int, db:Session = Depends(get_db)):
    task = db.get(Task, id)
    if task is None:
        raise(HTTPException(status_code=400, detail="Task not found"))
    db.delete(task)
    db.commit()
    
    

    
