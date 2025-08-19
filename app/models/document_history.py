# app/models/history.py

from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class DocumentHistory(Base):
    __tablename__ = "document_history"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"), nullable=False)

    old_status_id: Mapped[int | None] = mapped_column(ForeignKey("statuses.id"), nullable=True)
    new_status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"), nullable=False)

    changed_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    remarks: Mapped[str] = mapped_column(String(500), nullable=True)

    data_snapshot: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    document: Mapped["Document"] = relationship("Document", back_populates="status_history", lazy="selectin")
    old_status: Mapped["Status"] = relationship(
        "Status", back_populates="histories_as_old", foreign_keys=[old_status_id], lazy="selectin"
    )
    new_status: Mapped["Status"] = relationship(
        "Status", back_populates="histories_as_new", foreign_keys=[new_status_id], lazy="selectin"
    )
    changed_by_user: Mapped["User"] = relationship(
        "User", back_populates="status_changes", foreign_keys=[changed_by], lazy="selectin"
    )
