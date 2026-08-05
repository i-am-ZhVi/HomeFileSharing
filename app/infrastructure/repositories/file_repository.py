from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import and_, insert, or_, select, true
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.logger import logger
from app.features.files.repositories.interface import FileRepository
from app.infrastructure.db_models.file_table import File


class SQLAlchemyFileRepository(FileRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, file_id: int | None, sub_name: str | None, extension_id: int | None, mime_type_id: int | None, category_id: int | None) -> File | list[File] | None:
        logger.debug(
            "File repository: get files. Params: "
            "file_id=%s, sub_name=%r, extension_id=%s, mime_type_id=%s, category_id=%s",
            file_id, sub_name, extension_id, mime_type_id, category_id
        )
        try:
            if file_id:
                logger.info("file repository: ")
                response = await self.session.execute(select(File)
                    .where(File.id == file_id)
                    .options(
                        selectinload(File.category),
                        selectinload(File.mime_type),
                        selectinload(File.extension),
                        selectinload(File.versions),))

                result = response.scalar_one_or_none()

                if result:
                    logger.info(f"File repository: found file_id={result.id}")
                else:
                    logger.warning(f"File repository: file_id={file_id} not found")

                return result

            response = await self.session.execute(select(File)
                .where(and_(
                    (File.name.contains(sub_name) if sub_name else true()),
                    (File.extension_id == extension_id if extension_id else true()),
                    (File.mime_type_id == mime_type_id if mime_type_id else true()),
                    (File.category_id == category_id if category_id else true())
                )).options(
                    selectinload(File.category),
                    selectinload(File.mime_type),
                    selectinload(File.extension),
                    selectinload(File.versions),
                ))

            result = list(response.scalars().all())
            logger.info(f"File repository: found {len(result)} files matching filters")
            return result
        except SQLAlchemyError:
            logger.exception("File repository: database error occurred during get operational workflow")
            raise


    async def create(self, name: str, extension_id: int | None, mime_type_id: int | None, category_id: int, password_hash: str | None) -> File | None:
        logger.debug("File repository: create file. Params: "
            f"name={name}, extension_id={extension_id}, mime_type_id={mime_type_id}, category_id={category_id}, password_hash={password_hash}"
        )
        try:
            file = File(
                name=name,
                extension_id=extension_id,
                mime_type_id=mime_type_id,
                category_id=category_id,
                password_hash=password_hash
            )

            self.session.add(file)
            await self.session.commit()
            await self.session.refresh(file)

            logger.info(f"File repository: created file by id={file.id}")

            return file
        except SQLAlchemyError:
            logger.exception("File repository: database error occurred during create operational workflow")
            raise


    async def update(self, file_id: int, name: str | None, extension_id: int | None, mime_type_id: int | None, category_id: int | None, password_hash: str | None) -> File | None:
        logger.info(
            "File repository: update file. Params: "
            f"file_id={file_id}, name={name}, extension_id={extension_id}, mime_type_id={mime_type_id}, category_id={category_id}, password_hash={password_hash}"
        )

        try:
            response = await self.session.execute(select(File).where(File.id == file_id))
            file = response.scalar_one_or_none()

            if not file:
                logger.warning(f"File repository: file_id={file_id} not fount")
                return None

            if name: file.name = name
            if extension_id: file.extension_id = extension_id
            if mime_type_id: file.mime_type_id = mime_type_id
            if category_id: file.category_id = category_id
            if password_hash: file.password_hash = password_hash

            await self.session.commit()
            await self.session.refresh(file)

            logger.info(f"File repository: update file by id={file.id}")

            return file

        except SQLAlchemyError:
            logger.exception("File repository: database error occurred during update ooperaional workflow")
            raise
