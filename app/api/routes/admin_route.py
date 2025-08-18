# app/api/routes/admins.py

from typing import List

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_admin_service
from app.core.security import get_current_admin_user
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    current_admin: User = Depends(get_current_admin_user),
    service: AdminService = Depends(get_admin_service),
):
    return await service.create_user(data)


@router.get("/users", response_model=List[UserRead])
async def get_all_users(
    current_admin: User = Depends(get_current_admin_user),
    service: AdminService = Depends(get_admin_service),
):
    return await service.get_all_users(current_admin.id)


@router.get("/users/{user_id}", response_model=UserRead)
async def get_user_by_id(
    user_id: int,
    current_admin: User = Depends(get_current_admin_user),
    service: AdminService = Depends(get_admin_service),
):
    return await service.get_user_by_id(user_id)


@router.patch("/users/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    data: UserUpdate,
    current_admin: User = Depends(get_current_admin_user),
    service: AdminService = Depends(get_admin_service),
):
    return await service.update_user(user_id, data)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_admin: User = Depends(get_current_admin_user),
    service: AdminService = Depends(get_admin_service),
):
    await service.delete_user(user_id)
    return None
