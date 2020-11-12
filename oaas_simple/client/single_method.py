from typing import Any

from oaas import ClientDefinition

from oaas_simple.data import create_data, from_data
from oaas_simple.rpc import call_pb2


class SingleMethod:
    def __init__(
        self, *, stub: Any, client_definition: ClientDefinition, method_name: str
    ):
        self.stub = stub
        self.client_definition = client_definition
        self.method = method_name

    def __call__(self, *args, **kwargs):
        parameters = []

        for arg in args:
            param = call_pb2.ServiceCallParam(name=None, data=create_data(arg))
            parameters.append(param)

        for arg_name, arg in kwargs.items():
            param = call_pb2.ServiceCallParam(name=arg_name, data=create_data(arg))
            parameters.append(param)

        response: call_pb2.Data = self.stub.InvokeMethod(
            call_pb2.ServiceCall(  # ignore: type
                namespace=self.client_definition.namespace,
                service=self.client_definition.name,
                version=self.client_definition.version,
                method=self.method,
                parameters=parameters,
            )
        )

        return from_data(response)
