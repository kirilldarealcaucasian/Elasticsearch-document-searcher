from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PostS(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    rubrics: list[str]
    text: str
    created_date: datetime
