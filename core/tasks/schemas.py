from datetime import datetime
from typing import Optional
from pydantic import (
    BaseModel,
    Field
)


class TaskBaseSchema(BaseModel):
    title: str = Field(
        ...,
        max_length=150,
        min_length=5,
        description="Title of the task"
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Description of the task"
    )
    is_completed: bool = Field(
        ...,
        description="Status of the task"
    )
    

class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskUpdateSchema(TaskBaseSchema):
    pass


class TaskResponseSchema(TaskBaseSchema):
    id: int = Field(
        ...,
        description="Unique identifier of the object"
    )
    created_at: datetime = Field(
        ...,
        description="Record creation timestamp"
    )
    updated_at: datetime = Field(
        ...,
        description="Record updating timestamp"
    )
    