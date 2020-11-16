from typing import List
from unittest import TestCase

import weary


# generated
@weary.model
class TestEnvironment:
    def name(self) -> str:
        pass


# generated
@weary.model
class ApplicationModel:
    def __init__(self) -> None:
        pass

    def versions(self) -> List[str]:
        pass

    def environments(self) -> List[TestEnvironment]:
        pass


# user
@weary.property(ApplicationModel, "environments")
def resolve_property(self: ApplicationModel, context) -> List[TestEnvironment]:
    pass


# user
@weary.property(ApplicationModel, "versions")
def resolve_property(self: ApplicationModel, context) -> List[str]:
    return ["1", "2", "3"]


class TestWearyPropertyResolving(TestCase):
    def test_resolve_property(self):
        app = ApplicationModel()

        self.assertEqual(["1", "2", "3"], app.versions())
