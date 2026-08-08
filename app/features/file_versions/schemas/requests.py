from typing import TYPE_CHECKING
import uuid
from features.base_schema import BaseResponse
if TYPE_CHECKING:
    from features.files.schemas.requests import FileFileVersionResponse


class FileVersionResponse(BaseResponse):
    id: uuid.UUID
    version: str
    bytes: int
    checksum: str

    file: "FileFileVersionResponse"

class FileVersionFileResponse(BaseResponse):
    id: uuid.UUID
    version: str
    bytes: int
    checksum: str
