# app/routes/admin.py

from typing import Annotated

from fastapi import APIRouter, Depends

from ..schemas.user import UserCreate, UserRead
from ..services.admin import AdminService, get_admin_service

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/users", response_model=UserRead)
def create_user(
    create_data: UserCreate,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
):
    return admin_service.create_user(create_data)
