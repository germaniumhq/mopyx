from typing import List
from mopyx import model, render, render_call, action

import unittest


@model
class TreeNode:
    def __init__(self, name: str) -> None:
        self.selected = True
        self.name = name
        self.children: List['TreeNode'] = []


class TreeWidgetNode:
    def __init__(self):
        self.label: str = ""
        self.checked = True
        self.children: List['TreeWidgetNode'] = []


class TestNestedRender(unittest.TestCase):
    """
    A simple "tree" test.
    """

    def test_nested_render(self):
        """
        Test if tree rendering works correctly.
        """
        model = TreeNode("root")
        child1 = TreeNode("child1")
        model.children.append(child1)
        child2 = TreeNode("child2")
        model.children.append(child2)

        @render
        def render_widget_item(parent_node, node, item):
            def update_labels():
                node.label = item.name
                node.checked = item.selected

            render_call(update_labels, ignore_updates=True)

            if parent_node:
                parent_node.children.append(node)

            for child in item.children:
                render_widget_item(node, TreeWidgetNode(), child)

        root_node = TreeWidgetNode()

        render_widget_item(None, root_node, model)

        root_node.checked = False

        @action
        def select_node(item, selected):
            item.selected = selected

            for child in item.children:
                select_node(child, selected)

        select_node(model, False)

        self.assertFalse(model.selected)
        self.assertFalse(child1.selected)
        self.assertFalse(child2.selected)

        self.assertFalse(root_node.checked)
        self.assertFalse(root_node.children[0].checked)
        self.assertFalse(root_node.children[1].checked)


if __name__ == '__main__':
    unittest.main()
