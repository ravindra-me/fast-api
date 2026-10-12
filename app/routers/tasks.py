from fastapi import APIRouter, HTTPException
from app.schema import TaskCreate, TaskOut, TaskListOut

router = APIRouter(prefix='/tasks', tags=["tasks"])

TASKS = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Setup VS Code", "done": True},
    {"id": 3, "title": "Learn SQL", "done": False},
]

@router.get('')
async def list_tasks(done: bool | None = None, search: str | None = None):
    result = TASKS
    if done is not None:
        result = [t for t in result if t['done'] == True]
    if search:
        result = [t for  t in result if search.lower() in t['title'].lower()]
    return result

@router.get("/{task_id}")
def get_task(task_id: int):
    for task in TASKS:
        if task["id"] == task_id:
            return task
    raise(HTTPException(status_code=404, detail="This Task is not found"))


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