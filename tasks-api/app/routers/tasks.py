import json
from pathlib import Path

from fastapi import APIRouter, HTTPException,Depends, Query
from app.schema import TaskCreate, TaskOut, TaskListOut

router = APIRouter(prefix='/tasks', tags=["tasks"])

DATA_FILE = Path(__file__).parent.parent / "data" / "tasks.json"
TASKS = json.loads(DATA_FILE.read_text())

def pagination(skip: int = 0, limit: int = Query(10, le=100)):
    return {"skip": skip, "limit": limit}

@router.get('')
async def list_tasks(done: bool | None = None, search: str | None = None, page:dict=Depends(pagination)):
    result = TASKS
    if done is not None:
        result = [t for t in result if t['done'] == True]
    if search:
        result = [t for  t in result if search.lower() in t['title'].lower()]
    start= page['skip']
    end = start + page['limit']
    return {"data":result[start:end], 'total':len(result)}

@router.get("/{task_id}")
def get_task(task_id: int):
    for task in TASKS:
        if task["id"] == task_id:
            return task
    raise(HTTPException(status_code=404, detail="This Task is not found"))

# create
@router.post('')
async def create_task(payload:TaskCreate):
    new_task = {
        "id": len(TASKS) + 1, **payload.model_dump()
    }
    TASKS.append(new_task)
    return new_task

# update task
@router.put('/{id}')
async def update_task(id: int, payload:TaskCreate):
    is_find=False
    for index, listItem in enumerate(TASKS):
        if listItem["id"] == id:
            TASKS[index] = {"id": id, **payload.model_dump()}
            return TASKS[index]
    raise(HTTPException(status_code=400, detail="Task not found"))