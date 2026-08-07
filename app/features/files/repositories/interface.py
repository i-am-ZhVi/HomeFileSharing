from abc import ABC, abstractmethod
from typing import Optional

from infrastructure.db_models.file_table import File


class FileRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> File | None:
        pass

    @abstractmethod
    async def get_list(self, sub_name: str | None, extension_id: int | None) -> list[File]:
        pass

    @abstractmethod
    async def create(self, name: str, extension_id: int | None, password_hash: str | None) -> File | None:
        pass

    @abstractmethod
    async def update(self, file_id: int, name: str | None, extension_id: int | None, password_hash: str | None) -> File | None:
        pass
