from abc import ABC, abstractmethod

from app.infrastructure.db_models.file_version_table import FileVersion


class FileVersionRepository(ABC):
    @abstractmethod
    async def get(self, version_id: str | None, file_id: int | None) -> FileVersion | list[FileVersion] | None:
        pass

    @abstractmethod
    async def create(self, version_uuid: str, file_id: int, version: str | None, bytes: int, checksum: str) -> FileVersion | None:
        pass

    @abstractmethod
    async def update(self, version_uuid: str, file_id: int | None, version: str | None, bytes: int | None, checksum: str | None) -> FileVersion | None:
        pass
