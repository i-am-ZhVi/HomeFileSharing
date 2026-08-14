from features.category.repositories.interface import CategoryRepository
from infrastructure.db_models.category_table import Category


class GetCategoryByNameUseCase:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def execute(self, name: str) -> Category | None:
        return await self.repo.get_by_name(name=name)
