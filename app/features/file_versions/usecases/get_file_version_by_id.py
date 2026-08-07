from app.features.file_versions.repositories.interface import FileVersionRepository
from app.infrastructure.db_models.file_version_table import FileVersion


class GetFileVersionByIdUseCase:
    def __init__(self, repo: FileVersionRepository):
        self.repo = repo

    async def execute(self, id: str) -> FileVersion | list[FileVersion] | None:
        return await self.repo.get_by_id(id=id)
