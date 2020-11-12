from typing import Dict, Optional

import oaas
import oaas.registry


@oaas.service("oaas-registry")
class OaasRegistryService(oaas.registry.OaasRegistry):
    # FIXME: externalize into its own package? or move to core OaaS?
    def __init__(self) -> None:
        self._services: Dict[str, oaas.registry.ServiceAddress] = dict()

    def resolve_service(
        self, service_definition: oaas.registry.ServiceDefinition
    ) -> Optional[oaas.registry.ServiceAddress]:
        return self._services.get(service_definition_key(service_definition), None)

    def register_service(
        self,
        service_definition: oaas.registry.ServiceDefinition,
        service_address: oaas.registry.ServiceAddress,
    ) -> None:
        self._services[service_definition_key(service_definition)] = service_address


def service_definition_key(service_definition: oaas.registry.ServiceDefinition) -> str:
    return (
        service_definition.get("protocol", "")
        + ":"
        + service_definition.get("namespace", "")
        + ":"
        + service_definition.get("name", "")
        + ":"
        + service_definition.get("version", "")
    )
