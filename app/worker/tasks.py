from app.core.celery import celery_app
from celery.utils.log import get_task_logger
from app.services.process_service import process_service
from app.services.storage_service import storage_service
from app.models.package import Package
from app.models.scheduled_task import ScheduledTask
from tortoise import Tortoise
from app.core.config import settings
import asyncio
import os
import shutil
from datetime import datetime, timedelta, timezone

logger = get_task_logger(__name__)


@celery_app.task
def test_task(word: str):
    logger.info(f"Test task received: {word}")
    return f"test task return {word}"


async def init_db():
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={
            "models": [
                "app.models.user",
                "app.models.package",
                "app.models.original_package_history",
                "app.models.process_task",
                "app.models.operation_log",
                "app.models.scheduled_task",
                "aerich.models",
            ]
        },
    )


async def run_process_package(package_id: int, file_path: str = None):
    await init_db()

    temp_download_path = None
    try:
        package = await Package.get_or_none(id=package_id)
        if not package:
            logger.error(f"Package {package_id} not found")
            return

        # If file_path is None or not exists, try to download from R2
        if not file_path or not os.path.exists(file_path):
            if package.r2_original_path:
                logger.info(
                    f"File not found locally. Downloading from R2: {package.r2_original_path}"
                )
                # Create temp path
                temp_dir = os.path.join(os.getcwd(), "temp_downloads", str(package_id))
                os.makedirs(temp_dir, exist_ok=True)
                # Extract filename from R2 key
                filename = os.path.basename(package.r2_original_path)
                temp_download_path = os.path.join(temp_dir, filename)

                try:
                    storage_service.download_file(
                        package.r2_original_path, temp_download_path
                    )
                    file_path = temp_download_path
                except Exception as e:
                    logger.error(f"Failed to download file from R2: {e}")
                    # Cannot proceed
                    package.status = "processed_failed"
                    await package.save()
                    return
            else:
                logger.error(f"No file path and no R2 path for package {package_id}")
                package.status = "processed_failed"
                await package.save()
                return

        package.status = "processing"
        await package.save()

        try:
            output_path = await process_service.process_package(package_id, file_path)

            # Upload to R2
            filename = os.path.basename(output_path)
            object_name = f"{package_id}/processed/{filename}"
            logger.info(f"Uploading processed file to R2: {object_name}")
            public_url = storage_service.upload_file(output_path, object_name)

            package.status = "processed_success"
            package.r2_processed_path = object_name
            package.download_url = public_url
            package.is_distributing = True  # Auto-enable distribution after success
            await package.save()
            logger.info(
                f"Package {package_id} processed successfully. Download URL: {public_url}"
            )

        except Exception as e:
            logger.error(f"Processing failed for package {package_id}: {e}")
            package.status = "processed_failed"
            await package.save()

    finally:
        # Cleanup temp file if we downloaded it
        if temp_download_path and os.path.exists(temp_download_path):
            try:
                shutil.rmtree(os.path.dirname(temp_download_path))
            except Exception as e:
                logger.error(f"Failed to cleanup temp file: {e}")

        await Tortoise.close_connections()


@celery_app.task
def process_package_task(package_id: int, file_path: str = None):
    logger.info(f"Processing package {package_id}, path {file_path}")
    try:
        asyncio.run(run_process_package(package_id, file_path))
    except Exception as e:
        logger.error(f"Unexpected error in task: {e}")
        raise e
    return "Processing completed"


async def run_check_scheduled_tasks():
    await init_db()
    try:
        now = datetime.now(timezone.utc)
        # Find active tasks that are due
        tasks = await ScheduledTask.filter(is_active=True, next_run_at__lte=now).all()

        logger.info(f"Found {len(tasks)} scheduled tasks to run")

        for task in tasks:
            logger.info(f"Triggering scheduled task for package {task.package_id}")
            # Trigger processing task
            process_package_task.delay(task.package_id, None)

            # Update task schedule
            task.last_run_at = now
            task.next_run_at = now + timedelta(seconds=task.interval_seconds)
            await task.save()

    except Exception as e:
        logger.error(f"Error checking scheduled tasks: {e}")
    finally:
        await Tortoise.close_connections()


@celery_app.task
def check_scheduled_tasks():
    """
    Periodic task to check and trigger scheduled package processing
    """
    asyncio.run(run_check_scheduled_tasks())
