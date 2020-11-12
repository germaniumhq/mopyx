import os
import re

from oaas_registry_api.rpc.registry_pb2 import (
    OaasResolveServiceResponse,
    OaasServiceDefinition,
)

IP_PORT_ADDRESS = re.compile("^(.+)(:\d+)?$")


def find_registry() -> OaasResolveServiceResponse:
    if "OAAS_REGISTRY" in os.environ:
        return read_oaas_registry_from_environ()

    return create_static_search_list()


def read_oaas_registry_from_environ() -> OaasResolveServiceResponse:
    oaas_registry = os.environ["OAAS_REGISTRY"]

    return OaasResolveServiceResponse(
        services=[
            OaasServiceDefinition(
                namespace="default",
                name="oaas-registry",
                version="1",
                tags={"protocol": "grpc"},
                locations=[oaas_registry],
            )
        ]
    )


def create_static_search_list() -> OaasResolveServiceResponse:
    return OaasResolveServiceResponse(
        services=[
            OaasServiceDefinition(
                namespace="default",
                name="oaas-registry",
                version="1",
                tags={"protocol": "grpc"},
                locations=[
                    "localhost:8999",
                    # docker
                    "172.17.0.1:8999",
                    # kubernetes
                    "oaas-registry:8999",
                    "oaas-registry.oaas-registry.svc.cluster.local:8999",
                ],
            )
        ]
    )
