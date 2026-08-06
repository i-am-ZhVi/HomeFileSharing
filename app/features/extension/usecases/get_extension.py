from app.features.extension.repositories.interface import ExtensionRepository
from app.infrastructure.db_models.extension_table import Extension


class GetExtensionUseCase:
    def __init__(self, repo: ExtensionRepository):
        self.repo = repo

    async def execute(self, extension_id: int | None, sub_name: str | None) -> Extension | list[Extension] | None:
        return await self.repo.get(extension_id=extension_id, sub_name=sub_name)
