from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.user import UserRole


class UserBase(BaseModel):
    full_name: str
    username: str
    role: UserRole = UserRole.STAFF


# For ADMIN access only
class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: str | None = None
    username: str | None = None
    role: UserRole | None = UserRole.STAFF
    password: str | None = None


class UserRead(BaseModel):
    id: int
    full_name: str
    username: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


# For ADMIN access only
class UserDetail(UserRead):
    is_active: bool
    created_at: datetime
    updated_at: datetime


# For ADMIN access only
class UserDelete(BaseModel):
    is_active: bool | None = None
