from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.worker.tasks"]
)

# Configure Redis connection options to handle timeouts better
celery_app.conf.broker_transport_options = {
    "socket_timeout": 30,
    "socket_connect_timeout": 30,
    "socket_keepalive": True,
}

celery_app.conf.result_backend_transport_options = {
    "socket_timeout": 30,
    "socket_connect_timeout": 30,
    "socket_keepalive": True,
}

celery_app.conf.broker_connection_retry_on_startup = True

# celery_app.conf.task_routes = {
#     "app.worker.tasks.*": {"queue": "main-queue"},
# }

celery_app.conf.beat_schedule = {
    "check-scheduled-tasks-every-minute": {
        "task": "app.worker.tasks.check_scheduled_tasks",
        "schedule": 60.0,
    },
}
