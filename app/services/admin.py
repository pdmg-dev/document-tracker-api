# app/services/admin.py

from typing import Annotated, List, Optional

from fastapi import Depends

from ..core.logger import get_logger
from ..core.security import hash_password
from ..models.user import User
from ..repositories.user import UserRepository, get_user_repository
from ..schemas.user import UserCreate, UserRead
from ..utils import exceptions

logger = get_logger(__name__)


class AdminService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, create_data: UserCreate) -> Optional[User]:
        exsiting_user = self.user_repository.get_user(create_data.username)
        if exsiting_user:
            logger.info(f"User already exists! (username: '{exsiting_user.username}')")
            raise exceptions.bad_request("User already exists")

        hashed_password = hash_password(create_data.password)
        new_user = User(
            **create_data.model_dump(exclude="password"),
            hashed_password=hashed_password,
        )
        created_user = self.user_repository.create(new_user)
        logger.info(f"New user created! (username: '{new_user.username}')")
        return UserRead.model_validate(created_user)

    def get_all_users(self) -> List[UserRead]:
        users = self.user_repository.get_all()
        if not users:
            logger.info("Users table empty!")
            raise exceptions.bad_request("No active users")
        return [UserRead.model_validate(user) for user in users]


def get_admin_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
):
    return AdminService(user_repository)
