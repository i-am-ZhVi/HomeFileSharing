from abc import ABC, abstractmethod
from typing import Optional

from app.infrastructure.db_models.file_table import File


class FileRepository(ABC):
    @abstractmethod
    async def get(self, file_id: int | None, sub_name: str | None, extension_id: int | None, mime_type: str | None, category_id: int | None) -> File | list[File] | None:
        pass

    @abstractmethod
    async def create(self, name: str, extension_id: int | None, mime_type_id: int | None, category_id: int, password_hash: str | None) -> File | None:
        pass

    @abstractmethod
    async def update(self, file_id: int, name: str | None, extension_id: int | None, mime_type_id: int | None, category_id: int | None, password_hash: str | None) -> File | None:
        pass
