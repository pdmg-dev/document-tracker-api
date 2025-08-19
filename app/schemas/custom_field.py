# app/schemas/custom_field.py

from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class CustomFieldBase(BaseModel):
    name: str
    field_type: str # TODO: Consider using Literal for stricter typing
    required: bool = False
    options: Optional[List[str]] = None


class CustomFieldCreate(CustomFieldBase):
    document_type_id: int


class CustomFieldUpdate(BaseModel):
    name: Optional[str] = None
    field_type: Optional[str] = None  # TODO: Consider using Literal for stricter typing
    required: Optional[bool] = None
    options: Optional[List[str]] = None


class CustomFieldRead(CustomFieldBase):
    id: int
    document_type_id: int

    model_config = ConfigDict(from_attributes=True)
