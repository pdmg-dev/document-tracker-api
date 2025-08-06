
# app/routes/user.py

from typing import Annotated

from fastapi import APIRouter, Depends

from ..schemas.user import UserLogin
from ..services.user import UserService, get_user_service

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/login")
def login(
    login_data: UserLogin,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return user_service.login_for_access_token(login_data)