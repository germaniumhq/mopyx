import unittest
from mopyx import model, action


@model
class Model:
    def __init__(self):
        self.count = 0

    @action
    def increment(self):
        self.count += 1


class TestActionOnModel(unittest.TestCase):

    def test_action_on_model(self):
        root_model = Model()

        self.assertEqual(0, root_model.count)
        root_model.increment
        self.assertEqual(0, root_model.count)

        root_model.increment()
        self.assertEqual(1, root_model.count)


if __name__ == '__main__':
    unittest.main()
