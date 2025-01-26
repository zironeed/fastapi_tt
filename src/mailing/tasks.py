import asyncio
from celery import Celery
from src.config import settings
from src.mailing import schemas, services


app = Celery(
    __name__,
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    broker_connection_retry_on_startup=True,
    worker_max_tasks_per_child=25
)
notification_service = services.NotificationService()

@app.task
def send_notification(notification: schemas.Notification):
    """Send notification"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(
            notification_service.process_recipients(
                notification['recipients'],
                notification["message"],
            )
        )
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(
            notification_service.process_recipients(
                notification['recipients'],
                notification["message"],
            )
        )
    finally:
        loop.close()
