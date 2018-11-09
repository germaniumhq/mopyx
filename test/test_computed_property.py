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
                self.items = []

            @computed
            def sumation(self):
                registered_events.append("Sumator.sumation")
                return sum(self.items)

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
            "Sumator.sumation",
            "SumatorUi.update_label",
        ]

        self.assertEqual(initial_events, registered_events)
        registered_events = []

        m.items = [1, 2, 3]
        self.assertEqual("sum is 6", ui.label)
        self.assertEqual(6, m.sumation)

        items_update_events = [
            "Sumator.sumation",
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


if __name__ == '__main__':
    unittest.main()
