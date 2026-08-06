from app.features.mime_types.repositories.interface import MimeTypeRepository
from app.infrastructure.db_models.mime_type_table import MimeType


class CreateMimeTypeUseCase:
    def __init__(self, repo: MimeTypeRepository):
        self.repo = repo

    async def execute(self, name: str, category_id: int) -> MimeType | None:
        return await self.repo.create(name=name, category_id=category_id)
