from fastapi import APIRouter
from src.mailing import schemas, tasks

router = APIRouter(prefix="/api", tags=["mailing"])

@router.post("/notify")
async def notify(notification: schemas.Notification):
    """Create notification"""
    countdown = [0, 3600, 86400][notification.delay]
    tasks.send_notification.apply_async(args=[notification.dict()], countdown=countdown)
