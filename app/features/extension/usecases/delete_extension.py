from pathlib import Path
from core.config import settings
from core.logger import logger
from features.extension.repositories.interface import ExtensionRepository
from infrastructure.db_models.extension_table import Extension


class DeleteExtensionUseCase:
    def __init__(self, repo: ExtensionRepository):
        self.repo = repo

    async def execute(self, id: int, name: str, dir_name: str) -> bool:

        directory = settings.UPLOAD_DIRECTORY / Path(dir_name)

        if not directory.exists():
            logger.error(f"Folder '{dir_name}' not exists.")
            return await self.repo.delete(id=id)

        ext = name if name.startswith('.') else f'.{name}'

        search_pattern = f"*{ext}"
        files_deleted = 0

        for file_path in directory.rglob(search_pattern):
            if file_path.is_file():
                try:
                    logger.info(f"Deleting file: {file_path}")
                    file_path.unlink()
                    files_deleted += 1
                except Exception as e:
                    logger.error(f"File delete error {file_path}: {e}")

        logger.info(f"Files deleted: {files_deleted}")


        return await self.repo.delete(id=id)
