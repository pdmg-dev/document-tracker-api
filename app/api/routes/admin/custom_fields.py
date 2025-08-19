# app/api/routes/admin/custom_fields.py

from typing import Sequence

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_custom_field_service
from app.core.security import get_current_admin_user
from app.models.user import User
from app.schemas.custom_field import (CustomFieldCreate, CustomFieldRead,
                                      CustomFieldUpdate)
from app.services.custom_field_service import CustomFieldService

router = APIRouter()


@router.post("/custom-fields", response_model=CustomFieldRead, status_code=status.HTTP_201_CREATED)
async def create_custom_field(
    data: CustomFieldCreate,
    current_admin: User = Depends(get_current_admin_user),
    service: CustomFieldService = Depends(get_custom_field_service),
):
    return await service.create_custom_field(data)


@router.get("/document-types/{document_type_id}/custom-fields", response_model=Sequence[CustomFieldRead])
async def list_custom_fields_for_document_type(
    document_type_id: int,
    current_admin: User = Depends(get_current_admin_user),
    service: CustomFieldService = Depends(get_custom_field_service),
):
    return await service.get_fields_by_document_type(document_type_id)


@router.get("/custom-fields/{field_id}", response_model=CustomFieldRead)
async def get_custom_field(
    field_id: int,
    current_admin: User = Depends(get_current_admin_user),
    service: CustomFieldService = Depends(get_custom_field_service),
):
    return await service.get_custom_field(field_id)


@router.patch("/custom-fields/{field_id}", response_model=CustomFieldRead)
async def update_custom_field(
    field_id: int,
    updates: CustomFieldUpdate,
    current_admin: User = Depends(get_current_admin_user),
    service: CustomFieldService = Depends(get_custom_field_service),
):
    return await service.update_custom_field(field_id, updates)


@router.delete("/custom-fields/{field_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_custom_field(
    field_id: int,
    current_admin: User = Depends(get_current_admin_user),
    service: CustomFieldService = Depends(get_custom_field_service),
):
    await service.delete_custom_field(field_id)
    return None
