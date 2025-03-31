from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import User
from src.repository.user_repository import UserRepository
from src.schemas.user import UserCreate
from src.services.auth import AuthService
from src.core.security import create_access_token, get_password_hash


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repository = UserRepository(self.db)
        self.auth_service = AuthService(db)

    async def create_user(self, user_data: UserCreate) -> User:
        user = await self.auth_service.register_user(user_data)
        return user

    async def get_user_by_username(self, username: str) -> User | None:
        user = await self.user_repository.get_by_username(username)
        return user

    async def get_user_by_email(self, email: str) -> User | None:
        user = await self.user_repository.get_user_by_email(email)
        return user

    async def confirmed_email(self, email: str) -> None:
        user = await self.user_repository.confirmed_email(email)
        return user

    async def update_avatar_url(self, email: str, url: str):
        return await self.user_repository.update_avatar_url(email, url)

    async def create_password_reset_token(self, email: str) -> Optional[str]:
        """
        Create a password reset token for the user
        """
        user = await self.get_user_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with this email not found"
            )

        # Create a token that expires in 1 hour
        token_data = {
            "sub": user.email,
            "type": "password_reset"
        }
        token = create_access_token(token_data, expires_delta=timedelta(hours=1))
        return token

    async def reset_password(self, email: str, new_password: str) -> User:
        """
        Reset user's password
        """
        user = await self.get_user_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        hashed_password = get_password_hash(new_password)
        return await self.user_repository.update_password(user, hashed_password)