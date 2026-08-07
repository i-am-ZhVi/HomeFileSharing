from fastapi import APIRouter
from features.category.routes import router as category_router
from features.extension.routes import router as extension_router
from features.mime_types.routes import router as mime_type_router

router = APIRouter(prefix="/api")

router.include_router(category_router)
router.include_router(extension_router)
router.include_router(mime_type_router)
