# app/models/document.py

from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from app.core.database import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    tracking_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    document_type: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    origin: Mapped[str] = mapped_column(String(100), index=True, nullable=False)

    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)

    current_status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"), nullable=False)

    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    updated_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    creator = relationship("User", back_populates="documents_created", foreign_keys=[created_by])
    updater = relationship("User", back_populates="documents_updated", foreign_keys=[updated_by])
    current_status = relationship("Status", back_populates="documents")
    status_history: Mapped[List["DocumentStatusHistory"]] = relationship(
        "DocumentStatusHistory", back_populates="document", cascade="all, delete-orphan"
    )
