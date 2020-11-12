from typing import Any, Optional, Dict

from oaas_grpc.server import OaasGrpcServer
from oaas_grpc.server.find_ips import find_ips
from oaas_registry_api import OaasRegistryStub
from oaas_registry_api.rpc.registry_pb2 import OaasServiceDefinition
from oaas_simple.server.service_invoker_proxy import noop

import oaas

noop()


class OaasSimpleServer(oaas.ServerMiddleware):
    def __init__(self, *, port=8999):
        super(OaasSimpleServer, self).__init__()

        self._grpc_server = OaasGrpcServer(port=port)
        self.port = port

    def serve(self) -> None:
        # we ensure we're serving with the gRPC server first
        self._grpc_server.serve()

        # we can get the registry only after the server is servicing
        # in case this _is_ the registry.
        registry = oaas.get_client(OaasRegistryStub)

        # we register the services
        locations = find_ips(port=self.port)
        for service_definition in oaas.registrations.services:
            if self._grpc_server.can_serve(service_definition=service_definition):
                continue

            print(
                f"Added SIMPLE service: {service_definition.gav} as {service_definition.code}"
            )

            registry.register_service(
                OaasServiceDefinition(
                    namespace=service_definition.namespace,
                    name=service_definition.name,
                    version=service_definition.version,
                    tags={
                        "_protocol": "simple",
                    },
                    locations=locations,
                )
            )

    def join(self) -> None:
        self._grpc_server.join()

    def can_serve(self, service_definition: oaas.ServiceDefinition) -> bool:
        # We can serve both gRPC, and simple services, since we embed both
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
            f"Simple service middleware can't dynamically publish services. "
            f"Can't serve service {instance}"
        )

    def unpublish(self, id: str) -> None:
        raise Exception(
            "Simple service middleware can't dynamically unpublish services"
        )
