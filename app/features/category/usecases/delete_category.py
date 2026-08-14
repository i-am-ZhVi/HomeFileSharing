import os
from pathlib import Path
import shutil
from core.logger import logger
from core.config import settings
from features.category.repositories.interface import CategoryRepository
from infrastructure.db_models.category_table import Category


class DeleteCategoryUseCase:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def execute(self, id: int, name: str) -> bool:
        folder_path = settings.UPLOAD_DIRECTORY + "/" + name
        if not os.path.exists(folder_path):
            logger.error(f"Delete category usecase: folder {folder_path} not exist.")
            return False


        try:
            shutil.rmtree(folder_path)

            if not os.path.exists(folder_path):
                logger.info(f"Folder {folder_path} and all files was deleted.")
            else:
                logger.error(f"Process end, but folder {folder_path} still exists.")
                return False

        except Exception as e:
            logger.critical(f"Critical error upon deletion folder {folder_path}: {e}")
            return False

        return await self.repo.delete(id=id)
