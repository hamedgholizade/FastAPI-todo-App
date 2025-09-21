from celery import Celery
import time
import datetime

from core.config import settings


celery_app = Celery("worker", backend=settings.CELERY_BACKEND_URL, broker=settings.CELERY_BROKER_URL)
celery_app.conf.update(
    broker_connection_retry_on_startup=True,
    timezone="UTC",
    beat_schedule={
        "print-hello-every-minute": {
            "task": "core.celery_conf.print_hello",
            "schedule": 60,  # every minute
        },
    },
)


@celery_app.task
def add_number(x, y):
    time.sleep(20)
    return x + y


@celery_app.task
def print_hello():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Hello! Current time: {now}")
