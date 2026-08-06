from app.features.file_versions.repositories.interface import FileVersionRepository
from app.infrastructure.db_models.file_version_table import FileVersion


class GetFileVersionUseCase:
    def __init__(self, repo: FileVersionRepository):
        self.repo = repo

    async def execute(self, version_id: str | None, file_id: int | None) -> FileVersion | list[FileVersion] | None:
        return await self.repo.get(version_id=version_id, file_id=file_id)
