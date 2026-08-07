from pydantic import BaseModel

from features.category.schemas.requests import CategoryResponse


class MimeTypeResponse(BaseModel):
    id: int
    name: str

    category: CategoryResponse
