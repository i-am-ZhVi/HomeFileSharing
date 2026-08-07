from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import and_, desc, insert, or_, select, true
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from infrastructure.db_models.extension_table import Extension
from infrastructure.db_models.mime_type_table import MimeType
from core.logger import logger
from features.files.repositories.interface import FileRepository
from infrastructure.db_models.file_table import File


class SQLAlchemyFileRepository(FileRepository):
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_by_id(self, id: int) -> File | None:
        logger.debug(
            "File repository: get files. Params: "
            f"file_id={id}."
        )
        try:
            response = await self.session.execute(select(File)
                .where(File.id == id)
                .options(
                    selectinload(File.extension).selectinload(Extension.mime_type).selectinload(MimeType.category),
                    selectinload(File.versions),))

            result = response.scalar_one_or_none()

            if result:
                logger.info(f"File repository: found id={result.id}.")
            else:
                logger.warning(f"File repository: id={id} not found.")

            return result
        except SQLAlchemyError:
            logger.exception("File repository: database error occurred during get operational workflow.")
            raise

    async def get_list(self, sub_name: str | None, extension_id: int | None) -> list[File]:
        logger.debug(
            "File repository: get files. Params: "
            f"sub_name={sub_name}, extension_id={extension_id}.",
        )
        try:
            query = select(File).options(
                selectinload(File.extension).selectinload(Extension.mime_type).selectinload(MimeType.category),
                selectinload(File.versions),
            ).order_by(desc(File.created_at), desc(File.id))

            filters = []

            if sub_name:
                filters.append(File.name.contains(sub_name))

            if extension_id:
                filters.append(File.extension_id == extension_id)

            query = query.where(and_(*filters))

            response = await self.session.execute(query)

            result = list(response.scalars().all())
            logger.info(f"File repository: found {len(result)} files matching filters.")
            return result
        except SQLAlchemyError:
            logger.exception("File repository: database error occurred during get operational workflow.")
            raise


    async def create(self, name: str, extension_id: int | None, password_hash: str | None) -> File | None:
        logger.debug("File repository: create file. Params: "
            f"name={name}, extension_id={extension_id}, password_hash={password_hash}"
        )
        try:
            file = File(
                name=name,
                extension_id=extension_id,
                password_hash=password_hash
            )

            self.session.add(file)
            await self.session.commit()
            await self.session.refresh(file)

            new_file = await self.session.execute(select(File).where(File.id == file.id).options(
                selectinload(File.extension).selectinload(Extension.mime_type).selectinload(MimeType.category),
                selectinload(File.versions),
            ))

            logger.info(f"File repository: created file by id={file.id}")

            return new_file.scalar_one_or_none()
        except SQLAlchemyError:
            logger.exception("File repository: database error occurred during create operational workflow")
            raise


    async def update(self, file_id: int, name: str | None, extension_id: int | None, password_hash: str | None) -> File | None:
        logger.info(
            "File repository: update file. Params: "
            f"file_id={file_id}, name={name}, extension_id={extension_id}, password_hash={password_hash}"
        )

        try:
            response = await self.session.execute(select(File).options(
                selectinload(File.extension).selectinload(Extension.mime_type).selectinload(MimeType.category),
                selectinload(File.versions),
            ).where(File.id == file_id))
            file = response.scalar_one_or_none()

            if not file:
                logger.warning(f"File repository: file_id={file_id} not fount")
                return None

            if name: file.name = name
            if extension_id: file.extension_id = extension_id
            if password_hash: file.password_hash = password_hash

            await self.session.commit()
            await self.session.refresh(file)

            logger.info(f"File repository: update file by id={file.id}")

            return file

        except SQLAlchemyError:
            logger.exception("File repository: database error occurred during update ooperaional workflow")
            raise
