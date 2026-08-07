import uuid
from pydantic import BaseModel

from features.files.schemas.requests import FileResponse


class FileVersionResponse(BaseModel):
    id: uuid.UUID
    version: str
    bytes: int
    checksum: str
