from typing import TYPE_CHECKING
from fastapi import Form
from pydantic import BaseModel

from features.base_schema import BaseResponse
if TYPE_CHECKING:
    from features.file_versions.schemas.requests import FileVersionFileResponse
    from features.extension.schemas.requests import ExtensionFileResponse


class FileResponse(BaseResponse):
    id: int
    name: str

    extension: "ExtensionFileResponse"
    versions: list["FileVersionFileResponse"]


class FileExtensionResponse(BaseResponse):
    id: int
    name: str

    versions: list["FileVersionFileResponse"]

class FileFileVersionResponse(BaseResponse):
    id: int
    name: str

    extension: "ExtensionFileResponse"

class FileUpload(BaseModel):
    password: str | None = None

    @classmethod
    def as_form(cls, password: str = Form(None)):
        return cls(password=password)
