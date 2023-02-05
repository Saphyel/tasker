from datetime import datetime
from unittest.mock import Mock

import pytest

from model import TaskInput, Search, Query, SortEnum
from repository import TaskRepository

db_response = {"_id": "Id", "tag": "algo", "details": "nuevo", "date": "2022-12-12"}


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
        ["param", "expect"],
        [(Query(limit=1, sort=SortEnum.newest), []), (Query(limit=1, sort=SortEnum.newest), [db_response])],
    )
    def test_find(self, param, expect):
        self.collection.find.return_value.limit.return_value.sort.return_value = expect
        assert self.repository.find(Search(), param) == expect
