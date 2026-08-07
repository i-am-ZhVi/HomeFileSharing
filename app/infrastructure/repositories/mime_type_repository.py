from sqlalchemy import desc, select, true
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from core.logger import logger
from features.mime_types.repositories.interface import MimeTypeRepository
from infrastructure.db_models.category_table import Category
from infrastructure.db_models.mime_type_table import MimeType


class SQLAlchemyMimeTypeRepository(MimeTypeRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> MimeType | None:
        logger.debug(
            "MimeType repository: get mime type by id. Params: "
            f"id={id}."
        )
        try:
            response = await self.session.execute(select(MimeType).where(MimeType.id == id))
            result = response.scalar_one_or_none()

            if result:
                logger.info(f"MimeType repository: found id={result.id}.")
            else:
                logger.warning(f"MimeType repository: id={id} not found.")

            return result

        except SQLAlchemyError:
            logger.exception("MimeType repository: database error coccurred during get operation workflow.")
            raise

    async def get_list(self, sub_name: str | None, category_id: int | None) -> list[MimeType]:
        logger.debug(
            "MimeType repository: get mime types. Params: "
            f"sub_name={sub_name}, category_id={category_id}."
        )
        try:
            query = select(MimeType).options(selectinload(MimeType.files), selectinload(MimeType.category)).order_by(desc(MimeType.created_at), desc(MimeType.id))

            if sub_name:
                query = query.where(MimeType.name.contains(sub_name))

            if category_id:
                query = query.join(MimeType.category).where(Category.id == category_id)

            response = await self.session.execute(query)

            result = list(response.scalars().all())

            logger.info(f"MimeType repository: found {len(result)} mime_types matching filters.")

            return result

        except SQLAlchemyError:
            logger.exception("MimeType repository: database error coccurred during get operation workflow.")
            raise

    async def create(self, name: str, category_id: int) -> MimeType | None:
        logger.debug(
            "MimeType repository: create mime type. Params: "
            f"name={name}, category_id={category_id}."
        )
        try:
            mime_type = MimeType(name=name, category_id=category_id)

            self.session.add(mime_type)
            await self.session.commit()
            await self.session.refresh(mime_type)

            logger.info(f"MimeType repository: created mime type by id={mime_type.id}")

            return mime_type
        except SQLAlchemyError:
            logger.exception("MimeType repository: database error occurred during create operation workflow.")
            raise

    async def update(self, mime_type_id: int, name: str | None, category_id: int | None) -> MimeType | None:
        logger.debug(
            "MimeType repository: update MimeType. Params: "
            f"mime_type_id={mime_type_id}, name={name}, category_id={category_id}."
        )
        try:
            response = await self.session.execute(select(MimeType).where(MimeType.id == mime_type_id))

            mime_type = response.scalar_one_or_none()
            if not mime_type:
                logger.warning(f"MimeType repository: mime type id={mime_type_id} not found")
                return None

            if name: mime_type.name = name
            if category_id: mime_type.category_id = category_id

            await self.session.commit()
            await self.session.refresh(mime_type)

            logger.info(f"MimeType repository: update mime type by id={mime_type.id}")

            return mime_type

        except SQLAlchemyError:
            logger.exception("MimeType repository: database error occurred during update operation workflow.")
            raise
