from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Postgres-DB server URL
    SQLARCHEMY_DATABASE_URL_POSTGRES: str
    # JWT Secret-key
    JWT_SECRET_KEY: str
    # Redis server URL
    REDIS_URL: str
    # Email configuration
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = "no-reply@example.com"
    MAIL_PORT: int = 25
    MAIL_SERVER: str = "smtp4dev"
    MAIL_FROM_NAME: str = "Admin"
    MAIL_STARTTLS: bool = False
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = False
    # Celery configuration
    CELERY_BACKEND_URL: str
    CELERY_BROKER_URL: str
    # Sentry URL
    SENTRY_DSN: str
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
