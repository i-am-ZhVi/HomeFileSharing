from features.mime_types.repositories.interface import MimeTypeRepository
from infrastructure.db_models.mime_type_table import MimeType


class GetMimeTypeByNameUseCase:
    def __init__(self, repo: MimeTypeRepository):
        self.repo = repo

    async def execute(self, name: str) -> MimeType | None:
        return await self.repo.get_by_name(name=name)
