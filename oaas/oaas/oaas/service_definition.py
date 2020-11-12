from typing import Dict, Optional, Any, TypeVar, Type

ServiceDefinitionMetadata = Dict[str, Any]
T = TypeVar("T")


class ServiceDefinition:
    def __init__(
        self,
        *,
        namespace: str = "default",
        name: str,
        version: str = "1",
        code: Type[T],
        tags: Optional[Dict[str, str]] = None,
    ) -> None:
        self.namespace = namespace
        self.name = name
        self.version = version
        self.code = code
        self.tags = tags

    @property
    def gav(self) -> str:
        return f"{self.namespace}:{self.name}:{self.version}"
