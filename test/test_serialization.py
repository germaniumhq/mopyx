from typing import List
import json
import unittest

from mopyx import model


@model
class Model:
    def __init__(self):
        self.name: str = "name"
        self.items: List[str] = ["a", "b", "c"]


class NonDecoratedModel:
    def __init__(self):
        self.name: str = "name"
        self.items: List[str] = ["a", "b", "c"]


class TestSerialization(unittest.TestCase):
    """
    Tests the model serialization
    """

    def test_serialization(self):
        """
        Checks if a model being serialized will also yield the
        mopyx properties.
        """
        self.assertEqual(json.dumps(NonDecoratedModel().__dict__, sort_keys=True),
                         json.dumps(Model().__dict__, sort_keys=True))


if __name__ == '__main__':
    unittest.main()
