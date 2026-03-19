from pydantic import BaseModel, ConfigDict
from datetime import datetime


class PostCreate(BaseModel):
    title: str
    content: str


class PostOut(PostCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
