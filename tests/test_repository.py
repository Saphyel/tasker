from datetime import datetime
from unittest.mock import Mock

import pytest

from src.model import TaskInput, Search, Pagination, SortEnum, TaskOutput
from src.repository import TaskRepository


db_response = {"_id": "Id", "tag": "algo", "details": "nuevo", "date": "2022-12-12T11:11"}
endpoint_expect = TaskOutput(id="Id", tag="algo", details="nuevo", date="2022-12-12T11:11")


class TestWorkRepository:
    def setup_method(self):
        self.collection = Mock()
        db = Mock()
        db.task = self.collection
        self.repository = TaskRepository(db)

    def test_insert(self):
        insert_one_result = Mock()
        insert_one_result.inserted_id = "Id"
        self.collection.insert_one.return_value = insert_one_result
        assert self.repository.insert(TaskInput(date=datetime.utcnow(), tag="etiqueta", details="detalles")) == "Id"

    @pytest.mark.parametrize(
        ["param", "expect", "response"],
        [
            (Pagination(limit=1, sort=SortEnum.newest), [], []),
            (Pagination(limit=1, sort=SortEnum.newest), [endpoint_expect], [db_response]),
        ],
    )
    def test_find(self, param, expect, response):
        self.collection.find.return_value.limit.return_value.skip.return_value.sort.return_value = response
        assert self.repository.find(Search(), param).result == expect
