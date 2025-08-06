# app/schemas/user.py

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ..models.user import UserRole


class UserCreate(BaseModel):
    full_name: str = Field(..., max_length=100)
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8)


class UserRead(BaseModel):
    id: int
    full_name: str
    username: str
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
