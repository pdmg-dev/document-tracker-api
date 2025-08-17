from datetime import datetime
from pydantic import BaseModel, ConfigDict
import enum


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


class StatusRead(StatusBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
