from features.extension.repositories.interface import ExtensionRepository
from infrastructure.db_models.extension_table import Extension


class UpdateExtensionUseCase:
    def __init__(self, repo: ExtensionRepository):
        self.repo = repo

    async def execute(self, extension_id: int, extension_name: str | None, mime_type_id: int | None) -> Extension | None:
        return await self.repo.update(extension_id=extension_id, extension_name=extension_name, mime_type_id=mime_type_id)
