# app/models/document.py

from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.status import Status


class Document(Base):
    __tablename__ = "documents"

    document_type_id: Mapped[str] = mapped_column(ForeignKey("document_types.id"))
    data: Mapped[dict] = mapped_column(JSON)  # Stores dynamic field values

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tracking_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
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

    document_type: Mapped["DocumentType"] = relationship("DocumentType")
    creator: Mapped["User"] = relationship(
        "User", back_populates="documents_created", foreign_keys=[created_by], lazy="selectin"
    )
    updater: Mapped["User"] = relationship(
        "User", back_populates="documents_updated", foreign_keys=[updated_by], lazy="selectin"
    )
    current_status: Mapped["Status"] = relationship(back_populates="documents", lazy="selectin")

    # status_history: Mapped[List["DocumentStatusHistory"]] = relationship("DocumentStatusHistory", back_populates="document", cascade="all, delete-orphan")
