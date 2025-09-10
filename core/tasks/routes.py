from typing import List
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import (
    APIRouter,
    Path,
    status,
    HTTPException,
    Depends
)

from core.database import get_db
from tasks.models import TaskModel
from tasks.schemas import (
    TaskCreateSchema,
    TaskUpdateSchema,
    TaskResponseSchema
)


router = APIRouter(tags=["tasks"], prefix="/todo")

@router.get(
    "/tasks",
    status_code=status.HTTP_200_OK,
    response_model=List[TaskResponseSchema]
)
async def retrieve_tasks_list(db: Session = Depends(get_db)):
    result = db.query(TaskModel).all()
    return result


@router.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskResponseSchema
)
async def create_task(
    request: TaskCreateSchema,
    db: Session = Depends(get_db)
    ):
    task_obj = TaskModel(**request.model_dump())
    db.add(task_obj)
    db.commit()
    db.refresh(task_obj)
    return task_obj


@router.get(
    "/tasks/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=TaskResponseSchema
)
async def retrieve_tasks_detail(
    task_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
    ):
    task_obj = db.query(TaskModel).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(
            detail="Task not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return task_obj


@router.put(
    "/tasks/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=TaskResponseSchema
)
async def update_tasks_detail(
    request: TaskUpdateSchema,
    task_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
    ):
    task_obj = db.query(TaskModel).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(
            detail="Task not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    for field, value in request.model_dump().items():
        setattr(task_obj, field, value)
    db.commit()
    db.refresh(task_obj)
    return task_obj


@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_tasks_detail(
    task_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
    ):
    task_obj = db.query(TaskModel).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(
            detail="Task not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    db.delete(task_obj)
    db.commit()
