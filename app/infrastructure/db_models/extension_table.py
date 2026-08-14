from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.db_models.base_table import Base

if TYPE_CHECKING:
    from app.infrastructure.db_models.file_table import File
    from app.infrastructure.db_models.mime_type_table import MimeType

class Extension(Base):
    id: Mapped[int] = mapped_column(nullable=False, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    mime_type_id: Mapped[int] = mapped_column(ForeignKey("mime_type.id", ondelete="CASCADE"), nullable=False)

    mime_type: Mapped["MimeType"] = relationship(
        back_populates="extensions"
    )

    files: Mapped[list["File"]] = relationship(
        back_populates="extension", cascade="all, delete-orphan", passive_deletes=True
    )
