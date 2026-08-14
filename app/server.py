from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from core.config import settings
from features.routes import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    from features.category.schemas.requests import CategoryResponse, CategoryMimeTypeResponse
    from features.mime_types.schemas.requests import MimeTypeResponse, MimeTypeCategoryResponse, MimeTypeExtensionResponse
    from features.extension.schemas.requests import ExtensionResponse, ExtensionFileResponse, ExtensionMimeTypeResponse
    from features.files.schemas.requests import FileResponse, FileExtensionResponse, FileFileVersionResponse
    from features.file_versions.schemas.requests import FileVersionResponse, FileVersionFileResponse
    from core.logger import logger

    CategoryResponse.model_rebuild()
    CategoryMimeTypeResponse.model_rebuild()
    MimeTypeResponse.model_rebuild()
    MimeTypeCategoryResponse.model_rebuild()
    MimeTypeExtensionResponse.model_rebuild()
    ExtensionResponse.model_rebuild()
    ExtensionFileResponse.model_rebuild()
    ExtensionMimeTypeResponse.model_rebuild()
    FileResponse.model_rebuild()
    FileExtensionResponse.model_rebuild()
    FileFileVersionResponse.model_rebuild()
    FileVersionResponse.model_rebuild()
    FileVersionFileResponse.model_rebuild()

    logger.info("Pydantic models rebuilded.")
    yield


app = FastAPI(title="Home file sharing", docs_url="/api/docs", redoc_url="/api/redoc", openapi_url="/api/openapi.json", swagger_ui_oauth2_redirect_url="/api/docs/oauth2-redirect", lifespan=lifespan)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
def root():
    return "Hello, this is a home-based web service for file sharing."


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/api/web-app")
def web_app():
    return FileResponse("static/web_interface.html")
