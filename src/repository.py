from bson.objectid import ObjectId
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.database import Database

from model import Work, Query, Search


class WorkRepository:
    def __init__(self, db: Database):
        self.collection: Collection = db.work

    def insert(self, data: Work) -> ObjectId:
        return self.collection.insert_one(data.dict()).inserted_id

    def find(self, search: Search, query: Query) -> Cursor:
        return self.collection.find(search.dict(exclude_none=True)).sort(query.order).limit(query.limit)
