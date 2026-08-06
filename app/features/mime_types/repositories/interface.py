from abc import ABC, abstractmethod

from app.infrastructure.db_models.mime_type_table import MimeType


class MimeTypeRepository(ABC):
    @abstractmethod
    async def get(self, mime_type_id: int | None, sub_name: str | None, category_id: int | None) -> MimeType | list[MimeType] | None:
        pass

    @abstractmethod
    async def create(self, name: str, category_id: int) -> MimeType | None:
        pass

    @abstractmethod
    async def update(self, mime_type_id: int, name: str | None, category_id: int | None) -> MimeType | None:
        pass
