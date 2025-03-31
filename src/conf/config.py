from pydantic_settings import BaseSettings
from pydantic import ConfigDict, EmailStr


class Settings(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://postgres:022709@localhost:5432/book_app"

    # jwt
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = "secret"
    # redis
    REDIS_URL: str = "redis://localhost"
    # mail
    MAIL_USERNAME: EmailStr = "zeleniak@meta.ua"
    MAIL_PASSWORD: str = "Swr123456789"
    MAIL_FROM: EmailStr = "zeleniak.nikita@meta.ua"
    MAIL_PORT: int = 465
    MAIL_SERVER: str = "smtp.meta.ua"
    MAIL_FROM_NAME: str = "Rest API Service"
    MAIL_STARTTLS: bool = False
    MAIL_SSL_TLS: bool = True
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    # cloudinary
    CLD_NAME: str = "dmp77sul8"
    CLD_API_KEY: int = 317848239297635
    CLD_API_SECRET: str = "IEu0098QqyjuG4godRQRgNdd3G0"

    model_config = ConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )


settings = Settings()
