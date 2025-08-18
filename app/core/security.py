# app/core/security.py

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.logger import get_logger
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.services.token_service import TokenService, get_token_service
from app.utils import exceptions

logger = get_logger(__name__)

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def hash_password(plain_password: str) -> str:
    return password_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    token_service: TokenService = Depends(get_token_service),
    session: AsyncSession = Depends(get_db),
) -> User:
    token_data = token_service.decode_token(token)

    repo = UserRepository(session)
    user = await repo.get_user(token_data.username)

    if user is None:
        logger.info(f"User lookup failed: '{token_data.username}' not found.")
        raise exceptions.unauthorized("User not found")

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        logger.info(f"Access denied: User '{current_user.username}' is inactive.")
        raise exceptions.bad_request("User account is inactive")

    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if current_user.role != UserRole.ADMIN:
        logger.info(f"Access denied: User '{current_user.username}' is not an admin.")
        raise exceptions.unauthorized("Admin access required")
    return current_user
