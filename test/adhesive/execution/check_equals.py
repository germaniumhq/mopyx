from typing import Dict, Set

import unittest

test = unittest.TestCase()
test.maxDiff = None


def assert_equal_execution(expected: Dict[str, int],
                           actual: Dict[str, Set[str]]) -> None:
    test.assertSetEqual(set(expected.keys()), set(actual.keys()))
    actual_dict = dict()

    for k, v in actual.items():
        actual_dict[k] = len(v)

    test.assertDictEqual(expected, actual_dict)
