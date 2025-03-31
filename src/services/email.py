from pathlib import Path
from typing import Dict, Any

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from src.conf.config import settings
from src.core.email_token import create_email_token

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS,
    TEMPLATE_FOLDER=Path(__file__).parent / "templates",
)


async def send_email(
    email: EmailStr,
    subject: str,
    body: Dict[str, Any],
    template_name: str = "verify_email.html"
) -> None:

    try:
        message = MessageSchema(
            subject=subject,
            recipients=[email],
            template_body=body,
            subtype=MessageType.html,
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name=template_name)
    except ConnectionErrors as err:
        print(err)


async def send_verification_email(email: EmailStr, username: str, host: str) -> None:

    token_verification = create_email_token({"sub": email})
    await send_email(
        email=email,
        subject="Confirm your email",
        body={
            "host": host,
            "username": username,
            "token": token_verification,
        },
        template_name="verify_email.html"
    )


async def send_password_reset_email(email: EmailStr, reset_url: str) -> None:
    await send_email(
        email=email,
        subject="Password Reset Request",
        body={"reset_url": reset_url},
        template_name="password_reset.html"
    )