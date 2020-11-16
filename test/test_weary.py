import types
from typing import List
from unittest import TestCase

import weary


# generated
@weary.model
class TestEnvironment:
    @property
    def name(self) -> str:
        raise Exception("No provider for TestEnvironment.name")


# generated
@weary.model
class ApplicationModel:
    def __init__(self) -> None:
        pass

    @property
    def versions(self) -> List[str]:
        raise Exception("No provider for ApplicationModel.versions")

    @property
    def environments(self) -> List[TestEnvironment]:
        raise Exception("No provider for ApplicationModel.environments")

    @classmethod
    def _setmethod(cls, fname, f):
        setattr(cls, fname, types.DynamicClassAttribute(f, cls))


# user
@weary.property(ApplicationModel, "environments")
def resolve_property(self: ApplicationModel) -> List[TestEnvironment]:
    pass


# user
@weary.property(ApplicationModel, "versions")
def resolve_property(self: ApplicationModel) -> List[str]:
    return ["1", "2", "3"]


class TestWearyPropertyResolving(TestCase):
    def test_resolve_property(self):
        app = ApplicationModel()

        self.assertEqual(["1", "2", "3"], app.versions)
