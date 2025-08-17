from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.schemas.status import StatusRead
from app.schemas.user import UserRead


class HistoryBase(BaseModel):
    remarks: Optional[str] = None


class HistoryCreate(HistoryBase):
    document_id: int
    old_status_id: Optional[int] = None
    new_status_id: int
    changed_by: int


# Slim version (for listing quickly)
class HistoryRead(BaseModel):
    id: int
    new_status: StatusRead
    timestamp: datetime
    changed_by_user: UserRead

    model_config = ConfigDict(from_attributes=True)


# Full detail (used for "view document details")
class HistoryDetail(HistoryRead):
    old_status: Optional[StatusRead] = None
    remarks: Optional[str] = None
