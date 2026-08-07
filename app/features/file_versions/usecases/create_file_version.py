import hashlib
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from core.config import settings
from core.file_manager import file_manager
from features.file_versions.repositories.interface import FileVersionRepository
from infrastructure.db_models.file_version_table import FileVersion


class CreateFileVersionUseCase:
    def __init__(self, repo: FileVersionRepository):
        self.repo = repo

    async def execute(self, file_id: int, version: str | None, file: UploadFile, category_name: str) -> FileVersion | None:
        version_uuid = uuid4()

        if not await file_manager.save_file_to_directory(file=file, version_uuid=version_uuid, upload_dir=settings.UPLOAD_DIRECTORY + "/" + category_name):
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="file not saved")

        bytes = file.size

        hasher = hashlib.sha256()
        while chunk := await file.read(65536):
            hasher.update(chunk)

        return await self.repo.create(version_uuid=version_uuid, file_id=file_id, version=version, bytes=bytes if bytes else 0, checksum=hasher.hexdigest())
