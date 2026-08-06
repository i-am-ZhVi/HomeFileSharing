from app.features.mime_types.repositories.interface import MimeTypeRepository
from app.infrastructure.db_models.mime_type_table import MimeType


class GetMimeTypeUseCase:
    def __init__(self, repo: MimeTypeRepository):
        self.repo = repo

    async def execute(self, mime_type_id: int | None, sub_name: str | None, category_id: int | None) -> MimeType | list[MimeType] | None:
        return await self.repo.get(mime_type_id=mime_type_id, sub_name=sub_name, category_id=category_id)
