from typing import Optional, Dict, TypeVar, Type

import logging

import grpc
from grpc import Channel
from oaas_grpc.client import registry_discovery
from oaas_grpc.client.connection_test import is_someone_listening
from oaas_grpc.client.oaas_registry import oaas_registry
from oaas_grpc.client.proxy import ProxyInstanceHandler
from oaas_registry_api.rpc.registry_pb2 import (
    OaasServiceDefinition,
    OaasResolveServiceResponse,
    OaasServiceId,
)

LOG = logging.getLogger(__name__)

T = TypeVar("T")


def is_unavailable_service(oaas_grpc_exception):
    if not hasattr(oaas_grpc_exception, "args"):
        return False

    if not oaas_grpc_exception.args:
        return False

    if oaas_grpc_exception.args[0].code == grpc.StatusCode.UNAVAILABLE:
        return True

    return False


class GrpcProxyInstanceHandler(ProxyInstanceHandler):
    def __init__(
        self,
        *,
        namespace: str,
        name: str,
        version: str,
        tags: Optional[Dict[str, str]],
        code: Type[T],
    ):
        self.namespace = namespace
        self.name = name
        self.version = version
        self.tags = tags
        self.code = code

        self._failed_tries = 0

    def initial_instance(self):
        # the ooas-registry is only hosted on the grpc
        if (
            self.namespace == "default"
            and self.name == "oaas-registry"
            and self.version == "1"
        ):
            resolve_response = registry_discovery.find_registry()
        else:
            LOG.debug(
                f"=> resolve service %s:%s:%s", self.namespace, self.name, self.version
            )
            resolve_response = oaas_registry().resolve_service(
                OaasServiceDefinition(
                    namespace=self.namespace,
                    name=self.name,
                    version=self.version,
                    tags=self.tags,
                )
            )
            LOG.debug(
                f"<= resolve service %s:%s:%s", self.namespace, self.name, self.version
            )

        LOG.debug("=> find_channel")
        channel = self.find_channel(
            resolve_response=resolve_response,
            gav_service_name=f"{self.namespace}:{self.name}:{self.version}",
            tags=self.tags,
        )
        LOG.debug(f"<= find_channel %s", channel)

        return self.code(channel=channel)

    def call_error(self, oaas_grpc_proxy, oaas_grpc_exception, *args, **kw):
        # FIXME: this should recreate the instance only if the call is a grpc unavailable
        # exception.
        if not is_unavailable_service(oaas_grpc_exception) or self._failed_tries >= 5:
            self._failed_tries = 0
            raise oaas_grpc_exception

        self._failed_tries += 1

        try:
            oaas_grpc_proxy._delegate = self.initial_instance()
        except Exception as e:
            # recreating the instance failed for whatever reason, we can't retry
            # anymore.
            self._failed_tries = 0
            raise oaas_grpc_exception

        return oaas_grpc_proxy._delegate

    def call_success(self):
        self._failed_tries = 0

    def find_channel(
        self,
        *,
        resolve_response: OaasResolveServiceResponse,
        gav_service_name: str,
        tags: Optional[Dict[str, str]],
    ) -> Channel:
        if not resolve_response.services:
            raise Exception(
                f"No service registered for {gav_service_name} and tags {tags}"
            )

        for service_definition in resolve_response.services:
            for location in service_definition.locations:
                if is_someone_listening(location):
                    channel = grpc.insecure_channel(location)

                    return channel

            # none of the locations for that definition were accessible
            # unregister the service by the client.
            # FIXME: make unregistering by clients configurable
            # FIXME: shoulnd't have hardcoded values on _instance_id, but types
            oaas_registry().unregister_service(OaasServiceId(id=service_definition.id))

        raise Exception(
            f"Unable to find any listening service on any of the "
            f"locations for {gav_service_name}."
        )
