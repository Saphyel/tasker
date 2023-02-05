from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Model(BaseModel):
    class Config:
        anystr_strip_whitespace = True


class TaskInput(Model):
    date: datetime
    tag: str
    details: str


class TaskOutput(Model):
    id: str
    date: datetime
    tag: str
    details: str


class Search(Model):
    date: datetime | None
    tag: str | None


class SortEnum(str, Enum):
    newest = "newest"
    oldest = "oldest"


class Query(Model):
    limit: int
    sort: SortEnum
    last_seen: str | None
