from pathlib import Path
from core.config import settings
from core.logger import logger
from infrastructure.db_models.file_version_table import FileVersion
from features.mime_types.repositories.interface import MimeTypeRepository
from infrastructure.db_models.mime_type_table import MimeType


class DeleteMimeTypeUseCase:
    def __init__(self, repo: MimeTypeRepository):
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
