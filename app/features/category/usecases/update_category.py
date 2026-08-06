from app.features.category.repositories.interface import CategoryRepository
from app.infrastructure.db_models.category_table import Category


class GetCategoryUseCase:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def execute(self, category_id: int, name: str) -> Category | None:
        return await self.repo.update(category_id=category_id, category_name=name)
