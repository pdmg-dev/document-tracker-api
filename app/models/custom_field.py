# app/models/custom_field.py

from sqlalchemy import JSON, Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class CustomField(Base):
    __tablename__ = "custom_fields"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    document_type_id: Mapped[int] = mapped_column(ForeignKey("document_types.id"))
    name: Mapped[str] = mapped_column(String(100))
    field_type: Mapped[str] = mapped_column(String(50))  # e.g., "string", "number", "date", "select"
    required: Mapped[bool] = mapped_column(Boolean, default=False)
    options: Mapped[list[dict]] = mapped_column(JSON, nullable=True)  # For dropdown/select fields

    document_type: Mapped["DocumentType"] = relationship(back_populates="fields")
