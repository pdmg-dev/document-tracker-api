# app/services/auth.py

from datetime import timedelta
from typing import Annotated, Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..core.logger import get_logger
from ..core.security import verify_password
from ..core.settings import settings
from ..models.user import User
from ..repositories.user import UserRepository, get_user_repository
from ..schemas.token import Token
from ..services.token import TokenService, get_token_service
from ..utils import exceptions

logger = get_logger(__name__)

UserRepoDependency = Annotated[UserRepository, Depends(get_user_repository)]
TokenServiceDependency = Annotated[TokenService, Depends(get_token_service)]


class AuthService:
    def __init__(
        self,
        user_repository: UserRepoDependency,
        token_service: TokenServiceDependency,
    ):
        self.user_repository = user_repository
        self.token_service = token_service

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self.user_repository.get_user(username)
        if not user:
            logger.warning(f"Login failed: User '{username}' not found.")
            return None

        if not verify_password(password, user.hashed_password):
            logger.warning(f"Login failed: Incorrect password for user '{username}'.")
            return None

        logger.debug(f"Login success: User '{username}' authenticated.")
        return user

    def login_for_access_token(self, form_data: OAuth2PasswordRequestForm) -> Token:
        user = self.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise exceptions.unauthorized("Incorrect username or password")

        access_token = self.token_service.create_access_token(
            data={"sub": user.username},
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
        )

        logger.info(f"Access token issued for user '{user.username}'")
        return Token(access_token=access_token, token_type="bearer")


# Dependency injector
def get_auth_service(
    user_repository: UserRepoDependency,
    token_service: TokenServiceDependency,
) -> AuthService:
    return AuthService(user_repository, token_service)
