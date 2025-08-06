from ..repositories.user import UserRepository, get_user_repository
from fastapi import Depends
from typing import Annotated, Optional
from ..schemas.user import UserLogin
from ..models.user import User
from ..core.security import verify_password
from ..core.logger import get_logger
from ..utils import exceptions

logger = get_logger(__name__)

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self.user_repository.get_user(username)
        if not user:
            logger.info("Login failed: User not found.")
            return False
        if not verify_password(plain_password=password, hashed_password=user.hashed_password):
            logger.info("Login failed: Incorrect password.")
            return False
        return user

    def login_for_access_token(self, login_data: UserLogin) -> Optional[User]:
        user = self.authenticate_user(login_data.username, login_data.password)
        if not user:
            raise exceptions.unauthorized("Incorrect username or password")
        logger.info("User authenticated! Ready to create token.")
        return user

def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
):
    return UserService(user_repository)