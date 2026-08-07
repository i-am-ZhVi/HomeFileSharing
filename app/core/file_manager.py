from pathlib import Path
from uuid import UUID
import aiofiles
from fastapi import UploadFile


class FileManager:
    async def save_file_to_directory(self, file: UploadFile, version_uuid: UUID, upload_dir: str):
        file_name = ""
        if file.filename:
            name = Path(file.filename).name
            extension = Path(file.filename).suffix
            file_name += name + str(version_uuid) + extension
        else: file_name = str(version_uuid)

        path = Path(upload_dir)
        path.mkdir(parents=True, exist_ok=True)

        file_path = upload_dir + "/" + file_name

        async with aiofiles.open(file_path, "wb") as buffer:
            while chunk := await file.read(65536):
                await buffer.write(chunk)

        return True


file_manager = FileManager()
