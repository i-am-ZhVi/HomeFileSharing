from features.mime_types.repositories.interface import MimeTypeRepository
from infrastructure.db_models.mime_type_table import MimeType


class GetMimeTypeByIdUseCase:
    def __init__(self, repo: MimeTypeRepository):
        self.repo = repo

    async def execute(self, id: int) -> MimeType | None:
        return await self.repo.get_by_id(id=id)
