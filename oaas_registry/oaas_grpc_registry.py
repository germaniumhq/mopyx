import oaas
from oaas_registry_api.rpc.registry_pb2 import (
    OaasServiceDefinition,
    OaasResolveServiceResponse,
    OaasServiceId,
    OaasUnregisterServiceResponse,
)
from oaas_registry_api.rpc.registry_pb2_grpc import OaasRegistryServicer

from oaas_registry import registry_instance


@oaas.service("oaas-registry")
class OaasGrpcRegistry(OaasRegistryServicer):
    def register_service(
        self, request: OaasServiceDefinition, context
    ) -> OaasServiceDefinition:
        result = registry_instance.register_service(
            namespace=request.namespace,
            name=request.name,
            version=request.version,
            tags=request.tags,
            locations=request.locations,
        )

        return OaasServiceDefinition(
            id=result.id,
            namespace=result.namespace,
            name=result.name,
            version=result.version,
            tags=result.tags,
            locations=result.locations,
        )

    def resolve_service(
        self, request: OaasServiceDefinition, context
    ) -> OaasResolveServiceResponse:
        result = registry_instance.resolve_service(
            id=request.id,
            namespace=request.namespace,
            name=request.name,
            version=request.version,
            tags=request.tags,
        )

        return OaasResolveServiceResponse(
            services=[
                OaasServiceDefinition(
                    id=it.id,
                    namespace=it.namespace,
                    name=it.name,
                    version=it.version,
                    tags=it.tags,
                    locations=it.locations,
                )
                for it in result
            ]
        )

    def unregister_service(
        self, request: OaasServiceId, context
    ) -> OaasUnregisterServiceResponse:
        result = registry_instance.unregister_service(id=request.id)
        return OaasUnregisterServiceResponse(result=result)


def noop():
    """
    This function exists only for the automatic imports not to remove
    the import to this module, that registers the OaaSRegistry service
    """
    return None
