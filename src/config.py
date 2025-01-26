from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Redis
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"

    # Telegram
    tg_token: str

    # Email
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int = 587
    mail_server: str = "smtp.example.com"
    mail_starttls: bool = True
    mail_ssl_tls: bool = False
    use_credentials: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
