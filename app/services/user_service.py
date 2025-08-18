# app/services/admin_service.py

from typing import Sequence

from app.core.logger import get_logger
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserDetail, UserRead, UserUpdate
from app.utils import exceptions

logger = get_logger(__name__)


class AdminService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, create_data: UserCreate) -> UserRead:
        existing_user = await self.user_repository.get_user(create_data.username)
        if existing_user:
            logger.info(f"User creation failed: '{create_data.username}' already exists.")
            raise exceptions.bad_request("User already exists")

        hashed_password = hash_password(create_data.password)
        new_user = User(
            **create_data.model_dump(exclude={"password"}),
            hashed_password=hashed_password,
        )

        created_user = await self.user_repository.create(new_user)
        logger.info(f"User created successfully: '{created_user.username}'")
        return UserRead.model_validate(created_user)

    async def get_all_users(self, exclude_user_id: int) -> Sequence[UserRead]:
        users = await self.user_repository.get_all(exclude_user_id=exclude_user_id)
        if not users:
            logger.info("User fetch failed: No active users found.")
            raise exceptions.bad_request("No active users found")
        return [UserRead.model_validate(user) for user in users]

    async def get_user_by_id(self, user_id: int) -> UserDetail:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            logger.info(f"User fetch failed: ID {user_id} not found.")
            raise exceptions.not_found("User not found")
        return UserDetail.model_validate(user)

    async def update_user(self, user_id: int, update_data: UserUpdate) -> UserDetail:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            logger.info(f"User update failed: ID {user_id} not found.")
            raise exceptions.not_found("User not found")

        for field, value in update_data.model_dump(exclude_unset=True).items():
            if field == "password":
                setattr(user, "hashed_password", hash_password(value))
            else:
                setattr(user, field, value)

        updated_user = await self.user_repository.update(user)
        logger.info(f"User updated successfully: '{updated_user.username}'")
        return UserDetail.model_validate(updated_user)

    async def delete_user(self, user_id: int) -> None:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            logger.info(f"User deletion failed: ID {user_id} not found.")
            raise exceptions.not_found("User not found")

        await self.user_repository.delete(user)
        logger.info(f"User deleted successfully: ID {user_id}")
