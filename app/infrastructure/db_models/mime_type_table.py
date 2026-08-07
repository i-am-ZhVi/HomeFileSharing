from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.db_models.base_table import Base


class MimeType(Base):
    id: Mapped[int] = mapped_column(nullable=False, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=False)

    category: Mapped["Category"] = relationship(
        back_populates="mime_types"
    )

    extensions: Mapped[list["Extension"]] = relationship(
        back_populates="mime_type", cascade="all, delete-orphan", passive_deletes=True
    )
