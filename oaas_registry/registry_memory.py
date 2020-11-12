import functools
import uuid
from typing import Dict, Iterable, Callable, TypeVar, Optional

from countertype import CounterType
from readerwriterlock import rwlock

from oaas_registry.registry import Registry
from oaas_registry.service_definition import ServiceDefinition

T = TypeVar("T")


def write_lock(f: Callable[..., T]) -> Callable[..., T]:
    @functools.wraps(f)
    def wrapper(*args, **kw) -> T:
        self = args[0]
        try:
            self._wlock.acquire()
            return f(*args, **kw)
        finally:
            self._wlock.release()

    return wrapper


def read_lock(f: Callable[..., T]) -> Callable[..., T]:
    @functools.wraps(f)
    def wrapper(*args, **kw) -> T:
        self = args[0]
        try:
            self._rlock.acquire()
            return f(*args, **kw)
        finally:
            self._rlock.release()

    return wrapper


class RegistryMemory(Registry):
    def __init__(self) -> None:
        self._services: CounterType[ServiceDefinition] = CounterType()
        self._rwlock = rwlock.RWLockFair()
        self._wlock = self._rwlock.gen_wlock()
        self._rlock = self._rwlock.gen_rlock()

    @write_lock
    def register_service(
        self,
        *,
        protocol: str = "grpc",
        namespace: str = "default",
        name: str,
        version: str = "1",
        tags: Dict[str, str],
        locations: Iterable[str],
    ) -> ServiceDefinition:

        instance_id = str(uuid.uuid4())

        sd = ServiceDefinition(
            id=instance_id,
            protocol=protocol,
            namespace=namespace,
            name=name,
            version=version,
            locations=locations,
            tags=tags,
        )

        gav = f"{protocol}:{namespace}:{name}:{version}"

        self._services.put(
            sd,
            id=instance_id,
            gav=gav,
            **tags,
        )

        return sd

    @read_lock
    def resolve_service(
        self,
        *,
        id: Optional[str] = None,
        protocol: str = "grpc",
        namespace: str = "default",
        name: str,
        version: str = "1",
        tags: Dict[str, str],
    ) -> Iterable[ServiceDefinition]:
        gav = f"{protocol}:{namespace}:{name}:{version}"

        if id:
            return self._services.find_all(
                id=id,
                gav=gav,
                **tags,
            )

        return self._services.find_all(
            gav=gav,
            **tags,
        )

    @write_lock
    def unregister_service(self, *, id: str) -> bool:
        existing_object = self._services.remove(id=id)

        if existing_object:
            return True

        return False

    @read_lock
    def _print_registered_services(self) -> None:
        print("Services:")
        for service in self._services.find_all():
            print(service)
