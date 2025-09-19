import time
import httpx
import random
from fastapi import FastAPI, Request, status, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from tasks.routes import router as tasks_routes
from users.routes import router as users_routes
from core.config import settings


# Advanced Python Scheduler


scheduler = AsyncIOScheduler()


def my_task():
    print(f"Task executed at {time.strftime('%Y-%m-%d %H:%M:%S')}")


tags_metadata = [
    {"name": "tasks", "description": "Operations related to task management"}
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application starting up")

    # Scheduler
    scheduler.add_job(my_task, IntervalTrigger(seconds=10))
    scheduler.start()

    # Redis cache init
    redis = aioredis.from_url(
        settings.REDIS_URL,
        encoding="utf8",
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    print("✅ Redis cache initialized")

    yield

    scheduler.shutdown()
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
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=error_response
    )


# background task handling


def start_task(task_id):
    print(f"doing the process: {task_id}")
    time.sleep(task_id)
    print(f"finished task {task_id}")


@app.get("/initiate-task", status_code=200)
async def initiate_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(start_task, task_id=random.randint(5, 15))
    return JSONResponse(content={"detail": "task is done"})

# caching example

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

# Set up the cache backend
redis = aioredis.from_url(settings.REDIS_URL)
cache_backend = RedisBackend(redis)
FastAPICache.init(cache_backend, prefix="fastapi-cache")

async def request_current_weather(latitude: float, longitude: float):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        current_weather = data.get("current", {})
        return current_weather
    else:
        return None
    

@app.get("/fetch-current-weather", status_code=200)
@cache(expire=10)
async def fetch_current_weather(latitude: float = 40.7128, longitude: float = -74.0060):
    current_weather = await request_current_weather(latitude, longitude)
    if current_weather:

        return JSONResponse(content={"current_weather": current_weather})
    else:
        return JSONResponse(content={"detail": "Failed to fetch weather"}, status_code=500)
    