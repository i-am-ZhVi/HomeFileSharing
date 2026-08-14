from features.mime_types.repositories.interface import MimeTypeRepository
from infrastructure.db_models.mime_type_table import MimeType


class GetMimeTypeListUseCase:
    def __init__(self, repo: MimeTypeRepository):
        self.repo = repo

    async def execute(self, sub_name: str | None, extension_id: int | None, category_id: int | None) -> list[MimeType]:
        return await self.repo.get_list(sub_name=sub_name, extension_id=extension_id, category_id=category_id)
