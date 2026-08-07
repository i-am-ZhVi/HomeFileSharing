from fastapi import APIRouter
from features.category.routes import router as category_router
from features.extension.routes import router as extension_router

router = APIRouter(prefix="/api", tags=["API"])

router.include_router(category_router)
router.include_router(extension_router)
