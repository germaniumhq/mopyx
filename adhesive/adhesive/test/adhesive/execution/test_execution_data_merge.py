import unittest

from adhesive.execution.ExecutionData import ExecutionData


class TestExecutionData(unittest.TestCase):
    def test_process_data_merge(self):
        data1 = ExecutionData({
            "list": [1, 2, 3],
            "set": {"a", "b"},
            "dict": {
                "a": "a",
                "b": "b",
            },
            "number": 3,
            "to_remove": 1,
        })

        data2 = ExecutionData({
            "list": [4, 5, 6],
            "set": {"b", "c"},
            "dict": {
                "b": "b2",
                "c": "c",
            },
            "number": 1,
            "to_remove": None
        })

        result = ExecutionData.merge(data1, data2)

        self.assertEqual({
            "list": [4, 5, 6],  # same type, gets overwritten
            "set": {"a", "b", "c"},
            "dict": {
                "a": "a",
                "b": "b2", # keys are taken first from the 2nd object
                "c": "c",
            },
            "number": 1
        }, result.as_dict())
