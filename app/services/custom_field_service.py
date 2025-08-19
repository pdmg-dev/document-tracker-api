# app/services/custom_field_service.py

from typing import Sequence

from app.core.logger import get_logger
from app.models.custom_field import CustomField
from app.repositories.custom_field_repository import CustomFieldRepository
from app.schemas.custom_field import CustomFieldCreate, CustomFieldUpdate
from app.utils import exceptions

logger = get_logger(__name__)


class CustomFieldService:
    def __init__(self, repo: CustomFieldRepository):
        self.repo = repo

    async def create_custom_field(self, data: CustomFieldCreate) -> CustomField:
        field = CustomField(
            document_type_id=data.document_type_id,
            name=data.name,
            field_type=data.field_type,
            required=data.required,
            options=data.options,
        )
        return await self.repo.create(field)

    async def get_custom_field(self, field_id: int) -> CustomField:
        field = await self.repo.get_by_id(field_id)
        if not field:
            logger.warning(f"CustomField {field_id} not found")
            raise exceptions.not_found(f"CustomField {field_id} not found")
        return field

    async def get_fields_by_document_type(self, document_type_id: int) -> Sequence[CustomField]:
        return await self.repo.get_all_by_document_type(document_type_id)

    async def update_custom_field(self, field_id: int, updates: CustomFieldUpdate) -> CustomField:
        field = await self.get_custom_field(field_id)
        for attr, value in updates.model_dump(exclude_unset=True).items():
            setattr(field, attr, value)
        return await self.repo.update(field)

    async def delete_custom_field(self, field_id: int) -> None:
        field = await self.get_custom_field(field_id)
        await self.repo.delete(field)