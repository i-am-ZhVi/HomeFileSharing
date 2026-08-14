
from typing import TYPE_CHECKING

from pydantic import BaseModel
from features.base_schema import BaseResponse

if TYPE_CHECKING:
    from features.extension.schemas.requests import ExtensionMimeTypeResponse
    from features.category.schemas.requests import CategoryMimeTypeResponse


class MimeTypeResponse(BaseResponse):
    id: int
    name: str

    category: "CategoryMimeTypeResponse"
    extensions: list["ExtensionMimeTypeResponse"]


class MimeTypeCategoryResponse(BaseModel):
    id: int
    name: str

    extensions: list["ExtensionMimeTypeResponse"]

class MimeTypeExtensionResponse(BaseResponse):
    id: int
    name: str

    category: "CategoryMimeTypeResponse"
