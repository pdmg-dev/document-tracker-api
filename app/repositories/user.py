# app/repositories/user.py

from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.user import User


class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, user: User) -> None:
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def get_user(self, username: int) -> User:
        statement = select(User).where(User.username == username)
        return self.db_session.execute(statement).scalar_one_or_none()


def get_user_repository(db_session: Annotated[Session, Depends(get_db)]) -> Session:
    return UserRepository(db_session)
