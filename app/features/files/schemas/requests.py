from fastapi import Form
from pydantic import BaseModel

from features.extension.schemas.requests import ExtensionResponse
from features.mime_types.schemas.requests import MimeTypeResponse


class FileResponse(BaseModel):
    id: int
    name: str
    extension: ExtensionResponse


class FileUpload(BaseModel):
    password: str | None = None

    @classmethod
    def as_form(cls, password: str = Form(None)):
        return cls(password=password)
