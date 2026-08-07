import aiofiles
from fastapi import UploadFile


class FileManager:
    async def save_file_to_directory(self, file: UploadFile, file_name: str, upload_dir: str):
        file_path = upload_dir + "/" + file_name

        async with aiofiles.open(file_path, "wb") as buffer:
            while chunk := await file.read(65536):
                await buffer.write(chunk)

        return True


file_manager = FileManager()
