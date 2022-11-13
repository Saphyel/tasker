from bson.objectid import ObjectId
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.database import Database

from model import Work, Search


class WorkRepository:
    def __init__(self, db: Database):
        self.collection: Collection = db.work

    def insert(self, data: Work) -> ObjectId:
        return self.collection.insert_one(data.dict()).inserted_id

    def find(self, query: Search) -> Cursor:
        return self.collection.find(query.dict(exclude_none=True))
