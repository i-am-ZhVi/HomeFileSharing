from sqlalchemy import desc, select, true
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.logger import logger
from app.features.category.repositories.interface import CategoryRepository
from app.infrastructure.db_models.category_table import Category
from app.infrastructure.db_models.mime_type_table import MimeType


class SQLAlchemyCategoryRepository(CategoryRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> Category | None:
        logger.debug(
            "Category repository: get category by id. Params: "
            f"id={id}."
        )
        try:
            response = await self.session.execute(select(Category).where(Category.id == id).options(selectinload(Category.mime_types), selectinload(Category.files)))
            result = response.scalar_one_or_none()

            if result:
                logger.info(f"Category repository: found id={result.id}.")
            else:
                logger.warning(f"Category repository: id={id} not found.")

            return result
        except SQLAlchemyError:
            logger.exception("Category repository: database error coccurred during get operation workflow.")
            raise

    async def get_list(self, sub_name: str | None, mime_type_id: int | None) -> list[Category]:
        logger.debug(
            "Category repository: get list categories. Params: "
            f"sub_name={sub_name}, mime_type_id={mime_type_id}."
        )
        try:
            query = select(Category).options(selectinload(Category.mime_types), selectinload(Category.files)).order_by(desc(Category.created_at), desc(Category.id))

            if sub_name:
                query = query.where(Category.name.contains(sub_name))

            if mime_type_id:
                query = query.join(Category.mime_types).where(MimeType.id == mime_type_id)

            response = await self.session.execute(query)
            result = list(response.scalars().all())

            logger.info(f"Category repository: found {len(result)} categories matching filters.")
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
            response = await self.session.execute(select(Category).where(Category.id == category_id).options(selectinload(Category.mime_types), selectinload(Category.files)))

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
