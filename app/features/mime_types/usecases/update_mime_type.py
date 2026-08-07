from features.mime_types.repositories.interface import MimeTypeRepository
from infrastructure.db_models.mime_type_table import MimeType


class UpdateMimeTypeUseCase:
    def __init__(self, repo: MimeTypeRepository):
        self.repo = repo

    async def execute(self, mime_type_id: int, name: str | None, category_id: int | None) -> MimeType | None:
        return await self.repo.update(mime_type_id=mime_type_id, name=name, category_id=category_id)
