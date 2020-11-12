import abc
from typing import Dict, Iterable, Optional

from oaas_registry.service_definition import ServiceDefinition


class Registry(metaclass=abc.ABCMeta):
    """
    This registry represents a simple decorator for the actual
    implementations.
    """

    @abc.abstractmethod
    def register_service(
        self,
        *,
        namespace: str = "default",
        name: str,
        version: str = "1",
        tags: Dict[str, str],
        locations: Iterable[str],
    ) -> ServiceDefinition:
        ...

    @abc.abstractmethod
    def resolve_service(
        self,
        *,
        id: Optional[str] = None,
        namespace: str = "default",
        name: str,
        version: str = "1",
        tags: Dict[str, str],
    ) -> Iterable[ServiceDefinition]:
        ...

    @abc.abstractmethod
    def unregister_service(self, *, id: str) -> bool:
        ...
