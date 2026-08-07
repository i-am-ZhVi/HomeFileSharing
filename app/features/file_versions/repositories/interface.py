from abc import ABC, abstractmethod
from uuid import UUID

from infrastructure.db_models.file_version_table import FileVersion


class FileVersionRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: str) -> FileVersion | None:
        pass

    @abstractmethod
    async def get_list(self, file_id: int | None) -> list[FileVersion]:
        pass

    @abstractmethod
    async def create(self, version_uuid: UUID, file_id: int, version: str | None, bytes: int, checksum: str) -> FileVersion | None:
        pass

    @abstractmethod
    async def update(self, version_uuid: str, file_id: int | None, version: str | None, bytes: int | None, checksum: str | None) -> FileVersion | None:
        pass
