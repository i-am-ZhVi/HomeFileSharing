from abc import ABC, abstractmethod

from app.infrastructure.db_models.extension_table import Extension


class ExtensionRepository(ABC):
    @abstractmethod
    async def get(self, extension_id: int | None, sub_name: str | None) -> Extension | list[Extension] | None:
        pass

    @abstractmethod
    async def create(self, extension_name: str) -> Extension | None:
        pass

    @abstractmethod
    async def update(self, extension_id: int, extension_name: str) -> Extension | None:
        pass
