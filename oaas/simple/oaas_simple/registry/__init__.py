from typing import Optional

import oaas
import oaas.registry


@oaas.client("oaas-registry")
class OaasRegistry(oaas.registry.OaasRegistry):
    ...


_oaas_registry: Optional[OaasRegistry] = None


def oaas_registry() -> OaasRegistry:
    global _oaas_registry

    if _oaas_registry:
        return _oaas_registry

    _oaas_registry = oaas.get_client(OaasRegistry)  # type: ignore

    return _oaas_registry
