# app/repositories/user.py

from typing import Annotated, List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.user import User


class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, user: User) -> User:
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def get_user(self, username: int) -> Optional[User]:
        statement = select(User).where(User.username == username)
        return self.db_session.scalars(statement).one_or_none()

    def get_all(self) -> List[User]:
        statement = select(User).where(User.is_active.is_(True))
        return self.db_session.scalars(statement).all()

    def get_by_id(self, user_id: int) -> Optional[User]:
        statement = select(User).where(User.id == user_id)
        return self.db_session.scalars(statement).one_or_none()

    def update(self, user) -> User:
        self.db_session.commit()
        self.db_session.refresh(user)
        return user


def get_user_repository(
    db_session: Annotated[Session, Depends(get_db)],
) -> UserRepository:
    return UserRepository(db_session)
