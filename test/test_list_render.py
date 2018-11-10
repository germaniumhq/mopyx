from mopyx import model, render_call
import unittest


@model
class RootModel:
    def __init__(self):
        self.items = list()


class TestListRender(unittest.TestCase):
    """
    Just a basic test if lists are correctly triggering
    changes.
    """

    def test_if_lists_update_correctly(self):
        """
        Test if a list can do multiple appends.
        """
        root_model = RootModel()
        list_length = [0]
        registered_events = []

        @render_call
        def update_length():
            registered_events.append('update_length')
            list_length[0] = len(root_model.items)

        self.assertEqual(['update_length'], registered_events)
        registered_events.clear()

        root_model.items.clear()  # clearing an empty list shouldn't trigger events
        self.assertEqual([], registered_events)
        registered_events.clear()

        self.assertEqual(0, list_length[0])
        root_model.items.append(1)
        self.assertEqual(1, list_length[0])
        root_model.items.append(1)
        self.assertEqual(2, list_length[0])

        root_model.items = []

        self.assertEqual(0, list_length[0])
        root_model.items.append(1)
        self.assertEqual(1, list_length[0])
        root_model.items.append(1)
        self.assertEqual(2, list_length[0])


if __name__ == '__main__':
    unittest.main()
