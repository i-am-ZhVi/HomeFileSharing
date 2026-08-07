from abc import ABC, abstractmethod

from infrastructure.db_models.extension_table import Extension


class ExtensionRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> Extension | None:
        pass

    @abstractmethod
    async def get_list(self, sub_name: str | None, mime_type_id: int | None) -> list[Extension]:
        pass

    @abstractmethod
    async def create(self, extension_name: str, mime_type_id: int) -> Extension | None:
        pass

    @abstractmethod
    async def update(self, extension_id: int, extension_name: str | None, mime_type_id: int | None) -> Extension | None:
        pass
