from abc import ABC, abstractmethod
from typing import Optional


class FileRepository(ABC):
    @abstractmethod
    async def get(self, file_id: Optional[int], sub_name: Optional[str], extention_id: Optional[int], mime_type: Optional[str], category_id: Optional[int]) -> Optional[File | list[File]]:
        pass

    @abstractmethod
    async def create(self, name: str, extension_id: Optional[int], mime_type: Optional[str], category_id: int, password_hash: Optional[str]) -> Optional[File]:
        pass

    @abstractmethod
    async def update(self, file_id: int, name: str, extension_id: Optional[int], mime_type: Optional[str], category_id: int, password_hash: Optional[str]) -> Optional[File]:
        pass
