from pathlib import Path
from infrastructure.db_models.file_version_table import FileVersion
from core.config import settings
from core.logger import logger
from features.extension.repositories.interface import ExtensionRepository
from infrastructure.db_models.extension_table import Extension


class DeleteExtensionUseCase:
    def __init__(self, repo: ExtensionRepository):
        self.repo = repo

    async def execute(self, id: int, versions: list[FileVersion], dir_name: str) -> bool:

        directory = settings.UPLOAD_DIRECTORY / Path(dir_name)

        if not directory.exists():
            logger.error(f"Folder '{dir_name}' not exists.")
            return await self.repo.delete(id)

        for version in versions:
            search_pattern = f"*{version.id}*"
            files_deleted = 0

            for file_path in directory.rglob(search_pattern):
                if file_path.is_file():
                    try:
                        logger.info(f"Deleting file: {file_path}")
                        file_path.unlink()
                        files_deleted += 1
                    except Exception as e:
                        logger.error(f"File delete error {file_path}: {e}")

        return await self.repo.delete(id=id)
