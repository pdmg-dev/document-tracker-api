# app/schemas/document.py

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from ..models.document import DocumentStatus


class DocumentBase(BaseModel):
    tracking_number: str = Field(..., max_length=20)
    document_type: str = Field(..., max_length=50)
    payee_name: str = Field(..., max_length=100)
    amount: Decimal = Field(..., ge=0)
    originating_office: str | None = Field(None, max_length=100)
    current_status: DocumentStatus = Field(default=DocumentStatus.received)


class DocumentCreate(DocumentBase):
    created_by: int


class DocumentRead(DocumentBase):
    id: int
    created_at: datetime
    created_by: int
    is_deleted: bool
    is_archived: bool
    deleted_at: datetime | None = None
    archived_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class DocumentUpdate(BaseModel):
    tracking_number: str | None = Field(None, max_length=20)
    document_type: str | None = Field(None, max_length=50)
    payee_name: str | None = Field(None, max_length=100)
    amount: Decimal | None = Field(None, ge=0)
    originating_office: str | None = Field(None, max_length=100)
    current_status: DocumentStatus | None = None
    is_deleted: bool | None = None
    is_archived: bool | None = None
