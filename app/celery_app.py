from celery.result import AsyncResult
from celery import Celery
from dotenv import dotenv_values

config = dotenv_values(".env")

celery_app = Celery(
    "tasks",
    backend=config["celery_backend"],
    broker=config["celery_broker"],
    include=["app.celery_tasks"],
)


def is_celery_started() -> bool:
    inspector = celery_app.control.inspect()
    active_workers = inspector.active()
    return active_workers is not None


def task_result(task_id: str) -> AsyncResult:
    return AsyncResult(task_id, app=celery_app)


if __name__ == "__main__":
    celery_app.start()
