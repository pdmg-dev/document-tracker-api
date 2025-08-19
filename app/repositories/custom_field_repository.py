from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.custom_field import CustomField


class CustomFieldRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, custom_field: CustomField) -> CustomField:
        self.session.add(custom_field)
        await self.session.commit()
        await self.session.refresh(custom_field)
        return custom_field

    async def get_all_by_document_type(self, document_type_id: int) -> Sequence[CustomField]:
        stmt = select(CustomField).where(CustomField.document_type_id == document_type_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, field_id: int) -> Optional[CustomField]:
        stmt = select(CustomField).where(CustomField.id == field_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, custom_field: CustomField) -> CustomField:
        await self.session.commit()
        await self.session.refresh(custom_field)
        return custom_field

    async def delete(self, custom_field: CustomField) -> None:
        await self.session.delete(custom_field)
        await self.session.commit()