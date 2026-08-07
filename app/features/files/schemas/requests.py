from pydantic import BaseModel

from features.extension.schemas.requests import ExtensionResponse
from features.mime_types.schemas.requests import MimeTypeResponse


class FileResponse(BaseModel):
    id: int
    name: str
    extension: ExtensionResponse
    mime_type: MimeTypeResponse
