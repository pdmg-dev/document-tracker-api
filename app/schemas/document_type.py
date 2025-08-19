# app/schemas/document_type.py

from typing import Optional

from pydantic import BaseModel, ConfigDict


class DocumentTypeBase(BaseModel):
    name: str
    description: Optional[str] = None


class DocumentTypeCreate(DocumentTypeBase):
    pass

class DocumentTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class DocumentTypeRead(DocumentTypeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
