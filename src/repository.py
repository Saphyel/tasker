from bson.objectid import ObjectId
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.database import Database

from model import TaskInput, Query, Search, SortEnum


class TaskRepository:
    def __init__(self, db: Database):
        self.collection: Collection = db.task

    def insert(self, data: TaskInput) -> ObjectId:
        return self.collection.insert_one(data.dict()).inserted_id

    def find(self, search: Search, query: Query) -> Cursor:
        params = search.dict(exclude_none=True)
        if query.last_seen:
            params["_id"] = {"$gt": query.last_seen}
        result = self.collection.find(params).limit(query.limit)
        if query.sort == SortEnum.newest:
            result = result.sort("date", -1)
        elif query.sort == SortEnum.oldest:
            result = result.sort("date", 1)
        return result
