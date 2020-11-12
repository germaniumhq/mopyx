import unittest

from oaas_grpc.client.proxy import GrpcCallProxy, ProxyInstanceHandler


class SimpleObject:
    def simple_call(self):
        return "abc"


class TestInstanceHandler(ProxyInstanceHandler):
    def initial_instance(self):
        return SimpleObject()

    def call_error(self, oaas_grpc_proxy, oaas_grpc_exception, *args, **kw):
        pass

    def call_success(self):
        pass


class TestDelegateMethod(unittest.TestCase):
    def test_delegate_methods_are_shared(self):
        proxy = GrpcCallProxy(instance_handler=TestInstanceHandler())
        self.assertIs(proxy.simple_call, proxy.simple_call)

    def test_delegate_methods_can_be_called(self):
        proxy = GrpcCallProxy(instance_handler=TestInstanceHandler())
        self.assertEqual("abc", proxy.simple_call())
