
from datetime import datetime, tzinfo
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import text
from infrastructure.db_models.base_table import Base


class File(Base):
    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    extension: Mapped[str] = mapped_column(nullable=True)
    mime_type: Mapped[str] = mapped_column(nullable=True)
    category: Mapped[str] = mapped_column(nullable=False, default="other", server_default="other")
    uploader_name: Mapped[str] = mapped_column(nullable=False, default="anonimous", server_default="anonimous")
    password_hash: Mapped[str] = mapped_column(nullable=True)
    upload_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now(), server_default=text("TIMEZONE('utc', now())"))
