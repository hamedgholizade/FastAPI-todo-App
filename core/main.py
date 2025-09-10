from fastapi import (
    FastAPI,
)
from contextlib import asynccontextmanager

from tasks.routes import router as tasks_routes

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
    description="This is the section for description of todoapp",
    version="0.0.1",
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
