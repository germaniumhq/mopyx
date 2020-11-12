from typing import Any, Dict, cast, TypeVar, Optional

import oaas._registrations as registrations
from oaas import ServiceDefinition
from oaas.client_definition import ClientDefinition
from oaas.client_provider import ClientMiddleware
from oaas.server_provider import ServerMiddleware

T = TypeVar("T")


class ReflectionInvoker:
    def __init__(self, *, delegate: Any) -> None:
        self._delegate = delegate

    def __getattr__(self, item):
        return getattr(self._delegate, item)


class LocalClientServerMiddleware(ClientMiddleware, ServerMiddleware):
    """
    Provides a server that can invoke local services
    """

    def __init__(self) -> None:
        self._service_instance: Dict[str, Any] = dict()

    def serve(self) -> None:
        for service_definition in registrations.services:
            self._service_instance[service_definition.name] = service_definition.code()

    def join(self) -> None:
        pass

    def create_client(self, client_definition: ClientDefinition) -> T:
        service_instance = self._service_instance[client_definition.name]

        return cast(T, ReflectionInvoker(delegate=service_instance))

    def can_handle(self, client_definition: ClientDefinition) -> bool:
        return True

    def can_serve(self, service_definition: ServiceDefinition) -> bool:
        return True

    def can_publish(self, *, instance: Any) -> bool:
        return False

    def publish(
        self,
        instance: Any,
        name: str,
        namespace: str = "default",
        version: str = "1",
        tags: Optional[Dict[str, str]] = None,
    ) -> str:
        raise Exception(
            f"LocalClientServerMiddleware is a test middleware. "
            f"Can't serve service {instance}"
        )

    def unpublish(self, id: str) -> None:
        raise Exception(
            f"LocalClientServerMiddleware is a test middleware. "
            f"Can't unserve service instance id {id}"
        )
