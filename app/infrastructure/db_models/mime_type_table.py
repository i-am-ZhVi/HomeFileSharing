from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.db_models.base_table import Base

if TYPE_CHECKING:
    from app.infrastructure.db_models.category_table import Category
    from app.infrastructure.db_models.extension_table import Extension


class MimeType(Base):
    id: Mapped[int] = mapped_column(nullable=False, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id", ondelete="CASCADE"), nullable=False)

    category: Mapped["Category"] = relationship(
        back_populates="mime_types"
    )

    extensions: Mapped[list["Extension"]] = relationship(
        back_populates="mime_type", cascade="all, delete-orphan", passive_deletes=True
    )
