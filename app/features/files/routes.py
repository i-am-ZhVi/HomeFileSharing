import mimetypes
from pathlib import Path
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse as FastApiFileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from core.file_manager import file_manager
from features.category.usecases.get_category_by_name import GetCategoryByNameUseCase
from features.extension.usecases.get_extension_by_name import GetExtensionByNameUseCase
from features.mime_types.usecases.get_mime_type_by_name import GetMimeTypeByNameUseCase
from features.file_versions.usecases.create_file_version import CreateFileVersionUseCase
from infrastructure.repositories.file_version_repository import SQLAlchemyFileVersionRepository
from core.config import settings
from core.logger import logger
from features.category.usecases.create_category import CreateCategoryUseCase
from features.category.usecases.get_category_list import GetCategoryListUseCase
from features.extension.usecases.create_extension import CreateExtensionUseCase
from features.extension.usecases.get_extension_list import GetExtensionListUseCase
from features.mime_types.usecases.create_mime_type import CreateMimeTypeUseCase
from features.mime_types.usecases.get_mime_type_list import GetMimeTypeListUseCase
from infrastructure.repositories.category_repository import SQLAlchemyCategoryRepository
from infrastructure.repositories.extension_repository import SQLAlchemyExtensionRepository
from infrastructure.repositories.mime_type_repository import SQLAlchemyMimeTypeRepository
from features.files.usecases.create_file import CreateFileUseCase
from features.files.usecases.get_file_by_id import GetFileByIdUseCase
from features.files.usecases.get_file_list import GetFileListUseCase
from features.files.usecases.update_file import UpdateFileUseCase
from infrastructure.repositories.file_repository import SQLAlchemyFileRepository
from core.database import get_db_session
from features.files.schemas.requests import FileResponse, FileUpload

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
async def create(info: FileUpload = Depends(FileUpload.as_form), file: UploadFile = File(...), session: AsyncSession = Depends(get_db_session)):
    if not file.filename:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST)

    repo = SQLAlchemyFileRepository(session)
    usecase = CreateFileUseCase(repo)

    file_extension = Path(file.filename).suffix[1:]


    extension_repo = SQLAlchemyExtensionRepository(session)
    extension_get_by_name_usecase = GetExtensionByNameUseCase(extension_repo)

    extension = await extension_get_by_name_usecase.execute(name=file_extension if file_extension else "")
    extension_id = None


    if extension:
        extension_id = extension.id
    else:
        file_mime_type, encodings = mimetypes.guess_type(file.filename)
        mime_type_repo = SQLAlchemyMimeTypeRepository(session)
        mime_type_get_by_name_usecase = GetMimeTypeByNameUseCase(mime_type_repo)
        mime_type = await mime_type_get_by_name_usecase.execute(name=file_mime_type if file_mime_type else "")
        mime_type_id = None
        if mime_type:
            mime_type_id = mime_type.id
        else:
            category_repo = SQLAlchemyCategoryRepository(session)
            category_get_by_name_usecase = GetCategoryByNameUseCase(category_repo)
            category_id = None
            category = await category_get_by_name_usecase.execute(name=settings.OTHER_FILES_DIRECTORY_NAME)
            if category:
                category_id = category.id
            else:
                category_create_usecase = CreateCategoryUseCase(category_repo)
                retries = 1
                while not category_id and retries < 5:
                    other_category = await category_create_usecase.execute(name=settings.OTHER_FILES_DIRECTORY_NAME)
                    if other_category:
                        category_id = other_category.id
                    logger.exception(f"File routes: The directory for other files is not being created | retries {retries}/5.")
                    retries += 1
                if not category_id:
                    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="The directory for other files is not being created.")
            mime_type_create_usecase = CreateMimeTypeUseCase(mime_type_repo)
            mime_type = await mime_type_create_usecase.execute(file_mime_type if file_mime_type else "", category_id)

            if not mime_type:
                retries = 1
                while not mime_type and retries < 5:
                    mime_type = await mime_type_create_usecase.execute(file_mime_type if file_mime_type else "", category_id)
                    logger.exception(f"File routes: The mime type {file_mime_type if file_mime_type else ""} is not being created | retries {retries}/5.")
                    retries += 1
                if not mime_type:
                    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"File routes: The mime type {file_mime_type if file_mime_type else ""} is not being created.")

            mime_type_id = mime_type.id

        extension_create_usecase = CreateExtensionUseCase(extension_repo)
        extension = await extension_create_usecase.execute(file_extension if file_extension else "", mime_type_id)

        if not extension:
            retries = 1
            while not extension and retries < 5:
                extension = await extension_create_usecase.execute(file_extension if file_extension else "", mime_type_id)
                logger.exception(f"File routes: The extension {file_extension if file_extension else ""} is not being created | retries {retries}/5.")
                retries += 1
            if not extension:
                raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"File routes: The extension {file_extension if file_extension else ""} is not being created.")

        extension_id = extension.id


    response = await usecase.execute(name=file.filename.replace(f".{file_extension}", ""), extension_id=extension_id, password_hash=info.password)

    if not response:
        return None

    file_version_repo = SQLAlchemyFileVersionRepository(session)
    file_version_create_usecase = CreateFileVersionUseCase(file_version_repo)
    await file_version_create_usecase.execute(file_id=response.id, version="v1.0", file=file, category_name=response.extension.mime_type.category.name)

    return FileResponse.model_validate(response, from_attributes=True)


@router.get("/download/{id}")
async def download(id: int, session: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyFileRepository(session)
    usecase = GetFileByIdUseCase(repo)
    file = await usecase.execute(id)

    if not file:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)

    file_version = file.versions[0]

    if not file_version:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)

    file_path = await file_manager.find_file_path_from_directory(version_uuid=file_version.id, upload_dir=f"{settings.UPLOAD_DIRECTORY}/{file.extension.mime_type.category.name}")

    file_name = file.name

    if file.extension.name != "":
        file_name += "." + file.extension.name

    return FastApiFileResponse(
        path=file_path,
        filename=file_name
    )



@router.patch("/{id}", response_model=FileResponse | None)
async def update(id: int, name: str | None = None, extension_id: int | None = None, password_hash: str | None = None, session: AsyncSession = Depends(get_db_session)):
    repo = SQLAlchemyFileRepository(session)
    usecase = UpdateFileUseCase(repo)
    response = await usecase.execute(file_id=id, name=name, extension_id=extension_id, password_hash=password_hash)

    return FileResponse.model_validate(response, from_attributes=True)
