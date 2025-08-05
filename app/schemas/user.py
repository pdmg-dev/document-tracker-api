# app/schemas/user.py

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from ..models.user import UserRole

class UserCreate(BaseModel):
    full_name: str
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    full_name: str
    username: str
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)