from app.core.config import settings

TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "app.models.user",
                "app.models.package",
                "app.models.original_package_history",
                "app.models.process_task",
                "app.models.operation_log",
                "app.models.scheduled_task",
                "aerich.models",
            ],
            "default_connection": "default",
        }
    },
}
