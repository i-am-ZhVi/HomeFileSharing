from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from features.extension.usecases.delete_extension import DeleteExtensionUseCase
from core.database import get_db_session
from features.extension.schemas.requests import ExtensionResponse
from features.extension.usecases.create_extension import CreateExtensionUseCase
from features.extension.usecases.get_extension_by_id import GetExtensionByIdUseCase
from features.extension.usecases.get_extension_list import GetExtensionListUseCase
from features.extension.usecases.update_extension import UpdateExtensionUseCase
from infrastructure.repositories.extension_repository import SQLAlchemyExtensionRepository


router = APIRouter(prefix="/extensions", tags=["Extensions"])

@router.get("/", response_model=list[ExtensionResponse])
async def get_list(sub_name: str | None = None, mime_type_id: int | None = None, session: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyExtensionRepository(session)
    usecase = GetExtensionListUseCase(repo)

    response = await usecase.execute(sub_name, mime_type_id)

    return [ExtensionResponse.model_validate(extension, from_attributes=True) for extension in response]


@router.get("/{id}", response_model=ExtensionResponse | None)
async def get_by_id(id: int, session: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyExtensionRepository(session)
    usecase = GetExtensionByIdUseCase(repo)

    response = await usecase.execute(id)

    return ExtensionResponse.model_validate(response, from_attributes=True)


@router.post("/", response_model=ExtensionResponse)
async def create(name: str, mime_type_id: int, session: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyExtensionRepository(session)
    usecase = CreateExtensionUseCase(repo)

    response = await usecase.execute(name, mime_type_id)

    return ExtensionResponse.model_validate(response, from_attributes=True)


@router.patch("/{id}", response_model=list[ExtensionResponse])
async def update(id: int, name: str | None = None, mime_type_id: int | None = None, session: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyExtensionRepository(session)
    usecase = UpdateExtensionUseCase(repo)

    response = await usecase.execute(id, name, mime_type_id)

    return ExtensionResponse.model_validate(response, from_attributes=True)

@router.delete("/{id}", response_model=list[ExtensionResponse])
async def delete(id: int, session: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyExtensionRepository(session)
    usecase = GetExtensionByIdUseCase(repo)

    extension = await usecase.execute(id)

    if not extension:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)

    delete_usecase = DeleteExtensionUseCase(repo)

    if not await delete_usecase.execute(id=id, name=extension.name, dir_name=extension.mime_type.category.name):
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)

    return {
        "message": f"The {extension.name} extension was deleted."""
    }
