
from datetime import datetime
import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text
from infrastructure.db_models.base_table import Base


class FileVersion(Base):
    id: Mapped[uuid.UUID] = mapped_column(nullable=False, primary_key=True)
    file_id: Mapped[int] = mapped_column(ForeignKey("file.id", ondelete="CASCADE"), nullable=False)
    version: Mapped[str] = mapped_column(nullable=True)
    bytes: Mapped[int] = mapped_column(nullable=False)
    checksum: Mapped[str] = mapped_column(nullable=False)

    file: Mapped["File"] = relationship(back_populates="versions")
