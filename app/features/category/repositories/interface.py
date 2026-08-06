from abc import ABC, abstractmethod

from app.infrastructure.db_models.category_table import Category


class CategoryRepository(ABC):
    @abstractmethod
    async def get(self, category_id: int | None, sub_name: str | None, mime_type_id: int | None) -> Category | list[Category] | None:
        pass

    @abstractmethod
    async def create(self, category_name: str) -> Category | None:
        pass

    @abstractmethod
    async def update(self, category_id: int, category_name: str) -> Category | None:
        pass
