from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Model(BaseModel):
    class Config:
        str_strip_whitespace = True


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
    tag: str | None = None
    date: datetime | None = None


class SortEnum(str, Enum):
    newest = "newest"
    oldest = "oldest"


class Pagination(Model):
    limit: int
    sort: SortEnum
    page: int = 1
    total: int | None = None


class Result(Model):
    pagination: Pagination
    result: list
