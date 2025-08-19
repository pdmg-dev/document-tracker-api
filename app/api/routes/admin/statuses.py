# app/api/statuses.py

from typing import Sequence

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_status_service
from app.core.security import get_current_admin_user
from app.models.user import User
from app.schemas.status import StatusCreate, StatusRead, StatusUpdate
from app.services.status_service import StatusService

router = APIRouter()


@router.post("/statuses", response_model=StatusRead, status_code=status.HTTP_201_CREATED)
async def create_status(
    data: StatusCreate,
    current_admin: User = Depends(get_current_admin_user),
    service: StatusService = Depends(get_status_service),
):
    return await service.create_status(data)


@router.get("/statuses", response_model=Sequence[StatusRead])
async def get_all_statuses(
    current_admin: User = Depends(get_current_admin_user), service: StatusService = Depends(get_status_service)
):
    return await service.get_all_statuses()


@router.get("/statuses/{status_id}", response_model=StatusRead)
async def get_status(
    status_id: int,
    current_admin: User = Depends(get_current_admin_user),
    service: StatusService = Depends(get_status_service),
):
    return await service.get_status(status_id)


@router.patch("/statuses/{status_id}", response_model=StatusRead)
async def update_status_info(
    status_id: int,
    updates: StatusUpdate,
    current_admin: User = Depends(get_current_admin_user),
    service: StatusService = Depends(get_status_service),
):
    return await service.update_status_info(status_id, updates)


@router.delete("/statuses/{status_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_status(
    status_id: int,
    current_admin: User = Depends(get_current_admin_user),
    service: StatusService = Depends(get_status_service),
):
    await service.delete_status(status_id)
    return None
