# app/repositories/status_repo.py

from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.status import Status


class StatusRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, status: Status) -> Status:
        self.session.add(status)
        await self.session.commit()
        await self.session.refresh(status)
        return status

    async def get_all(self) -> Sequence[Status]:
        stmt = select(Status)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, status_id: int) -> Optional[Status]:
        stmt = select(Status).where(Status.id == status_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_name(self, name: str) -> Optional[Status]:
        stmt = select(Status).where(Status.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, status: Status) -> Status:
        await self.session.commit()
        await self.session.refresh(status)
        return status

    async def delete(self, status: Status) -> None:
        await self.session.delete(status)
        await self.session.commit()
