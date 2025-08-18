# app/api/dependencies.py

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories import status_repository, user_repository
from app.services import (admin_service, auth_service, status_service,
                          token_service)
from app.services.token_service import get_token_service


def get_status_service(
    session: AsyncSession = Depends(get_db),
) -> status_service.StatusService:
    repo = status_repository.StatusRepository(session)
    return status_service.StatusService(repo)


def get_admin_service(
    session: AsyncSession = Depends(get_db),
) -> admin_service.AdminService:
    repo = user_repository.UserRepository(session)
    return admin_service.AdminService(repo)


def get_auth_service(
    session: AsyncSession = Depends(get_db),
    token: token_service.TokenService = Depends(get_token_service),
) -> auth_service.AuthService:
    repo = user_repository.UserRepository(session)
    return auth_service.AuthService(repo, token)
