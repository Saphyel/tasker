from datetime import datetime, timezone

from pydantic import BaseModel, Field


class Model(BaseModel):
    class Config:
        anystr_strip_whitespace = True


class Work(Model):
    date: datetime = Field(
        default_factory=datetime.utcnow().replace(tzinfo=timezone.utc, hour=0, minute=0, second=0, microsecond=0)
    )
    tag: str
    details: str


class Search(Model):
    date: datetime | None
    tag: str | None
