from pathlib import Path
from uuid import UUID
import aiofiles
from fastapi import UploadFile

from core.config import settings


class FileManager:
    async def save_file_to_directory(self, file: UploadFile, version_uuid: UUID, upload_dir: str):
        file_name = ""
        if file.filename and not settings.FILE_CRYPT:
            name = Path(file.filename).name
            extension = Path(file.filename).suffix
            file_name += name + "-" + str(version_uuid) + extension
        else: file_name = str(version_uuid)


        path = Path(upload_dir)
        path.mkdir(parents=True, exist_ok=True)

        file_path = upload_dir + "/" + file_name

        async with aiofiles.open(file_path, "wb") as buffer:
            while chunk := await file.read(65536):
                await buffer.write(chunk)

        return True

    async def find_file_path_from_directory(self, version_uuid: UUID, upload_dir: str):
        directory = Path(upload_dir)

        file_path = ""

        for find_path in directory.rglob(f"*{version_uuid}*"):
            if find_path.is_file():
                file_path = str(find_path)

        return file_path




file_manager = FileManager()
