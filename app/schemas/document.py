from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.history import HistoryDetail
from app.schemas.status import CurrentStatusRead
from app.schemas.user import UserRead


class DocumentBase(BaseModel):
    document_type_id: int
    data: Dict[str, Any]  # TODO: Refine this later with stricter validation

class DocumentCreate(DocumentBase):
    model_config = ConfigDict(extra="forbid")

class DocumentUpdate(BaseModel):
    data: Optional[Dict[str, Any]] = None
    current_status_id: Optional[int] = None
    updated_by: Optional[int] = None
    is_active: Optional[bool] = None
    is_archived: Optional[bool] = None

# Slim version (for listing quickly or dashboard)
class DocumentRead(DocumentBase):
    id: int
    tracking_number: str
    current_status: CurrentStatusRead
    created_by: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Full detail (used for "view document details")
class DocumentDetail(DocumentRead):
    is_active: Optional[bool] = None
    is_archived: Optional[bool] = None 
    creator: Optional[UserRead] = None
    updater: Optional[UserRead] = None
    updated_at: datetime
    status_history: List[HistoryDetail] = []
