from datetime import datetime
import re
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column
from sqlalchemy.sql import text

class Base(DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now(), server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now(), server_default=text("TIMEZONE('utc', now())"))

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()
