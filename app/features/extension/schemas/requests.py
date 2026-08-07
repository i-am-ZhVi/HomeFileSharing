from pydantic import BaseModel

from features.category.schemas.requests import CategoryResponse


class ExtensionResponse(BaseModel):
    id: int
    name: str
