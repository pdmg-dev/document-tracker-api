# app/api/routes/documents.py

from typing import Sequence

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_document_service
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.document import DocumentCreate, DocumentRead, DocumentUpdate
from app.services.document_service import DocumentService

router = APIRouter()


@router.post("/", response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
async def create_document(
    data: DocumentCreate,
    service: DocumentService = Depends(get_document_service),
    current_user: User = Depends(get_current_active_user),
):
    return await service.create_document(current_user.id, data)


@router.get("/", response_model=Sequence[DocumentRead])
async def list_documents(
    service: DocumentService = Depends(get_document_service),
    current_user: User = Depends(get_current_active_user),
):
    return await service.get_all_documents()


@router.get("/{document_id}", response_model=DocumentRead)
async def get_document(
    document_id: int,
    service: DocumentService = Depends(get_document_service),
    current_user: User = Depends(get_current_active_user),
):
    return await service.get_document(document_id)


@router.patch("/documents/{document_id}", response_model=DocumentRead)
async def update_document(
    document_id: int,
    updates: DocumentUpdate,
    current_user: User = Depends(get_current_active_user),
    service: DocumentService = Depends(get_document_service),
):
    return await service.update_document(document_id, updates)


@router.delete("/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_active_user),
    service: DocumentService = Depends(get_document_service),
):
    await service.delete_document(document_id)
    return None


@router.post("/{doc_id}/archive", response_model=DocumentRead)
async def archive_document(doc_id: int, service: DocumentService = Depends(get_document_service)):
    return await service.archive_document(doc_id)
