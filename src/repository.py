from datetime import timezone

from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from model import TaskInput, Pagination, Search, SortEnum, Result, TaskOutput
from settings import app_settings


class TaskRepository:
    def __init__(self, db: Database):
        self.collection: Collection = db.task

    def insert(self, data: TaskInput) -> ObjectId:
        if not data.date.tzname():
            data.date = data.date.replace(tzinfo=timezone.utc, microsecond=0, second=0)
        return self.collection.insert_one(data.dict()).inserted_id

    def find(self, search: Search, pagination: Pagination) -> Result:
        params = search.dict(exclude_none=True)
        pagination.total = self.collection.estimated_document_count(params)
        result = self.collection.find(params).limit(pagination.limit).skip(pagination.limit * (pagination.page - 1))
        if pagination.sort == SortEnum.newest:
            result = result.sort("date", -1)
        elif pagination.sort == SortEnum.oldest:
            result = result.sort("date", 1)

        return Result(
            pagination=pagination,
            result=[
                TaskOutput(date=item["date"], tag=item["tag"], details=item["details"], id=str(item["_id"]))
                for item in result
            ],
        )

    def check_health(self) -> dict:
        return self.collection.database.client.server_info()


def task_repository(database_uri: str = app_settings.database_uri) -> TaskRepository:
    return TaskRepository(MongoClient(database_uri).work)
