from sqlalchemy import delete, desc, select, true
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from infrastructure.db_models.file_table import File
from infrastructure.db_models.mime_type_table import MimeType
from core.logger import logger
from features.extension.repositories.interface import ExtensionRepository
from infrastructure.db_models.extension_table import Extension


class SQLAlchemyExtensionRepository(ExtensionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> Extension | None:
        logger.debug(
            "Extension repository: get extension by id. Params: "
            f"id={id}."
        )
        try:
            response = await self.session.execute(select(Extension).where(Extension.id == id).options(
                selectinload(Extension.files).selectinload(File.versions), selectinload(Extension.mime_type).selectinload(MimeType.category)))
            result = response.scalar_one_or_none()

            if result:
                logger.info(f"Extension repository: found id={result.id}.")
            else:
                logger.warning(f"Extension repository: id={id} not found.")

            return result
        except SQLAlchemyError:
            logger.exception("Extension repository: database error coccurred during get operation workflow.")
            raise

    async def get_by_name(self, name: str) -> Extension | None:
        logger.debug(
            "Extension repository: get extension by name. Params: "
            f"name={name}."
        )
        try:
            response = await self.session.execute(select(Extension).where(Extension.name == name).options(
                selectinload(Extension.files).selectinload(File.versions), selectinload(Extension.mime_type).selectinload(MimeType.category)))
            result = response.scalar_one_or_none()

            if result:
                logger.info(f"Extension repository: found name={result.name}.")
            else:
                logger.warning(f"Extension repository: name={name} not found.")

            return result
        except SQLAlchemyError:
            logger.exception("Extension repository: database error coccurred during get operation workflow.")
            raise

    async def get_list(self, sub_name: str | None, mime_type_id: int | None) -> list[Extension]:
        logger.debug(
            "Extension repository: get list extensions. Params: "
            f"sub_name={sub_name}, mime_type_id={mime_type_id}."
        )
        try:
            query = select(Extension).options(
                selectinload(Extension.files).selectinload(File.versions), selectinload(Extension.mime_type).selectinload(MimeType.category)
            ).order_by(desc(Extension.created_at), desc(Extension.id))

            if sub_name:
                query = query.where(Extension.name.contains(sub_name))

            if mime_type_id:
                query = query.where(Extension.mime_type_id == mime_type_id)

            response = await self.session.execute(query)
            result = list(response.scalars().all())

            logger.info(f"Extension repository: found {len(result)} extensions matching filters.")
            return result

        except SQLAlchemyError:
            logger.exception("Extension repository: database error coccurred during get operation workflow.")
            raise

    async def create(self, extension_name: str, mime_type_id: int) -> Extension | None:
        logger.debug(
            "Extension repository: create extension. Params: "
            f"extension_name={extension_name}."
        )
        try:
            extension = Extension(name=extension_name, mime_type_id=mime_type_id)

            self.session.add(extension)
            await self.session.commit()
            await self.session.refresh(extension)

            logger.info(f"Extension repository: created extension by id={extension.id}")

            return extension
        except SQLAlchemyError:
            logger.exception("Extension repository: database error occurred during create operation workflow.")
            raise

    async def update(self, extension_id: int, extension_name: str | None, mime_type_id: int | None) -> Extension | None:
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

            if extension_name: extension.name = extension_name
            if mime_type_id: extension.mime_type_id = mime_type_id

            await self.session.commit()
            await self.session.refresh(extension)

            logger.info(f"Extension repository: update extension by id={extension.id}")

            return extension

        except SQLAlchemyError:
            logger.exception("Extension repository: database error occurred during update operation workflow.")
            raise


    async def delete(self, id: int) -> bool:
        logger.debug(
            "Extension repository: delete extension. Params: "
            f"id={id}."
        )
        try:
            await self.session.execute(delete(Extension).where(Extension.id == id))
            await self.session.commit()

            logger.info(f"Extension repository: deleted extension by id={id}")

            return True

        except SQLAlchemyError:
            logger.exception("Extension repository: database error occurred during update operation workflow.")
            raise
