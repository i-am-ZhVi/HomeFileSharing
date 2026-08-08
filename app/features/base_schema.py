from datetime import datetime
from pydantic import BaseModel, ConfigDict


class BaseResponse(BaseModel):
    created_at: datetime
    updated_at: datetime
