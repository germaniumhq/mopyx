import unittest
from typing import Any, Dict

import oaas
from test.local_serialization_provider import LocalClientServerMiddleware


@oaas.service("datastore")
class DataStoreService:
    def __init__(self) -> None:
        self._items: Dict[str, Any] = dict()

    def put_item(self, key: str, value: Any) -> None:
        self._items[key] = value

    def get_item(self, key: str) -> Any:
        if key in self._items:
            return self._items.get(key)

        return None

    def remove_item(self, key: str) -> None:
        del self._items[key]


@oaas.client("datastore")
class DataStore:
    def put_item(self, key: str, value: Any) -> None:
        ...

    def get_item(self, key: str) -> Any:
        ...

    def remove_item(self, key: str) -> None:
        ...


provider = LocalClientServerMiddleware()
oaas.register_server_provider(provider)
oaas.register_client_provider(provider)

oaas.serve()


class TestServiceRegistrar(unittest.TestCase):
    def test_service_calls(self) -> None:
        data_store = oaas.get_client(DataStore)

        self.assertIsNone(data_store.get_item("a"))
        data_store.put_item("a", "avalue")
        self.assertEqual("avalue", data_store.get_item("a"))
        data_store.remove_item("a")
        self.assertIsNone(data_store.get_item("a"))
