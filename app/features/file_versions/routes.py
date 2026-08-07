from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

from features.files.usecases.get_file_by_id import GetFileByIdUseCase
from infrastructure.repositories.file_repository import SQLAlchemyFileRepository
from features.file_versions.usecases.create_file_version import CreateFileVersionUseCase
from features.file_versions.usecases.get_file_version_by_id import GetFileVersionByIdUseCase
from features.file_versions.usecases.update_file_version import UpdateFileVersionUseCase
from features.file_versions.schemas.requests import FileVersionResponse
from features.file_versions.usecases.get_file_version_list import GetFileVersionListUseCase
from infrastructure.repositories.file_version_repository import SQLAlchemyFileVersionRepository
from core.database import get_db_session


router = APIRouter(prefix="/file_versions", tags=["File versions"])

@router.get("/", response_model=list[FileVersionResponse])
async def get_list(file_id: int | None = None, session: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyFileVersionRepository(session)
    usecase = GetFileVersionListUseCase(repo)

    response = await usecase.execute(file_id)

    return [FileVersionResponse.model_validate(file_version, from_attributes=True) for file_version in response]


@router.get("/{version_uuid}", response_model=FileVersionResponse | None)
async def get_by_id(version_uuid: str, session: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyFileVersionRepository(session)
    usecase = GetFileVersionByIdUseCase(repo)

    response = await usecase.execute(version_uuid)

    return FileVersionResponse.model_validate(response, from_attributes=True)


@router.post("/", response_model=FileVersionResponse | None)
async def create(file_id: int, version: str | None, file: UploadFile, session: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyFileVersionRepository(session)
    usecase = CreateFileVersionUseCase(repo)

    file_repo = SQLAlchemyFileRepository(session)
    file_get_by_id_usecase = GetFileByIdUseCase(file_repo)
    file_db = await file_get_by_id_usecase.execute(file_id)
    if not file_db:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"File by id {file_id} not found.")

    response = await usecase.execute(file_id=file_id, version=version, file=file, category_name=file_db.extension.mime_type.category.name)

    return FileVersionResponse.model_validate(response, from_attributes=True)


@router.patch("/{version_uuid}", response_model=FileVersionResponse | None)
async def update(version_uuid: str, file_id: int | None, version: str | None,
    bytes: int | None, checksum: str | None, session: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyFileVersionRepository(session)
    usecase = UpdateFileVersionUseCase(repo)

    response = await usecase.execute(version_uuid=version_uuid, file_id=file_id, version=version, bytes=bytes, checksum=checksum)

    return FileVersionResponse.model_validate(response, from_attributes=True)
