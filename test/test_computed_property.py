from mopyx import model, computed, render

import unittest


class TestComputedDecorator(unittest.TestCase):
    """
    Simple test to see if computed gets calculated correctly.
    """

    def test_computed_decorator(self):
        registered_events = []

        @model
        class Sumator:
            def __init__(self):
                self.label = "sum is"
                self.other = "other"
                self.items = []

            @computed
            def sumation(self):
                registered_events.append("Sumator.sumation")

                # This should register the current sumation as a listener
                # for self.other changes via the renderer
                self.other

                # We update the same value with a new value. This should
                # not trigger the listener, since that would be an
                # infinite loop.
#                self.other = "other test"

                return sum(self.items)

            @computed
            def nested_sumation(self):
                registered_events.append("Sumator.nested_sumation")

                return f"{self.sumation} sum"

        class SumatorUi:
            def __init__(self, model):
                self.label = ""
                self.model = model

                self.update_label()

            @render
            def update_label(self):
                registered_events.append("SumatorUi.update_label")
                self.label = f"{self.model.label} {self.model.sumation}"

        """
        Just a basic sumator test
        """
        m = Sumator()
        ui = SumatorUi(m)

        initial_events = [
            "Sumator.nested_sumation",
            "Sumator.sumation",
            "SumatorUi.update_label",
        ]

        self.assertEqual(initial_events, registered_events)
        registered_events = []

        m.items = [1, 2, 3]
        self.assertEqual("sum is 6", ui.label)
        self.assertEqual(6, m.sumation)
        self.assertEqual("6 sum", m.nested_sumation)

        items_update_events = [
            "Sumator.sumation",
            "Sumator.nested_sumation",
            "SumatorUi.update_label",
        ]
        self.assertEqual(items_update_events, registered_events)
        registered_events = []

        m.label = "sumation is"
        self.assertEqual("sumation is 6", ui.label)
        self.assertEqual(6, m.sumation)

        label_update_events = [
            "SumatorUi.update_label"
        ]
        self.assertEqual(label_update_events, registered_events)

        m.items.append(4)
        self.assertEqual("10 sum", m.nested_sumation)


if __name__ == '__main__':
    unittest.main()
