from typing import Dict, Iterable, Optional


class ServiceDefinition:
    def __init__(
        self,
        *,
        id: Optional[str] = None,
        namespace: str = "default",
        name: str,
        version: str = "1",
        protocol: str = "grpc",
        tags: Dict[str, str],
        locations: Iterable[str],
    ) -> None:
        self.id = id
        self.protocol = protocol
        self.namespace = namespace
        self.name = name
        self.version = version
        self.tags = tags
        self.locations = locations

    def __repr__(self) -> str:
        return f"svc:{self.protocol}:{self.namespace}:{self.name}:{self.version} tags: {self.tags}"
