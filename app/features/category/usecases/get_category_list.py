from app.features.category.repositories.interface import CategoryRepository
from app.infrastructure.db_models.category_table import Category


class GetCategoryListUseCase:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def execute(self, sub_name: str | None, mime_type_id: int | None) -> list[Category]:
        return await self.repo.get_list(sub_name=sub_name, mime_type_id=mime_type_id)
