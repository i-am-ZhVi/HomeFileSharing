from features.file_versions.repositories.interface import FileVersionRepository
from infrastructure.db_models.file_version_table import FileVersion


class GetFileVersionListUseCase:
    def __init__(self, repo: FileVersionRepository):
        self.repo = repo

    async def execute(self, file_id: int | None) -> list[FileVersion]:
        return await self.repo.get_list(file_id=file_id)
