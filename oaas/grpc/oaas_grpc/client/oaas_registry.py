from typing import Optional

import oaas
from oaas_registry_api import OaasRegistryStub
import os
import logging

LOG = logging.getLogger(__name__)


_oaas_registry: Optional[OaasRegistryStub] = None


def clear_registry():
    global _oaas_registry
    _oaas_registry = None


os.register_at_fork(after_in_child=clear_registry)


def oaas_registry() -> OaasRegistryStub:
    """
    Get a reference to the `oaas-registry`
    """
    global _oaas_registry

    if _oaas_registry:
        LOG.debug("oaas_registry() Using cached registry client")
        return _oaas_registry

    LOG.debug("oaas_registry() Using new registry client")
    _oaas_registry = oaas.get_client(OaasRegistryStub)  # type: ignore

    return _oaas_registry
