from app.features.file_versions.repositories.interface import FileVersionRepository
from app.infrastructure.db_models.file_version_table import FileVersion


class UpdateFileVersionUseCase:
    def __init__(self, repo: FileVersionRepository):
        self.repo = repo

    async def execute(self, version_uuid: str, file_id: int | None, version: str | None, bytes: int | None, checksum: str | None) -> FileVersion | list[FileVersion] | None:
        return await self.repo.update(version_uuid=version_uuid, file_id=file_id, version=version, bytes=bytes, checksum=checksum)
