import unittest

from oaas_grpc.client.proxy import GrpcCallProxy, ProxyInstanceHandler


class FailingType:
    def call_method(self) -> str:
        raise Exception("broken")


class SucceedingType:
    def call_method(self) -> str:
        return "abc"


class TestInstanceHandler(ProxyInstanceHandler):
    def initial_instance(self):
        return FailingType()

    def call_error(self, oaas_grpc_proxy, oaas_grpc_exception, *args, **kw):
        oaas_grpc_proxy._delegate = SucceedingType()

        # the call should be retried
        return oaas_grpc_proxy._delegate

    def call_success(self):
        pass


class TestRetryStrategy(unittest.TestCase):
    def test_error_invocation(self) -> None:
        proxy = GrpcCallProxy(
            instance_handler=TestInstanceHandler(),
        )
        self.assertEqual("abc", proxy.call_method())
