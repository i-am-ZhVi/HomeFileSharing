
from datetime import datetime, tzinfo
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text
from infrastructure.db_models.base_table import Base


class File(Base):
    id: Mapped[int] = mapped_column(nullable=False, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    extension_id: Mapped[int] = mapped_column(ForeignKey("extension.id"), nullable=False)
    mime_type: Mapped[str] = mapped_column(nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=True)
    upload_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now(), server_default=text("TIMEZONE('utc', now())"))

    extension: Mapped["Extension"] = relationship(
        back_populates="files"
    )

    category: Mapped["Category"] = relationship(
        back_populates="files"
    )

    versions: Mapped[list["FileVersion"]] = relationship(
        back_populates="file", cascade="all, delete-orphan", passive_deletes=True
    )
