from app.features.extension.repositories.interface import ExtensionRepository
from app.infrastructure.db_models.extension_table import Extension


class GetExtensionListUseCase:
    def __init__(self, repo: ExtensionRepository):
        self.repo = repo

    async def execute(self, sub_name: str | None) -> list[Extension]:
        return await self.repo.get_list(sub_name=sub_name)
