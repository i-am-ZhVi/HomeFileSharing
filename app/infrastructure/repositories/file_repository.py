

from abc import ABC, abstractmethod
from typing import Optional

from app.features.files.repositories.interface import FileRepository
from app.infrastructure.db_models.file_table import File


class SQLAlchemyFileRepository(FileRepository):
    async def get(self, file_id: Optional[int], sub_name: Optional[str], extention_id: Optional[int], mime_type: Optional[str], category_id: Optional[int]) -> Optional[File | list[File]]:
        pass


    async def create(self, name: str, extension_id: Optional[int], mime_type: Optional[str], category_id: int, password_hash: Optional[str]) -> Optional[File]:
        pass


    async def update(self, file_id: int, name: str, extension_id: Optional[int], mime_type: Optional[str], category_id: int, password_hash: Optional[str]) -> Optional[File]:
        pass
