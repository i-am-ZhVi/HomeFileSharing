from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db_models.base_table import Base


class Extension(Base):
    id: Mapped[int] = mapped_column(nullable=False, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    files: Mapped[list["File"]] = relationship(
        back_populates="extension", cascade="all, delete-orphan", passive_deletes=True
    )
