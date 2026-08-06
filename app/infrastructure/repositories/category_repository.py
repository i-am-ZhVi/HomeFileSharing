from sqlalchemy import select, true
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.logger import logger
from app.features.category.repositories.interface import CategoryRepository
from app.infrastructure.db_models.category_table import Category


class SQLAlchemyCategoryRepository(CategoryRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, category_id: int | None, sub_name: str | None, mime_type_id: int | None) -> Category | list[Category] | None:
        logger.debug(
            "Category repository: get categories. Params: "
            f"category_id={category_id}, sub_name={sub_name}, mime_type_id={mime_type_id}."
        )
        try:
            if category_id:
                response = await self.session.execute(select(Category).where(Category.id == category_id))
                result = response.scalar_one_or_none()

                if result:
                    logger.info(f"Category repository: found category_id={result.id}.")
                else:
                    logger.warning(f"Category repository: category_id={category_id} not found.")

                return result

            response = await self.session.execute(select(Category).options(selectinload(Category.mime_types))
                .where(Category.name.contains(sub_name) if sub_name else true()))

            response_list = list(response.scalars().all())

            result = []

            if mime_type_id:
                for category in response_list:
                    for mime_type in category.mime_types:
                        if mime_type.id == mime_type_id:
                            result.append(category)
                            break

            else: result = response_list

            logger.info(f"Category repository: found {len(result)} files matching filters.")

            return result

        except SQLAlchemyError:
            logger.exception("Category repository: database error coccurred during get operation workflow.")
            raise

    async def create(self, category_name: str) -> Category | None:
        logger.debug(
            "Category repository: create category. Params: "
            f"category_name={category_name}."
        )
        try:
            category = Category(name=category_name)

            self.session.add(category)
            await self.session.commit()
            await self.session.refresh(category)

            logger.info(f"Category repository: created category by id={category.id}")

            return category
        except SQLAlchemyError:
            logger.exception("Category repository: database error occurred during create operation workflow.")
            raise

    async def update(self, category_id: int, category_name: str) -> Category | None:
        logger.debug(
            "Category repository: update category. Params: "
            f"category_id={category_id}, category_name={category_name}."
        )
        try:
            response = await self.session.execute(select(Category).where(Category.id == category_id))

            category = response.scalar_one_or_none()
            if not category:
                logger.warning(f"Category repository: category_id={category_id} not found")
                return None

            category.name = category_name

            await self.session.commit()
            await self.session.refresh(category)

            logger.info(f"Category repository: update category by id={category.id}")

            return category

        except SQLAlchemyError:
            logger.exception("Category repository: database error occurred during update operation workflow.")
            raise
