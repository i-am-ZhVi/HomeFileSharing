from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db_session
from features.mime_types.usecases.create_mime_type import CreateMimeTypeUseCase
from features.mime_types.usecases.get_mime_type_by_id import GetMimeTypeByIdUseCase
from features.mime_types.usecases.get_mime_type_list import GetMimeTypeListUseCase
from features.mime_types.usecases.update_mime_type import UpdateMimeTypeUseCase
from infrastructure.repositories.mime_type_repository import SQLAlchemyMimeTypeRepository
from features.mime_types.schemas.requests import MimeTypeResponse


router = APIRouter(prefix="/mime_types", tags=["Mime types"])


@router.get("/", response_model=list[MimeTypeResponse])
async def get_list(sub_name: str | None = None, category_id: int | None = None, session: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyMimeTypeRepository(session)
    usecase = GetMimeTypeListUseCase(repo)
    response = await usecase.execute(sub_name, category_id)

    return [MimeTypeResponse.model_validate(mime_type, from_attributes=True) for mime_type in response]

@router.get("/{id}", response_model=MimeTypeResponse | None)
async def get_by_id(id: int, session: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyMimeTypeRepository(session)
    usecase = GetMimeTypeByIdUseCase(repo)
    response = await usecase.execute(id)

    return MimeTypeResponse.model_validate(response, from_attributes=True)


@router.post("/", response_model=MimeTypeResponse | None)
async def create(name: str, category_id: int, session: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyMimeTypeRepository(session)
    usecase = CreateMimeTypeUseCase(repo)
    response = await usecase.execute(name, category_id)

    return MimeTypeResponse.model_validate(response, from_attributes=True)


@router.patch("/{id}", response_model=MimeTypeResponse | None)
async def update(id: int, sub_name: str | None, category_id: int | None, session: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyMimeTypeRepository(session)
    usecase = UpdateMimeTypeUseCase(repo)
    response = await usecase.execute(id, sub_name, category_id)

    return MimeTypeResponse.model_validate(response, from_attributes=True)
