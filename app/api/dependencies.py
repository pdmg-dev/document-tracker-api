# app/api/dependencies.py

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories import (custom_field_repository, document_repository,
                              document_type_repository, status_repository,
                              user_repository)
from app.services import (auth_service, custom_field_service, document_service,
                          document_type_service, status_service, token_service,
                          user_service)
from app.services.token_service import get_token_service


def get_status_service(
    session: AsyncSession = Depends(get_db),
) -> status_service.StatusService:
    repo = status_repository.StatusRepository(session)
    return status_service.StatusService(repo)


def get_admin_service(
    session: AsyncSession = Depends(get_db),
) -> user_service.AdminService:
    repo = user_repository.UserRepository(session)
    return user_service.AdminService(repo)


def get_auth_service(
    session: AsyncSession = Depends(get_db),
    token: token_service.TokenService = Depends(get_token_service),
) -> auth_service.AuthService:
    repo = user_repository.UserRepository(session)
    return auth_service.AuthService(repo, token)


def get_document_type_service(session: AsyncSession = Depends(get_db)) -> document_type_service.DocumentTypeService:
    repo = document_type_repository.DocumentTypeRepository(session)
    return document_type_service.DocumentTypeService(repo)


def get_custom_field_service(session: AsyncSession = Depends(get_db)) -> custom_field_service.CustomFieldService:
    repo = custom_field_repository.CustomFieldRepository(session)
    return custom_field_service.CustomFieldService(repo)


def get_document_service(
    session: AsyncSession = Depends(get_db),
) -> document_service.DocumentService:
    doc_type_repo = document_type_repository.DocumentTypeRepository(session)
    field_repo = custom_field_repository.CustomFieldRepository(session)
    doc_repo = document_repository.DocumentRepository(session)
    status_repo = status_repository.StatusRepository(session)
    return document_service.DocumentService(doc_type_repo, field_repo, doc_repo, status_repo)
