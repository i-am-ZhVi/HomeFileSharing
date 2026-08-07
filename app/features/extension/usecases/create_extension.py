from features.extension.repositories.interface import ExtensionRepository
from infrastructure.db_models.extension_table import Extension


class CreateExtensionUseCase:
    def __init__(self, repo: ExtensionRepository):
        self.repo = repo

    async def execute(self, name: str) -> Extension | None:
        return await self.repo.create(extension_name=name)
