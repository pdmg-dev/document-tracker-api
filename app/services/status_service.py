# app/services/status_service.py

from typing import Sequence

from app.core.logger import get_logger
from app.models.status import Status
from app.repositories.status_repository import StatusRepository
from app.schemas.status import StatusCreate, StatusUpdate
from app.utils import exceptions

logger = get_logger(__name__)


class StatusService:
    def __init__(self, status_repository: StatusRepository):
        self.status_repository = status_repository

    async def create_status(self, data: StatusCreate) -> Status:
        status = Status(
            name=data.name,
            category=data.category,
            description=data.description,
        )
        return await self.status_repository.create(status)

    async def get_status(self, status_id: int) -> Status:
        status = await self.status_repository.get_by_id(status_id)
        if not status:
            logger.warning(f"Status {status_id} not found or deleted")
            raise exceptions.not_found(f"Status {status_id} not found")
        return status

    async def get_all_statuses(self) -> Sequence[Status]:
        statuses = await self.status_repository.get_all()
        return [status for status in statuses if status.is_active]

    async def update_status_info(self, status_id: int, updates: StatusUpdate) -> Status:
        status = await self.get_status(status_id)
        logger.info(f"Updating status {status_id} with fields: {updates.model_dump(exclude_unset=True)}")

        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(status, field, value)

        return await self.status_repository.update(status)

    async def delete_status(self, status_id: int) -> None:
        status = await self.get_status(status_id)
        await self.status_repository.delete(status)
