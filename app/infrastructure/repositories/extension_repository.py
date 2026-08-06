from sqlalchemy import desc, select, true
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.logger import logger
from app.features.extension.repositories.interface import ExtensionRepository
from app.infrastructure.db_models.extension_table import Extension


class SQLAlchemyExtensionRepository(ExtensionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> Extension | None:
        logger.debug(
            "Extension repository: get extension by id. Params: "
            f"id={id}."
        )
        try:
            response = await self.session.execute(select(Extension).where(Extension.id == id).options(selectinload(Extension.files)))
            result = response.scalar_one_or_none()

            if result:
                logger.info(f"Extension repository: found id={result.id}.")
            else:
                logger.warning(f"Extension repository: id={id} not found.")

            return result
        except SQLAlchemyError:
            logger.exception("Extension repository: database error coccurred during get operation workflow.")
            raise

    async def get_list(self, sub_name: str | None) -> list[Extension]:
        logger.debug(
            "Extension repository: get list extensions. Params: "
            f"sub_name={sub_name}."
        )
        try:
            query = select(Extension).options(selectinload(Extension.files)).order_by(desc(Extension.created_at), desc(Extension.id))

            if sub_name:
                query = query.where(Extension.name.contains(sub_name))

            response = await self.session.execute(query)
            result = list(response.scalars().all())

            logger.info(f"Extension repository: found {len(result)} extensions matching filters.")
            return result

        except SQLAlchemyError:
            logger.exception("Extension repository: database error coccurred during get operation workflow.")
            raise

    async def create(self, extension_name: str) -> Extension | None:
        logger.debug(
            "Extension repository: create extension. Params: "
            f"extension_name={extension_name}."
        )
        try:
            extension = Extension(name=extension_name)

            self.session.add(extension)
            await self.session.commit()
            await self.session.refresh(extension)

            logger.info(f"Extension repository: created extension by id={extension.id}")

            return extension
        except SQLAlchemyError:
            logger.exception("Extension repository: database error occurred during create operation workflow.")
            raise

    async def update(self, extension_id: int, extension_name: str) -> Extension | None:
        logger.debug(
            "Extension repository: update extension. Params: "
            f"extension_id={extension_id}, extension_name={extension_name}."
        )
        try:
            response = await self.session.execute(select(Extension).where(Extension.id == extension_id).options(selectinload(Extension.files)))

            extension = response.scalar_one_or_none()
            if not extension:
                logger.warning(f"Extension repository: extension_id={extension_id} not found")
                return None

            extension.name = extension_name

            await self.session.commit()
            await self.session.refresh(extension)

            logger.info(f"Extension repository: update extension by id={extension.id}")

            return extension

        except SQLAlchemyError:
            logger.exception("Extension repository: database error occurred during update operation workflow.")
            raise
