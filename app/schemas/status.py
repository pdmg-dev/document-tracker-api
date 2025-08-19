import enum
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StatusCategory(str, enum.Enum):
    MAIN = "main"
    SUB = "sub"


class StatusBase(BaseModel):
    name: str
    category: StatusCategory = StatusCategory.MAIN
    description: str | None = None


class StatusCreate(StatusBase):
    pass


class StatusUpdate(BaseModel):
    name: str | None = None
    category: StatusCategory | None = None
    description: str | None = None

class CurrentStatusRead(StatusBase):
    pass

class StatusRead(StatusBase):
    id: int
    created_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class StatusDelete(BaseModel):
    is_active: bool
