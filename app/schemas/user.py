from datetime import datetime
from pydantic import BaseModel, ConfigDict
import enum


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    STAFF = "staff"


class UserBase(BaseModel):
    full_name: str
    username: str
    role: UserRole = UserRole.STAFF
    is_active: bool = True


class UserCreate(UserBase):
    password: str  # plain password input


class UserUpdate(BaseModel):
    full_name: str | None = None
    username: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None
    password: str | None = None


class UserRead(BaseModel):
    id: int
    full_name: str
    username: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
