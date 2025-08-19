# app/services/document_service.py

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Sequence

from app.core.logger import get_logger
from app.models.document import Document
from app.repositories.custom_field_repository import CustomFieldRepository
from app.repositories.document_repository import DocumentRepository
from app.repositories.document_type_repository import DocumentTypeRepository
from app.repositories.status_repository import StatusRepository
from app.schemas.document import DocumentCreate, DocumentUpdate
from app.utils import exceptions

logger = get_logger(__name__)


class DocumentService:
    def __init__(
        self,
        document_type_repository: DocumentTypeRepository,
        custom_field_repository: CustomFieldRepository,
        document_repository: DocumentRepository,
        status_repository: StatusRepository,
    ):
        self.document_type_repository = document_type_repository
        self.custom_field_repository = custom_field_repository
        self.document_repository = document_repository
        self.status_repository = status_repository

    async def _validate_data(self, document_type_id: int, data: Dict[str, Any]) -> None:
        fields = await self.custom_field_repository.get_all_by_document_type(document_type_id)
        field_map = {field.name: field for field in fields}
        # Check required fields
        for field in fields:
            if field.required and field.name not in data:
                raise exceptions.bad_request(f"Missing required field: {field.name}")

        # Check unexpected fields
        for key in data.keys():
            if key not in field_map:
                raise exceptions.bad_request(f"Unexpected field: {key}")

        # Check type validation (basic for now)
        for name, value in data.items():
            field = field_map[name]
            if value is None:
                if field.required:
                    raise exceptions.bad_request(f"Missing required field: {name}")
                continue
            if field.field_type == "number" and not isinstance(value, (int, float)):
                raise exceptions.bad_request(f"Field {name} must be a number")
            if field.field_type == "string" and not isinstance(value, str):
                raise exceptions.bad_request(f"Field {name} must be a string")
            if field.field_type == "select":
                if value not in (field.options or []):
                    raise exceptions.bad_request(f"Field {name} must be one of {field.options}")

    async def create_document(self, user_id: int, data: DocumentCreate) -> Document:
        document_type = await self.document_type_repository.get_by_id(data.document_type_id)
        if not document_type:
            raise exceptions.not_found(f"DocumentType {data.document_type_id} not found")

        # Validate data in the custom fields
        await self._validate_data(data.document_type_id, data.data)

        tracking_number = self._generate_tracking_number()
        logger.info(f"Creating document with tracking number {tracking_number}")

        status = await self.status_repository.get_by_name("received")
        if not status:
            raise exceptions.bad_request("Default status 'received' not found in statuses table")
        status_id = status.id

        document = Document(
            document_type_id=data.document_type_id,
            data=data.data,
            tracking_number=tracking_number,
            current_status_id=status_id,
            created_by=user_id,
        )
        return await self.document_repository.create(document)

    async def get_document(self, document_id: int) -> Document:
        document = await self.document_repository.get_by_id(document_id)
        if not document or not document.is_active:
            logger.warning(f"Document {document_id} not found or deleted")
            raise exceptions.not_found(f"Document {document_id} not found")
        return document

    async def get_all_documents(self) -> Sequence[Document]:
        documents = await self.document_repository.get_all()
        return documents

    async def update_document(self, document_id: int, updates: DocumentUpdate) -> Document:
        document = await self.get_document(document_id)
        logger.info(f"Updating document {document_id} with fields: {updates.model_dump(exclude_unset=True)}")
        if updates.data:
            await self._validate_data(document.document_type_id, updates.data)
            document.data = {**document.data, **updates.data}

        for field, value in updates.model_dump(exclude_unset=True).items():
            if field != "data":
                setattr(document, field, value)

        return await self.document_repository.update(document)

    async def delete_document(self, document_id: int) -> None:
        document = await self.get_document(document_id)
        document.is_active = False
        await self.document_repository.delete(document)

    async def archive_document(self, document_id: int) -> Document:
        document = await self.get_document(document_id)
        document.is_archived = True
        return await self.document_repository.update(document)

    def _generate_tracking_number(self) -> str:
        year = datetime.now(timezone.utc).year
        unique_id = uuid.uuid4().hex[:6].upper()
        return f"DOC-{year}-{unique_id}"
