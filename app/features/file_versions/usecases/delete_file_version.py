import hashlib
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from core.logger import logger
from core.config import settings
from core.file_manager import file_manager
from features.file_versions.repositories.interface import FileVersionRepository
from infrastructure.db_models.file_version_table import FileVersion


class DeleteFileVersionUseCase:
    def __init__(self, repo: FileVersionRepository):
        self.repo = repo

    async def execute(self, version_uuid: str, dir_name: str) -> bool:
        directory = settings.UPLOAD_DIRECTORY / Path(dir_name)

        if not directory.exists():
            logger.error(f"Folder '{dir_name}' not exists.")
            return await self.repo.delete(version_uuid)

        search_pattern = f"*{version_uuid}*"
        files_deleted = 0

        for file_path in directory.rglob(search_pattern):
            if file_path.is_file():
                try:
                    logger.info(f"Deleting file: {file_path}")
                    file_path.unlink()
                    files_deleted += 1
                except Exception as e:
                    logger.error(f"File delete error {file_path}: {e}")

        return await self.repo.delete(version_uuid)
