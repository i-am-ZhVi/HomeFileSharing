from typing import TYPE_CHECKING, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.db_models.base_table import Base

if TYPE_CHECKING:
    from app.infrastructure.db_models.mime_type_table import MimeType

class Category(Base):
    id: Mapped[int] = mapped_column(nullable=False, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)


    mime_types: Mapped[list["MimeType"]] = relationship(
        back_populates="category", cascade="all, delete-orphan", passive_deletes=True
    )
