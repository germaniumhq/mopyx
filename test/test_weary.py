import unittest
from typing import List
from unittest import TestCase

import weary

# generated
from weary import WearyContext


@weary.model
class TestEnvironment:
    @property
    def name(self) -> str:
        raise Exception("No provider for TestEnvironment.name")


# generated
@weary.model
class ApplicationModel:
    @property
    def versions(self) -> List[str]:
        raise Exception("No provider for ApplicationModel.versions")

    @property
    def environments(self) -> List[TestEnvironment]:
        raise Exception("No provider for ApplicationModel.environments")


call_count = 0


# user
@weary.property(ApplicationModel, "environments")
def resolve_environments_property(
    self: ApplicationModel, context: WearyContext
) -> List[TestEnvironment]:
    global call_count
    call_count += 1

    return []


# user
@weary.property(ApplicationModel, "versions")
def resolve_versions_property(
    self: ApplicationModel, context: WearyContext
) -> List[str]:
    return ["1", "2", "3"]


class TestWearyPropertyResolving(TestCase):
    def test_resolve_property(self):
        app = ApplicationModel()

        self.assertEqual(["1", "2", "3"], app.versions)

    def test_caching(self):
        app = ApplicationModel()
        self.assertEqual([], app.environments)
        self.assertEqual([], app.environments)
        self.assertEqual(1, call_count)

    def test_constructor_overrides_property(self):
        app = ApplicationModel(versions=["a", "b", "c"])
        self.assertEqual(["a", "b", "c"], app.versions)

    @unittest.expectedFailure
    def test_wrong_property_in_constructor_raises_exception(self):
        ApplicationModel(appversions=["a", "b", "c"])
