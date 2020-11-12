Operation As A Service API

Installation
============

.. code:: sh

    pip install oaas

Usage
=====

.. code:: python

    from typing import Any, List

    import oaas


    @oaas.client("users-get")
    def get_users(group: str) -> List[Any]: ...


    @oaas.client("datastore")
    class DataStore:
        def put_item(self, key: str, value: Any) -> None: ...

        def get_item(self, key: str) -> None: ...

        def remove_item(self, key: str) -> None: ...


    @oaas.service("users-get")
    def get_user_list(group: str) -> List[Any]: ...


    @oaas.service("datastore")
    class DataStoreService:
        def put_item(self, key: str, value: Any) -> None: ...

        def get_item(self, key: str) -> None: ...

        def remove_item(self, key: str) -> None: ...


    @oaas.service("intercept")
    def get_user_intercept(group: str) -> List[Any]: ...


    @oaas.service("datastore")
    class DataStoreIntercept:
        def put_item(self, key: str, value: Any) -> None: ...

        def get_item(self, key: str) -> None: ...

        def remove_item(self, key: str) -> None: ...
