import unittest

from mopyx import render, render_call, model, action


@model
class RootModel:
    def __init__(self):
        self.name = "initial name"
        self.desc = "initial description"
        self.title = "initial title"


registered_events = []


class UiLabel:
    def __init__(self):
        self.label = None

    def set_label(self, label):
        registered_events.append("UiLabel.set_label")
        self.label = label


class UiComponent:
    def __init__(self, model):
        self.model = model

        self.name = UiLabel()
        self.description = UiLabel()
        self.title = None

        self.update_data()

    @render
    def update_data(self):
        registered_events.append("UiComponent.update_data")

        render_call(lambda: self.name.set_label(self.model.name))
        render_call(lambda: self.description.set_label(self.model.desc))

        self.title = self.model.title


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
        ]
        self.assertEqual(registered_events, main_rerender)


if __name__ == '__main__':
    unittest.main()

