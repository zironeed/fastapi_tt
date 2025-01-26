from pydantic import BaseModel, Field, EmailStr


class Recipient(BaseModel):
    """Recipient schema"""
    email: EmailStr | None = None
    tg_id: str | None = Field(None, max_length=150, pattern=r"^\d+$")


class Notification(BaseModel):
    """Notification schema"""
    message: str = Field(max_length=1024)
    delay: int = Field(ge=0, le=2, default=0)
    recipients: list[Recipient]
