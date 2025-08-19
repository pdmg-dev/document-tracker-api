# app/models/status.py

import enum
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, DateTime, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class StatusCategory(str, enum.Enum):
    MAIN = "main"
    SUB = "sub"


class Status(Base):
    __tablename__ = "statuses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    category: Mapped[StatusCategory] = mapped_column(Enum(StatusCategory), default=StatusCategory.MAIN, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    documents: Mapped[List["Document"]] = relationship("Document", back_populates="current_status", lazy="selectin")
    histories_as_old: Mapped[List["DocumentHistory"]] = relationship(
        "DocumentHistory", back_populates="old_status", foreign_keys="DocumentHistory.old_status_id", lazy="selectin"
    )
    histories_as_new: Mapped[List["DocumentHistory"]] = relationship(
        "DocumentHistory", back_populates="new_status", foreign_keys="DocumentHistory.new_status_id", lazy="selectin"
    )
