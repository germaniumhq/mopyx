import abc
from typing import TypedDict, List, Optional


class ServiceDefinitionRequired(TypedDict):
    name: str
    protocol: str


class ServiceDefinition(ServiceDefinitionRequired, total=False):
    namespace: str
    version: str


IpLink = str


class ServiceAddressRequired(TypedDict):
    port: int
    addresses: List[IpLink]


class ServiceAddress(ServiceAddressRequired, total=False):
    pass


class OaasRegistry(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def register_service(
        self, service: ServiceDefinition, address: ServiceAddress
    ) -> None:
        ...

    @abc.abstractmethod
    def resolve_service(self, service: ServiceDefinition) -> Optional[ServiceAddress]:
        ...
