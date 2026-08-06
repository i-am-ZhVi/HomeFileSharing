from sqlalchemy import select, true
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.logger import logger
from app.features.file_versions.repositories.interface import FileVersionRepository
from app.infrastructure.db_models.file_version_table import FileVersion


class SQLAlchemyFileVersionRepository(FileVersionRepository):
    async def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, version_id: str | None, file_id: int | None) -> FileVersion | list[FileVersion] | None:
        logger.debug(
            "File version repository: get file versions. Params"
            f"version_id={version_id}, file_id={file_id}."
        )
        try:
            if version_id:
                response = await self.session.execute(select(FileVersion)
                    .where(FileVersion.id == version_id)
                    .options(
                        selectinload(FileVersion.file)))
                result = response.scalar_one_or_none()

                if result:
                    logger.info(f"File version repository: found file version by id={version_id}.")
                else:
                    logger.warning(f"File version repository: file version by id={version_id} not found.")
                return result

            response = await self.session.execute(select(FileVersion)
                .where(FileVersion.file_id == file_id if file_id else true())
                .options(
                    selectinload(FileVersion.file)))

            result = list(response.scalars().all())

            logger.info(f"File version repository: found {len(result)} file versions matching filters.")

            return result
        except SQLAlchemyError:
            logger.exception("File version repository: database error occurred during get operational workflow.")
            raise



    async def create(self, version_uuid: str, file_id: int, version: str | None, bytes: int, checksum: str) -> FileVersion | None:
        logger.debug(
            "File version repository: create file version. Params"
            f"uuid={version_uuid}, file_id={file_id}, version={version}, bytes={bytes}, checksum={checksum}."
        )

        try:

            file_version = FileVersion(
                id=version_uuid,
                file_id=file_id,
                version=version,
                bytes=bytes,
                checksum=checksum,
            )

            self.session.add(file_version)
            await self.session.commit()
            await self.session.refresh(file_version)

            logger.info(f"File version repository: created file version by uuid={file_version.id}")

            return file_version

        except SQLAlchemyError:
            logger.exception("File version repository: database error occurred during create operational workflow.")
            raise


    async def update(self, version_uuid: str, file_id: int | None, version: str | None, bytes: int | None, checksum: str | None) -> FileVersion | None:
        logger.debug(
            "File version repository: update file version. Params"
            f"uuid={version_uuid}, file_id={file_id}, version={version}, bytes={bytes}, checksum={checksum}."
        )
        try:

            response = await self.session.execute(select(FileVersion).where(FileVersion.id == version_uuid))
            file_version = response.scalar_one_or_none()
            if not file_version:
                logger.warning(f"File version repository: version_uuid={version_uuid} not found")
                return

            if file_id: file_version.file_id = file_id
            if version: file_version.version = version
            if bytes: file_version.bytes = bytes
            if checksum: file_version.checksum = checksum

            await self.session.commit()
            await self.session.refresh(file_version)

            logger.info(f"File version repository: update file version by uuid={file_version.id}")

            return file_version

        except SQLAlchemyError:
            logger.exception("File version repository: database error occurred during update operational workflow.")
            raise
