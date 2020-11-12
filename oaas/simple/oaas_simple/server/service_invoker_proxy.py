from typing import Any, Dict

import oaas_simple.server.server
from oaas_simple.data import from_data, create_data
from oaas_simple.rpc import call_pb2
from oaas_simple.rpc import call_pb2_grpc

import oaas._registrations as registrations
from oaas import service


@service("service-invoker-proxy")
class ServiceInvokerProxy(call_pb2_grpc.ServiceInvokerServicer):
    def __init__(self) -> None:
        self._service_instances: Dict[str, Any] = dict()

        server = find_simple_server()

        # we only register the non grpc services as simple services
        for service_definition in registrations.services:
            if server._grpc_server.can_serve(service_definition):
                continue

            self._service_instances[service_definition.name] = service_definition.code()

    """
    Invokes the service on this server.
    """

    def InvokeMethod(self, request: call_pb2.ServiceCall, context) -> call_pb2.Data:  # type: ignore
        service_instance = self._service_instances[request.service]  # type: ignore

        service_method = getattr(service_instance, request.method)  # type: ignore

        args = []
        kw = {}

        for param in request.parameters:  # type: ignore
            value = from_data(param.data)

            if param.name:
                kw[param.name] = value
            else:
                args.append(value)

        result = service_method(*args, **kw)

        return create_data(result)


def find_simple_server():
    for server in registrations.servers_middleware:
        if isinstance(server, oaas_simple.server.server.OaasSimpleServer):
            return server

    raise Exception("No OaasSimpleServer was registered")


def noop():
    pass
