from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from features.files.usecases.create_file import CreateFileUseCase
from features.files.usecases.get_file_by_id import GetFileByIdUseCase
from features.files.usecases.get_file_list import GetFileListUseCase
from features.files.usecases.update_file import UpdateFileUseCase
from infrastructure.repositories.file_repository import SQLAlchemyFileRepository
from core.database import get_db_session
from features.files.schemas.requests import FileResponse


router = APIRouter(prefix="/files", tags=["Files"])

@router.get("/", response_model=list[FileResponse])
async def get_list(sub_name: str | None = None, extension_id: int | None = None, session: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyFileRepository(session)
    usecase = GetFileListUseCase(repo)
    response = await usecase.execute(sub_name=sub_name, extension_id=extension_id)

    return [FileResponse.model_validate(file, from_attributes=True) for file in response]


@router.get("/{id}", response_model=FileResponse | None)
async def get_by_id(id: int, session: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyFileRepository(session)
    usecase = GetFileByIdUseCase(repo)
    response = await usecase.execute(id)

    return FileResponse.model_validate(response, from_attributes=True)


@router.post("/", response_model=FileResponse | None)
async def create(name: str, extension_id: int, password_hash: str | None = None, session: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyFileRepository(session)
    usecase = CreateFileUseCase(repo)
    response = await usecase.execute(name=name, extension_id=extension_id, password_hash=password_hash)

    return FileResponse.model_validate(response, from_attributes=True)


@router.patch("/{id}", response_model=FileResponse | None)
async def update(id: int, name: str | None = None, extension_id: int | None = None, password_hash: str | None = None, session: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyFileRepository(session)
    usecase = UpdateFileUseCase(repo)
    response = await usecase.execute(file_id=id, name=name, extension_id=extension_id, password_hash=password_hash)

    return FileResponse.model_validate(response, from_attributes=True)
