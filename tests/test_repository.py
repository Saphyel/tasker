from datetime import datetime
from unittest.mock import Mock

import pytest

from src.model import Work, Search
from src.repository import WorkRepository


class TestWorkRepository:
    def setup_method(self):
        self.collection = Mock()
        db = Mock()
        db.work = self.collection
        self.repository = WorkRepository(db)

    def test_insert(self):
        insert_one_result = Mock()
        insert_one_result.inserted_id = "Id"
        self.collection.insert_one.return_value = insert_one_result
        assert self.repository.insert(Work(date=datetime.utcnow(), tag="etiqueta", details="detalles")) == "Id"

    @pytest.mark.parametrize(
        ["param", "expect"],
        [(Search(), []), (Search(), [{"_id": "id", "tag": "etiqueta", "details": "detalles", "date": "2022-12-12"}])],
    )
    def test_find(self, param, expect):
        self.collection.find.return_value = expect
        assert self.repository.find(param) == expect
