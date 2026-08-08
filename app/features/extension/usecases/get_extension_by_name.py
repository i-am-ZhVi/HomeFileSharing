from features.extension.repositories.interface import ExtensionRepository
from infrastructure.db_models.extension_table import Extension


class GetExtensionByNameUseCase:
    def __init__(self, repo: ExtensionRepository):
        self.repo = repo

    async def execute(self, name: str) -> Extension | None:
        return await self.repo.get_by_name(name=name)
