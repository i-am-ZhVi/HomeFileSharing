
from features.files.repositories.interface import FileRepository
from infrastructure.db_models.file_table import File


class UpdateFileUseCase:
    def __init__(self, repo: FileRepository):
        self.repo = repo

    async def execute(self, file_id: int, name: str | None, extension_id: int | None, mime_type_id: int | None, password_hash: str | None) -> File | None:
        return await self.repo.update(file_id=file_id, name=name, extension_id=extension_id, mime_type_id=mime_type_id, password_hash=password_hash)
