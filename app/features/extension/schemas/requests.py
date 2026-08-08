
from typing import TYPE_CHECKING
from features.base_schema import BaseResponse
if TYPE_CHECKING:
    from features.files.schemas.requests import FileExtensionResponse
    from features.mime_types.schemas.requests import MimeTypeExtensionResponse


class ExtensionResponse(BaseResponse):
    id: int
    name: str

    mime_type: "MimeTypeExtensionResponse"
    files: list["FileExtensionResponse"]


class ExtensionMimeTypeResponse(BaseResponse):
    id: int
    name: str

    files: list["FileExtensionResponse"]

class ExtensionFileResponse(BaseResponse):
    id: int
    name: str

    mime_type: "MimeTypeExtensionResponse"
