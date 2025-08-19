from fastapi import APIRouter, Depends
from app.schemas.history import HistoryRead, HistoryDetail
from app.services.history_service import HistoryService
from app.core.security import get_current_active_user
from app.models.user import User
from app.api.dependencies import get_history_service

router = APIRouter()


@router.get("/documents/{doc_id}", response_model=list[HistoryRead])
async def list_document_history(
    document_id: int,
    history_service: HistoryService = Depends(get_history_service),
    current_user: User = Depends(get_current_active_user),
):
    return await history_service.get_history_by_document(document_id)


@router.get("/{history_id}", response_model=HistoryDetail)
async def get_history_detail(
    history_id: int,
    history_service: HistoryService = Depends(get_history_service),
    current_user: User = Depends(get_current_active_user),
):
    return await history_service.get_history_detail(history_id)
