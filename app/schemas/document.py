from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from app.schemas.status import StatusRead
from app.schemas.user import UserRead
from app.schemas.history import HistoryDetail


class DocumentBase(BaseModel):
    tracking_number: str
    document_type: str
    origin: str
    title: str
    description: Optional[str] = None
    is_active: bool = True
    is_archived: bool = False


class DocumentCreate(DocumentBase):
    created_by: int
    current_status_id: int


class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    document_type: Optional[str] = None
    origin: Optional[str] = None
    is_active: Optional[bool] = None
    is_archived: Optional[bool] = None
    updated_by: Optional[int] = None


# Slim version (for listing quickly or dashboard)
class DocumentRead(DocumentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    current_status: StatusRead

    model_config = ConfigDict(from_attributes=True)


# Full detail (used for "view document details")
class DocumentDetail(DocumentRead):
    creator: Optional[UserRead] = None
    updater: Optional[UserRead] = None
    status_history: List[HistoryDetail] = []
