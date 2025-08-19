# app/services/document_type_service.py

from typing import Sequence

from app.core.logger import get_logger
from app.models.document_type import DocumentType
from app.repositories.document_type_repository import DocumentTypeRepository
from app.schemas.document_type import DocumentTypeCreate, DocumentTypeUpdate
from app.utils import exceptions

logger = get_logger(__name__)


class DocumentTypeService:
    def __init__(self, repo: DocumentTypeRepository):
        self.repo = repo

    async def create_document_type(self, data: DocumentTypeCreate) -> DocumentType:
        doc_type = DocumentType(name=data.name, description=data.description)
        return await self.repo.create(doc_type)

    async def get_document_type(self, document_type_id: int) -> DocumentType:
        doc_type = await self.repo.get_by_id(document_type_id)
        if not doc_type:
            logger.warning(f"DocumentType {document_type_id} not found")
            raise exceptions.not_found(f"DocumentType {document_type_id} not found")
        return doc_type

    async def get_all_document_types(self) -> Sequence[DocumentType]:
        return await self.repo.get_all()

    async def update_document_type(self, document_type_id: int, updates: DocumentTypeUpdate) -> DocumentType:
        doc_type = await self.get_document_type(document_type_id)
        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(doc_type, field, value)
        return await self.repo.update(doc_type)

    async def delete_document_type(self, document_type_id: int) -> None:
        doc_type = await self.get_document_type(document_type_id)
        await self.repo.delete(doc_type)