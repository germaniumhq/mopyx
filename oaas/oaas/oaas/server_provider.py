import abc
from typing import TypeVar, Any, Optional, Dict

from oaas.service_definition import ServiceDefinition

T = TypeVar("T")


class ServerMiddleware(metaclass=abc.ABCMeta):
    """
    Defines a serialization provider that can interpret the
    registrations and invoke the methods.
    """

    @abc.abstractmethod
    def serve(self) -> None:
        ...

    @abc.abstractmethod
    def join(self) -> None:
        ...

    @abc.abstractmethod
    def can_serve(self, service_definition: ServiceDefinition) -> bool:
        ...

    @abc.abstractmethod
    def can_publish(self, *, instance: Any) -> bool:
        ...

    @abc.abstractmethod
    def publish(
        self,
        instance: Any,
        name: str,
        namespace: str = "default",
        version: str = "1",
        tags: Optional[Dict[str, str]] = None,
    ) -> str:
        ...

    @abc.abstractmethod
    def unpublish(self, id: str) -> None:
        ...
