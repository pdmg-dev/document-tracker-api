# app/models/status.py

import enum
from datetime import datetime, timezone
from sqlalchemy import String, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
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

    # Relationships
    documents: Mapped[List["Document"]] = relationship("Document", back_populates="current_status")
    histories_as_old: Mapped[List["DocumentStatusHistory"]] = relationship(
        "DocumentStatusHistory", back_populates="old_status", foreign_keys="DocumentStatusHistory.old_status_id"
    )
    histories_as_new: Mapped[List["DocumentStatusHistory"]] = relationship(
        "DocumentStatusHistory", back_populates="new_status", foreign_keys="DocumentStatusHistory.new_status_id"
    )
