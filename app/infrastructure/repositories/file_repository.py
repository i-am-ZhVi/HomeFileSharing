

from abc import ABC, abstractmethod
from typing import Optional

from app.infrastructure.db_models.file_table import File


class FileRepository(ABC):
    @abstractmethod
    async def get(self, file_id: Optional[int]) -> Optional[File | list[File]]:
        pass

    @abstractmethod
    async def create(self, name: str, extension: Optional[str], mime_type: Optional[str], category: str, password_hash: Optional[str]) -> Optional[File]:
        pass

    @abstractmethod
    async def update(self, file_id: int, name: str, extension: Optional[str], mime_type: Optional[str], category: str, password_hash: Optional[str]) -> Optional[File]:
        pass
