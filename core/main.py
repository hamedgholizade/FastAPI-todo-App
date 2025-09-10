from fastapi import (
    FastAPI,
)
from contextlib import asynccontextmanager

from tasks.routes import router as tasks_routes
from users.routes import router as users_routes


tags_metadata = [
    {
    "name": "tasks",
    "description": "Operations related to task management"
    }
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application starting up")
    yield
    print("Application shutting down")


app = FastAPI(
    title="Todo Application",
    description=(
        "A simple and efficient Todo management APIs built with FastAPI."
        "This APIs allow users to create, retrieve, update and delete tasks."
        "It is designed for task tracking and productivity improvment."
        ),
    version="1.0.0",
    contact={
        "name": "Hamed Gholizade",
        "email": "hamedabbasgholi33@gmail.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://mit-license.org/"
    },
    docs_url="/swagger",
    redoc_url="/redoc",
    lifespan=lifespan,
    openapi_tags=tags_metadata
    )

app.include_router(tasks_routes)
app.include_router(users_routes)
