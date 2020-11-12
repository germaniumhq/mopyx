import oaas

from oaas_simple.registry.local_registry import OaasRegistryService
from oaas_simple.server.server import OaasSimpleServer

# noop on purpose, just to register it
dir(OaasRegistryService)

server_instance = OaasSimpleServer()
oaas.register_server_provider(server_instance)

oaas.serve()
print(f"OaaS Simple Registry started on port {server_instance.port}.")
oaas.join()
