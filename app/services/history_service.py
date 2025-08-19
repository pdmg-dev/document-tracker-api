from app.repositories.history_repository import HistoryRepository
from app.schemas.history import HistoryCreate
from app.models.document_history import DocumentHistory
from app.schemas.history import HistoryRead, HistoryDetail
from app.utils import exceptions


class HistoryService:
    def __init__(self, history_repository: HistoryRepository):
        self.history_repository = history_repository

    async def create_history_entry(self, history_in: HistoryCreate):
        history = DocumentHistory(**history_in.model_dump())
        return await self.history_repository.create(history)

    async def get_history_by_document(self, doc_id: int) -> list[HistoryRead]:
        histories = await self.history_repository.get_by_document(doc_id)
        return [HistoryRead.model_validate(h, from_attributes=True) for h in histories]

    async def get_history_detail(self, history_id: int) -> HistoryDetail:
        history = await self.history_repository.get_by_id(history_id)
        if not history:
            raise exceptions.not_found(f"History record {history_id} not found")
        return HistoryDetail.model_validate(history, from_attributes=True)
