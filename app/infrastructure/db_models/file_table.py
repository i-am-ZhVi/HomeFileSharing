
from datetime import datetime, tzinfo
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text
from infrastructure.db_models.base_table import Base

if TYPE_CHECKING:
    from app.infrastructure.db_models.extension_table import Extension
    from app.infrastructure.db_models.file_version_table import FileVersion

class File(Base):
    id: Mapped[int] = mapped_column(nullable=False, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    extension_id: Mapped[int] = mapped_column(ForeignKey("extension.id", ondelete="CASCADE"), nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=True)

    extension: Mapped["Extension"] = relationship(
        back_populates="files"
    )

    versions: Mapped[list["FileVersion"]] = relationship(
        back_populates="file", cascade="all, delete-orphan", passive_deletes=True
    )
