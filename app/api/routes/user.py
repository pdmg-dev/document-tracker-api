# app/routes/user.py

from typing import Annotated

from fastapi import APIRouter, Depends

from ..core.security import get_current_active_user
from ..models.user import User
from ..schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserRead)
def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
