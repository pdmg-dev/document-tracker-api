# app/repositories/document_type_repository.py

from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document_type import DocumentType


class DocumentTypeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, document_type: DocumentType) -> DocumentType:
        self.session.add(document_type)
        await self.session.commit()
        await self.session.refresh(document_type)
        return document_type

    async def get_all(self) -> Sequence[DocumentType]:
        stmt = select(DocumentType)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, document_type_id: int) -> Optional[DocumentType]:
        stmt = select(DocumentType).where(DocumentType.id == document_type_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, document_type: DocumentType) -> DocumentType:
        await self.session.commit()
        await self.session.refresh(document_type)
        return document_type

    async def delete(self, document_type: DocumentType) -> None:
        await self.session.delete(document_type)
        await self.session.commit()