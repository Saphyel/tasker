from datetime import datetime

from pydantic import BaseModel


class Model(BaseModel):
    class Config:
        anystr_strip_whitespace = True


class Work(Model):
    date: datetime
    tag: str
    details: str


class Search(Model):
    date: datetime | None
    tag: str | None


class Query(Model):
    limit: int
    order: str
