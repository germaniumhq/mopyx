import oaas

from oaas_registry_api.rpc.registry_pb2_grpc import OaasRegistryStub

oaas.client("oaas-registry")(OaasRegistryStub)
