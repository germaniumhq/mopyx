from typing import Callable, TypeVar, Type, Optional, Dict, Any

import oaas._registrations as registrations
from oaas.client_definition import ClientDefinitionMetadata, ClientDefinition
from oaas.client_provider import ClientMiddleware
from oaas.server_provider import ServerMiddleware
from oaas.service_definition import ServiceDefinition, ServiceDefinitionMetadata

import collections

T = TypeVar("T")
_dynamic_registrations: Dict[str, ServerMiddleware] = dict()


def client(
    name: str,
    namespace: str = "default",
    version: str = "1",
    tags: Dict[str, str] = None,
) -> Callable[..., Type[T]]:
    """
    Declare a service from the system. All the input and output data
    should be serializable. The serialization format depends on
    the provider being used. To get an instance to the client, call
    `get_client`.
    """

    def wrapper_builder(t: Type[T]) -> Type[T]:
        cd = ClientDefinition(
            name=name,
            namespace=namespace,
            version=version,
            code=t,
            tags=tags,
        )
        registrations.clients[t] = cd

        return t

    return wrapper_builder


def service(
    name: str,
    *,
    namespace: str = "default",
    version: str = "1",
    tags: Optional[Dict[str, str]] = None,
) -> Callable[..., Type[T]]:
    """
    Mark a service to be exposed to the system. All the input
    and output data should be serializable. The serialization
    format depends on the provider being used.
    """

    def wrapper_builder(t: Type[T]) -> Type[T]:
        sd = ServiceDefinition(
            namespace=namespace,
            name=name,
            version=version,
            code=t,
            tags=tags,
        )
        registrations.services.append(sd)

        return t

    return wrapper_builder


def publish(
    *,
    instance: Any,
    name: str,
    namespace: str = "default",
    version: str = "1",
    tags: Optional[Dict[str, str]] = None,
) -> str:
    for server_middleware in registrations.servers_middleware:
        if server_middleware.can_publish(instance=instance):
            instance_id = server_middleware.publish(
                instance=instance,
                name=name,
                namespace=namespace,
                version=version,
                tags=tags,
            )

            _dynamic_registrations[instance_id] = server_middleware
            return instance_id

    raise Exception(
        f"No middleware can publish {instance}. Register "
        f"the middleware first using oaas.register_server_provider(m)"
    )


def unpublish(
    *,
    id: str,
) -> None:
    if not id in _dynamic_registrations:
        raise Exception("Service wasn't pushed as a dynamic service.")

    middleware = _dynamic_registrations[id]
    middleware.unpublish(id=id)

    del _dynamic_registrations[id]


def serve() -> None:
    """
    Expose all the defined services using the underlying
    providers.
    """
    services_without_middleware = set()

    for service_definition in registrations.services:
        if not _has_server_middleware(service_definition):
            services_without_middleware.add(service_definition)

    if services_without_middleware:
        raise Exception(
            "Some services have no backing middleware. Make sure the "
            "middleware servers are added using oaas.register_server_provider() "
            f"before calling serve(): {services_without_middleware}"
        )

    for provider in registrations.servers_middleware:
        provider.serve()


def _has_server_middleware(service_definition) -> bool:
    for provider in registrations.servers_middleware:
        if provider.can_serve(service_definition):
            return True

    return False


def join() -> None:
    """
    Wait for all the defined servers to come down.
    """
    for provider in registrations.servers_middleware:
        provider.join()


def get_client(t: Type[T], **tags: str) -> T:
    """
    Create a client for the given type.
    """
    for provider in registrations.clients_middleware:
        if t not in registrations.clients:
            raise Exception(
                f"Type {t} was not registered using @oaas.client(). You "
                f"need to register first the client using @oaas.client() "
                f"either as oaas.client('service-name')(GrpcTypeStub) or "
                f"decorate the Simple service with @oaas.client."
            )

        client_definition = registrations.clients[t]
        if provider.can_handle(client_definition):
            retagged_client_definition = _merge_tags(client_definition, tags)
            return provider.create_client(retagged_client_definition)

    raise Exception(
        f"No serialization provider was registered to handle " f"{t} clients."
    )


def register_server_provider(server_middleware: ServerMiddleware):
    """
    Register a serialization provider. Normally this should be taken
    care by the middleware.
    """
    registrations.servers_middleware.add(server_middleware)


def register_client_provider(client_middleware: ClientMiddleware):
    """
    Register a serialization provider. Normally this should be taken
    care by the middleware.
    """
    registrations.clients_middleware.add(client_middleware)


def _merge_tags(
    client_definition: ClientDefinition, tags: Optional[Dict[str, str]]
) -> ClientDefinition:
    """
    Merge the extra tags in a new client definition.
    """
    if not tags:
        return client_definition

    if client_definition.tags:
        merged_tags = dict(client_definition.tags)
        merged_tags.update(tags)
    else:
        merged_tags = tags

    result = ClientDefinition(
        namespace=client_definition.namespace,
        name=client_definition.name,
        version=client_definition.version,
        code=client_definition.code,
        tags=merged_tags,
    )

    return result
