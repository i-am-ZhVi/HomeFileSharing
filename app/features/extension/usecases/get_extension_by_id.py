from features.extension.repositories.interface import ExtensionRepository
from infrastructure.db_models.extension_table import Extension


class GetExtensionByIdUseCase:
    def __init__(self, repo: ExtensionRepository):
        self.repo = repo

    async def execute(self, id: int) -> Extension | None:
        return await self.repo.get_by_id(id=id)
