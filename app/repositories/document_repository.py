# app/repositories/document_repo.py

from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document


class DocumentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, document: Document) -> Document:
        self.session.add(document)
        await self.session.commit()
        await self.session.refresh(document)
        return document

    async def get_by_id(self, document_id: int) -> Optional[Document]:
        stmt = select(Document).where(Document.id == document_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[Document]:
        stmt = select(Document)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, document: Document) -> Document:
        await self.session.commit()
        await self.session.refresh(document)
        return document

    async def delete(self, document: Document) -> None:
        await self.session.delete(document)
        await self.session.commit()

    async def get_by_tracking_number(self, tracking_number: str) -> Optional[Document]:
        stmt = select(Document).where(Document.tracking_number == tracking_number)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
