from pathlib import Path
from core.config import settings
from features.category.repositories.interface import CategoryRepository
from infrastructure.db_models.category_table import Category


class CreateCategoryUseCase:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def execute(self, name: str) -> Category | None:
        path = Path(settings.UPLOAD_DIRECTORY + "/" + name)
        path.mkdir(parents=True, exist_ok=True)
        return await self.repo.create(category_name=name)
