import logging
import sys
import signal

import oaas

# we import these two, to expose the oaas-registry service
from oaas_grpc.client.client import OaasGrpcClient
from oaas_grpc.server import OaasGrpcServer
from oaas_registry.oaas_grpc_registry import noop
from oaas_registry import registry_instance

noop()  # we have this function call so the optimize
# import keeps the registry definition

LOG = logging.getLogger(__name__)


def print_registered_services(a, b):
    registry_instance._print_registered_services()


def main():
    signal.signal(signal.SIGUSR1, print_registered_services)
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)

    oaas.register_server_provider(OaasGrpcServer())
    oaas.register_client_provider(OaasGrpcClient())

    oaas.serve()
    LOG.info("OaaS Registry listening on 8999")
    oaas.join()


if __name__ == "__main__":
    main()
