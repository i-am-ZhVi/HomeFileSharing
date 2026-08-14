from features.category.repositories.interface import CategoryRepository
from infrastructure.db_models.category_table import Category


class GetCategoryByIdUseCase:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def execute(self, id: int) -> Category | None:
        return await self.repo.get_by_id(id=id)
