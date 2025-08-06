# app/models/document.py

import enum
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DECIMAL, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..core.database import Base

if TYPE_CHECKING:
    from ..models.user import User


class DocumentStatus(str, enum.Enum):
    received = "received"
    processing = "processing"
    approved = "released"


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tracking_number: Mapped[str] = mapped_column(
        String(20), unique=True, index=True, nullable=False
    )
    document_type: Mapped[str] = mapped_column(String(50), nullable=False)
    payee_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), nullable=False)
    originating_office: Mapped[str] = mapped_column(String(100), nullable=True)

    current_status: Mapped[DocumentStatus] = mapped_column(
        Enum(DocumentStatus), default=DocumentStatus.received, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Foreign key
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # Relationship
    creator: Mapped["User"] = relationship("User", back_populates="created_documents")

    def __repr__(self) -> str:
        return (
            f"<Document(id={self.id}, tracking_number='{self.tracking_number}', "
            f"status='{self.current_status}', payee='{self.payee_name}')>"
        )
