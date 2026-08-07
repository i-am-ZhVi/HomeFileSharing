from fastapi import APIRouter
from features.category.routes import router as category_router


router = APIRouter(prefix="/api", tags=["API"])

router.include_router(category_router)
