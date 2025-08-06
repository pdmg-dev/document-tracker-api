# app/routes/admin.py

from typing import Annotated, List

from fastapi import APIRouter, Depends

from ..core.security import get_current_admin_user
from ..models.user import User
from ..schemas.user import UserCreate, UserRead
from ..services.admin import AdminService, get_admin_service

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/users", response_model=UserRead)
def create_user(
    create_data: UserCreate,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    current_user: Annotated[User, Depends(get_current_admin_user)],
):
    return admin_service.create_user(create_data)


@router.get("/users", response_model=List[UserRead])
def get_all_users(
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    current_user: Annotated[User, Depends(get_current_admin_user)],
):
    return admin_service.get_all_users()
