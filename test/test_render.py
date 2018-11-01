import unittest

from mopyx import render, render_call, model, action


@model
class RootModel:
    def __init__(self):
        self.name = "initial name"
        self.desc = "initial description"
        self.title = "initial title"
        self.items = ["a", "b", "c"]


registered_events = []


class UiLabel:
    def __init__(self):
        self.label = None

    def set_label(self, label):
        registered_events.append("UiLabel.set_label")
        self.label = label


class UiTable:
    def __init__(self):
        self.table_items = []

    def clear(self):
        self.table_items.clear()

    def add_item(self, item):
        self.table_items.append(item)


class UiComponent:
    def __init__(self, model):
        self.model = model

        self.name = UiLabel()
        self.description = UiLabel()
        self.items_table = UiTable()
        self.title = None

        self.update_data()

    @render
    def update_data(self):
        registered_events.append("UiComponent.update_data")

        render_call(lambda: self.name.set_label(self.model.name))
        render_call(lambda: self.description.set_label(self.model.desc))

        self.update_table()

        self.title = self.model.title

    @render
    def update_table(self):
        registered_events.append("UiComponent.update_table")

        self.items_table.clear()
        for item in self.model.items:
            self.items_table.add_item(item)


class TestRender(unittest.TestCase):
    """
    Test the @render decorator.
    """

    def test_render_function(self):
        """
        Will create a test rendering, and change properties.
        """
        model = RootModel()
        ui = UiComponent(model)

        self.assertEqual(model.name, ui.name.label)
        self.assertEqual(model.desc, ui.description.label)
        self.assertEqual(model.items, ui.items_table.table_items)

        model.name = "updated name"
        model.desc = "updated description"

        self.assertEqual(model.name, "updated name")
        self.assertEqual(model.desc, "updated description")

        self.assertEqual(model.name, ui.name.label)
        self.assertEqual(model.desc, ui.description.label)

        basic_rerender = [
            'UiComponent.update_data',
            'UiLabel.set_label',
            'UiLabel.set_label',
            'UiComponent.update_table',
            'UiLabel.set_label',
            'UiLabel.set_label',
        ]
        self.assertEqual(registered_events, basic_rerender)

        registered_events.clear()

        @action
        def custom_action():
            model.name = "new name"
            model.title = "new title"

        custom_action()

        main_rerender = [
            'UiComponent.update_data',
            'UiLabel.set_label',
            'UiLabel.set_label',
            'UiComponent.update_table'
        ]
        self.assertEqual(registered_events, main_rerender)

        registered_events.clear()

        model.items.append("x")
        self.assertEqual(model.items, ui.items_table.table_items)

        table_renderer = [
            'UiComponent.update_table'
        ]
        self.assertEqual(registered_events, table_renderer)


if __name__ == '__main__':
    unittest.main()

