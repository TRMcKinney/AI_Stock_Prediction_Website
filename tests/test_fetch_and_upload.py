import os
from datetime import datetime
from types import SimpleNamespace
import sys
import importlib

# Ensure required env vars are set before importing the module
os.environ.setdefault("ALPHA_VANTAGE_API_KEY", "test")
os.environ.setdefault("SUPABASE_URL", "http://example.com")
os.environ.setdefault("SUPABASE_KEY", "key")

sys.modules.setdefault(
    "prediction_history", importlib.import_module("backend.prediction_history")
)
import backend.fetch_and_upload as fu

class DummyTable:
    def __init__(self, count_data):
        self.count_data = count_data
        self.last_update = None
        self.last_insert = None
        self.mode = "select"

    def select(self, *args, **kwargs):
        self.mode = "select"
        return self

    def update(self, obj):
        self.mode = "update"
        self.last_update = obj
        return self

    def insert(self, obj):
        self.mode = "insert"
        self.last_insert = obj
        return self

    def eq(self, *args, **kwargs):
        return self

    def maybe_single(self):
        return self

    def execute(self):
        if self.mode == "select":
            return SimpleNamespace(data=self.count_data)
        return SimpleNamespace()

class DummySupabase:
    def __init__(self, count_data):
        self.table_instance = DummyTable(count_data)

    def table(self, name):
        return self.table_instance

def _patch_common(mocker, supabase, date):
    mocker.patch.object(fu, "supabase", supabase)
    mocker.patch.object(fu, "get_daily_stock_data", return_value=[])
    dt_mock = mocker.Mock(wraps=datetime)
    dt_mock.today.return_value = date
    mocker.patch.object(fu, "datetime", dt_mock)


def test_fetch_count_updated_when_no_data(mocker):
    supa = DummySupabase({"value": "2"})
    _patch_common(mocker, supa, datetime(2024, 1, 1))
    result = fu.fetch_and_upload()
    assert result == 0
    assert supa.table_instance.last_update == {"value": "3"}
    assert supa.table_instance.last_insert is None


def test_fetch_count_inserted_when_no_data_first_time(mocker):
    supa = DummySupabase(None)
    _patch_common(mocker, supa, datetime(2024, 1, 1))
    result = fu.fetch_and_upload()
    assert result == 0
    assert supa.table_instance.last_insert == {"date": "2024-01-01", "value": "1"}
    assert supa.table_instance.last_update is None
