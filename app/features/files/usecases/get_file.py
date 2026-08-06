
from app.features.files.repositories.interface import FileRepository
from app.infrastructure.db_models.file_table import File


class GetFileUseCase:
    def __init__(self, repo: FileRepository):
        self.repo = repo

    async def execute(self, file_id: int | None, sub_name: str | None, extension_id: int | None, mime_type_id: int | None, category_id: int | None) -> File | list[File] | None:
        return await self.repo.get(file_id=file_id, sub_name=sub_name, extension_id=extension_id, mime_type_id=mime_type_id, category_id=category_id)
