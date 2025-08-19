from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence, Optional
from app.models.document_history import DocumentHistory


class HistoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, history: DocumentHistory):
        self.session.add(history)
        await self.session.commit()
        await self.session.refresh(history)
        return history

    async def get_by_document(self, document_id: int) -> Sequence[DocumentHistory]:
        stmt = (
            select(DocumentHistory)
            .where(DocumentHistory.document_id == document_id)
            .order_by(DocumentHistory.timestamp.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, history_id: int) -> Optional[DocumentHistory]:
        stmt = select(DocumentHistory).where(DocumentHistory.id == history_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
