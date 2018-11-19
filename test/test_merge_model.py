from mopyx.util import merge_model
from mopyx import model, render_call

import unittest


@model
class CustomModel:
    def __init__(self, value):
        self.value = value


@model
class RootModel:
    def __init__(self) -> None:
        self.list_basic_strings = ["a", "b", "c"]
        self.list_changed_strings = ["A", "B", "C"]
        self.basic_value = 5
        self.changed_value = 7
        self.custom_value = CustomModel(3)
        self.custom_changed = CustomModel(5)
        self.custom_list = CustomModel(["al", "bl", "cl"])
        self.custom_list_changed = CustomModel(["alc", "blc", "clc"])
        self.custom_nested_list = CustomModel([CustomModel(["cnl"])])
        self.custom_nested_list_changed = CustomModel([CustomModel(["cnlc"])])
        self.none_property = None


class TestMergeModel(unittest.TestCase):
    def test_merge_model(self):
        root_model = RootModel()
        changed_model = RootModel()

        registered_events = set()

        @render_call
        def list_basic_strings():
            root_model.list_basic_strings
            registered_events.add("list_basic_strings")

        @render_call
        def list_changed_strings():
            root_model.list_changed_strings
            registered_events.add("list_changed_strings")

        @render_call
        def basic_value():
            root_model.basic_value
            registered_events.add("basic_value")

        @render_call
        def changed_value():
            root_model.changed_value
            registered_events.add("changed_value")

        @render_call
        def custom_value():
            root_model.custom_value
            registered_events.add("custom_value")

        @render_call
        def custom_changed():
            root_model.custom_changed.value
            registered_events.add("custom_changed")

        @render_call
        def custom_list():
            root_model.custom_list
            registered_events.add("custom_list")

        @render_call
        def custom_list_changed():
            root_model.custom_list_changed.value[1]
            registered_events.add("custom_list_changed")

        @render_call
        def custom_nested_list():
            root_model.custom_nested_list
            registered_events.add("custom_nested_list")

        @render_call
        def custom_nested_list_changed():
            root_model.custom_nested_list_changed.value[0].value
            registered_events.add("custom_nested_list_changed")

        @render_call
        def none_property():
            root_model.none_property
            registered_events.add("none_property")

        registered_events.clear()

        changed_model.list_changed_strings[2] = "D"
        changed_model.changed_value = 9
        changed_model.custom_changed.value = 9
        changed_model.custom_list_changed.value[1] = "3"
        changed_model.custom_nested_list_changed.value[0].value.append("1")

        merge_model(root_model, changed_model)

        self.assertEqual({
            "list_changed_strings",
            "changed_value",
            "custom_changed",
            "custom_list_changed",
            "custom_nested_list_changed",
        }, registered_events)


if __name__ == '__main__':
    unittest.main()
