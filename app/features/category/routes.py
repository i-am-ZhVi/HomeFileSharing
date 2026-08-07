
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from features.category.usecases.update_category import UpdateCategoryUseCase
from features.category.usecases.create_category import CreateCategoryUseCase
from features.category.usecases.get_category_by_id import GetCategoryByIdUseCase
from core.database import get_db_session
from features.category.schemas.requests import CategoryResponse
from features.category.usecases.get_category_list import GetCategoryListUseCase
from infrastructure.repositories.category_repository import SQLAlchemyCategoryRepository


router = APIRouter(prefix="/categories", tags=["Categories"])



@router.get("/", response_model=list[CategoryResponse])
async def get_list(sub_name: str | None = None, mime_type_id: int | None = None, session: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyCategoryRepository(session)
    usecase = GetCategoryListUseCase(repo)

    response = await usecase.execute(sub_name, mime_type_id)

    return [CategoryResponse.model_validate(category, from_attributes=True) for category in response]


@router.get("/{id}", response_model=CategoryResponse | None)
async def get_by_id(id: int, session: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyCategoryRepository(session)
    usecase = GetCategoryByIdUseCase(repo)

    response = await usecase.execute(id)

    return CategoryResponse.model_validate(response, from_attributes=True) if response else None


@router.post("/", response_model=CategoryResponse | None)
async def create(name: str, session: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyCategoryRepository(session)
    usecase = CreateCategoryUseCase(repo)

    response = await usecase.execute(name)

    return CategoryResponse.model_validate(response, from_attributes=True) if response else None


@router.patch("/{id}", response_model=CategoryResponse | None)
async def update(id: int, name: str, session: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyCategoryRepository(session)
    usecase = UpdateCategoryUseCase(repo)

    response = await usecase.execute(id, name)

    return CategoryResponse.model_validate(response, from_attributes=True) if response else None
