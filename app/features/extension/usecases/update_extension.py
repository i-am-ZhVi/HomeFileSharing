from app.features.extension.repositories.interface import ExtensionRepository
from app.infrastructure.db_models.extension_table import Extension


class UpdateExtensionUseCase:
    def __init__(self, repo: ExtensionRepository):
        self.repo = repo

    async def execute(self, extension_id: int, extension_name: str) -> Extension | None:
        return await self.repo.update(extension_id=extension_id, extension_name=extension_name)
