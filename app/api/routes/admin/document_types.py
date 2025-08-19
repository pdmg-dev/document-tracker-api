# app/api/routes/admin/document_types.py

from typing import Sequence

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_document_type_service
from app.core.security import get_current_admin_user
from app.models.user import User
from app.schemas.document_type import (DocumentTypeCreate, DocumentTypeRead,
                                       DocumentTypeUpdate)
from app.services.document_type_service import DocumentTypeService

router = APIRouter()


@router.post("/document-types", response_model=DocumentTypeRead, status_code=status.HTTP_201_CREATED)
async def create_document_type(
    data: DocumentTypeCreate,
    current_admin: User = Depends(get_current_admin_user),
    service: DocumentTypeService = Depends(get_document_type_service),
):
    return await service.create_document_type(data)


@router.get("/document-types", response_model=Sequence[DocumentTypeRead])
async def list_document_types(
    current_admin: User = Depends(get_current_admin_user),
    service: DocumentTypeService = Depends(get_document_type_service),
):
    return await service.get_all_document_types()


@router.get("/document-types/{document_type_id}", response_model=DocumentTypeRead)
async def get_document_type(
    document_type_id: int,
    current_admin: User = Depends(get_current_admin_user),
    service: DocumentTypeService = Depends(get_document_type_service),
):
    return await service.get_document_type(document_type_id)


@router.patch("/document-types/{document_type_id}", response_model=DocumentTypeRead)
async def update_document_type(
    document_type_id: int,
    updates: DocumentTypeUpdate,
    current_admin: User = Depends(get_current_admin_user),
    service: DocumentTypeService = Depends(get_document_type_service),
):
    return await service.update_document_type(document_type_id, updates)


@router.delete("/document-types/{document_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document_type(
    document_type_id: int,
    current_admin: User = Depends(get_current_admin_user),
    service: DocumentTypeService = Depends(get_document_type_service),
):
    await service.delete_document_type(document_type_id)
    return None
