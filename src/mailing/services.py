import asyncio
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from telegram import Bot
from src.config import settings
from src.mailing.schemas import Recipient


class NotificationService:
    """Service for sending notifications"""
    def __init__(self):
        self.telegram_bot = Bot(token=settings.tg_token)
        self.fast_mail = FastMail(
            ConnectionConfig(
                MAIL_USERNAME=settings.mail_username,
                MAIL_PASSWORD=settings.mail_password,
                MAIL_FROM=settings.mail_from,
                MAIL_PORT=settings.mail_port,
                MAIL_SERVER=settings.mail_server,
                MAIL_STARTTLS=settings.mail_starttls,
                MAIL_SSL_TLS=settings.mail_ssl_tls,
                USE_CREDENTIALS=settings.use_credentials
            )
        )

    async def send_tg(self, tg_id: str, message: str):
        await self.telegram_bot.send_message(chat_id=tg_id, text=message)

    async def send_email(self, email: str, message: str):
        email_message = MessageSchema(
            subject="Notification",
            recipients=[email],
            body=message,
            subtype="plain"
        )
        await self.fast_mail.send_message(email_message)

    async def process_recipients(self, recipients: list[Recipient], message: str):
        await asyncio.gather(*[
            self.send_tg(tg_id=recipient['tg_id'], message=message)
            if recipient.get('tg_id') else self.send_email(email=recipient['email'], message=message)
            for recipient in recipients
        ])
