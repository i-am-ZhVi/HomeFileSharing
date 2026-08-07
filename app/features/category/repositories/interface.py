from abc import ABC, abstractmethod

from infrastructure.db_models.category_table import Category


class CategoryRepository(ABC):

    @abstractmethod
    async def get_by_id(self, id: int) -> Category | None:
        pass

    @abstractmethod
    async def get_list(self, sub_name: str | None, mime_type_id: int | None) -> list[Category]:
        pass

    @abstractmethod
    async def create(self, category_name: str) -> Category | None:
        pass

    @abstractmethod
    async def update(self, category_id: int, category_name: str) -> Category | None:
        pass
