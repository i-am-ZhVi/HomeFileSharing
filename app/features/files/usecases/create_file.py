
from features.files.repositories.interface import FileRepository
from infrastructure.db_models.file_table import File


class CreateFileUseCase:
    def __init__(self, repo: FileRepository):
        self.repo = repo

    async def execute(self, name: str, extension_id: int, mime_type_id: int, password_hash: str | None) -> File | list[File] | None:
        return await self.repo.create(name=name, extension_id=extension_id, mime_type_id=mime_type_id, password_hash=password_hash)
