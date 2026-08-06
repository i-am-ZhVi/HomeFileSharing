from app.features.category.repositories.interface import CategoryRepository
from app.infrastructure.db_models.category_table import Category


class GetCategoryUseCase:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def execute(self, category_id: int | None, sub_name: str | None, mime_type_id: int | None) -> Category | list[Category] | None:
        return await self.repo.get(category_id=category_id, sub_name=sub_name, mime_type_id=mime_type_id)
