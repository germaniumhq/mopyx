import unittest

from oaas_registry.registry_memory import RegistryMemory


class RegistryTest(unittest.TestCase):
    def test_two_node_registrations(self):
        registry = RegistryMemory()

        sd1 = registry.register_service(
            name="abc",
            version="1",
            tags={
                "_protocol": "grpc",
                "instance": "sd1",
            },
            locations=[
                "localhost:8080",
                "192.168.0.1:8080",
            ],
        )

        sd2 = registry.register_service(
            name="abc",
            version="1",
            tags={
                "_protocol": "grpc",
                "instance": "sd2",
            },
            locations=[
                "localhost:8080",
                "192.168.0.2:8080",
            ],
        )

        services = registry.resolve_service(
            name="abc", version="1", tags={"_protocol": "grpc"}
        )

        self.assertTrue(sd1 in services)
        self.assertTrue(sd2 in services)

        services = registry.resolve_service(
            name="abc", version="1", tags={"_protocol": "grpc", "instance": "sd2"}
        )

        self.assertTrue(sd1 not in services)
        self.assertTrue(sd2 in services)

        registry.unregister_service(id=sd2.id)

        services = registry.resolve_service(
            name="abc", version="1", tags={"_protocol": "grpc"}
        )

        self.assertTrue(
            sd1 in services,
            msg="sd1 should still be in the services list, since only "
            "sd2 was removed",
        )
        self.assertTrue(
            sd2 not in services,
            msg="sd2 was removed, so it shouldn't be findable " "anymore",
        )

        registry.unregister_service(id=sd1.id)

        services = registry.resolve_service(
            name="abc", version="1", tags={"_protocol": "grpc"}
        )

        self.assertTrue(
            sd1 not in services,
            msg="sd1 was removed, so it shouldn't be findable " "anymore",
        )
        self.assertTrue(
            sd2 not in services,
            msg="sd2 was removed, so it shouldn't be findable " "anymore",
        )
