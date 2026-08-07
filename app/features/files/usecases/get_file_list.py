
from features.files.repositories.interface import FileRepository
from infrastructure.db_models.file_table import File


class GetFileListUseCase:
    def __init__(self, repo: FileRepository):
        self.repo = repo

    async def execute(self, sub_name: str | None, extension_id: int | None, mime_type_id: int | None) -> list[File]:
        return await self.repo.get_list(sub_name=sub_name, extension_id=extension_id, mime_type_id=mime_type_id)
