import abc
from typing import TypeVar

from oaas.client_definition import ClientDefinition

T = TypeVar("T")


class ClientMiddleware(metaclass=abc.ABCMeta):
    """
    Defines a serialization provider that can interpret the
    registrations and invoke the methods.
    """

    @abc.abstractmethod
    def create_client(self, client_definition: ClientDefinition) -> T:
        """
        Create a client proxy to the target definition. Tags might
        refine, or override the tags from the default client definition
        registration
        """
        ...

    @abc.abstractmethod
    def can_handle(self, client_definition: ClientDefinition) -> bool:
        pass
