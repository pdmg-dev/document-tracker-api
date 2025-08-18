# app/services/auth_service.py

from datetime import timedelta
from typing import Optional

from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import settings
from app.core.logger import get_logger
from app.core.security import verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.token import Token
from app.services.token_service import TokenService
from app.utils import exceptions

logger = get_logger(__name__)


class AuthService:
    def __init__(self, user_repository: UserRepository, token_service: TokenService):
        self.user_repository = user_repository
        self.token_service = token_service

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = await self.user_repository.get_user(username)
        if not user:
            logger.warning(f"Authentication failed: User '{username}' not found.")
            return None

        if not verify_password(password, user.hashed_password):
            logger.warning(f"Authentication failed: Incorrect password for user '{username}'.")
            return None

        logger.debug(f"Authentication success: User '{username}' verified.")
        return user

    async def login_for_access_token(self, form_data: OAuth2PasswordRequestForm) -> Token:
        user = await self.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise exceptions.unauthorized("Incorrect username or password")

        access_token = self.token_service.create_access_token(
            data={"sub": user.username},
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
        )

        logger.info(f"Access token issued for user '{user.username}'")
        return Token(access_token=access_token, token_type="bearer")
