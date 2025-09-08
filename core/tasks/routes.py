from fastapi import APIRouter

router = APIRouter(tags=["tasks"], prefix="/todo")


@router.get("/tasks")
async def retrieve_tasks_list():
    return []

@router.get("/tasks/{task_id}")
async def retrieve_tasks_detail(task_id: int):
    return [task_id]
