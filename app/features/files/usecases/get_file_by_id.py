
from app.features.files.repositories.interface import FileRepository
from app.infrastructure.db_models.file_table import File


class GetFileByIdUseCase:
    def __init__(self, repo: FileRepository):
        self.repo = repo

    async def execute(self, id: int) -> File | None:
        return await self.repo.get_by_id(id=id)
