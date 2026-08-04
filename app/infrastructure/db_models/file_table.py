
from sqlalchemy.orm import Mapped, mapped_column
from infrastructure.db_models.base_table import Base


class File(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
