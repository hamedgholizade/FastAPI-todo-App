import time
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager

from tasks.routes import router as tasks_routes
from users.routes import router as users_routes


tags_metadata = [
    {"name": "tasks", "description": "Operations related to task management"}
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
        "email": "hamedabbasgholi33@gmail.com",
    },
    license_info={"name": "MIT", "url": "https://mit-license.org/"},
    docs_url="/swagger",
    redoc_url="/redoc",
    lifespan=lifespan,
    openapi_tags=tags_metadata,
)

app.include_router(tasks_routes)
app.include_router(users_routes)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# origins = [
#     "http://127.0.0.1:5500",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    error_response = {
        "error": True,
        "status_code": exc.status_code,
        "detail": str(exc.detail),
    }
    return JSONResponse(status_code=exc.status_code, content=error_response)


@app.exception_handler(RequestValidationError)
async def http_validation_exception_handler(request, exc):
    print(exc.__dict__)
    error_response = {
        "error": True,
        "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "detail": "There was a problem with your form request",
        "content": exc.errors(),
    }
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response
    )
