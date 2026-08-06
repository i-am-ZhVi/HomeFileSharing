from sqlalchemy import select, true
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.logger import logger
from app.features.extension.repositories.interface import ExtensionRepository
from app.infrastructure.db_models.extension_table import Extension


class SQLAlchemyExtensionRepository(ExtensionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, extension_id: int | None, sub_name: str | None) -> Extension | list[Extension] | None:
        logger.debug(
            "Extension repository: get extensions. Params: "
            f"extension_id={extension_id}, sub_name={sub_name}."
        )
        try:
            if extension_id:
                response = await self.session.execute(select(Extension).where(Extension.id == extension_id))
                result = response.scalar_one_or_none()

                if result:
                    logger.info(f"Extension repository: found extension_id={result.id}.")
                else:
                    logger.warning(f"Extension repository: extension_id={extension_id} not found.")

                return result

            response = await self.session.execute(select(Extension).options(selectinload(Extension.files))
                .where(Extension.name.contains(sub_name) if sub_name else true()))

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
            response = await self.session.execute(select(Extension).where(Extension.id == extension_id))

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
