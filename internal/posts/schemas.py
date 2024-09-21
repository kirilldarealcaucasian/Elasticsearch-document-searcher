from uuid import UUID

from pydantic import BaseModel, ConfigDict
from datetime import datetime


class PostS(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    rubrics: list[str]
    text: str
    created_date: datetime