
from typing import TYPE_CHECKING
from features.base_schema import BaseResponse
if TYPE_CHECKING:
    from features.mime_types.schemas.requests import MimeTypeResponse
    from features.mime_types.schemas.requests import MimeTypeCategoryResponse


class CategoryResponse(BaseResponse):
    id: int
    name: str

    mime_types: list["MimeTypeCategoryResponse"]


class CategoryMimeTypeResponse(BaseResponse):
    id: int
    name: str
