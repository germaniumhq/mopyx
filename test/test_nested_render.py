from typing import List, Optional
from mopyx import model, render, render_call, action

import unittest


@model
class TreeItem:
    def __init__(self, parent: Optional['TreeItem'], name: str) -> None:
        self.selected = True
        self.name = name
        self.parent = parent
        self.children: List['TreeItem'] = []

        if parent:
            parent.children.append(self)


class TreeWidgetNode:
    def __init__(self,
                 parent_node: Optional['TreeWidgetNode'],
                 item: TreeItem):
        self.label: str = ""
        self.checked = True
        self.children: List['TreeWidgetNode'] = []
        self.item = item

        if parent_node:
            parent_node.children.append(self)

    # In UIs there is the case of wiring change listeners with
    # events that will fire endlessly. For example selecting the
    # parent node of a tree will selct its children. Children
    # will change the model up, setting the parent value again.
    # Mopyx will call the renderer, that will check the parent node
    # again, that will fire the rerendering again.
    #
    # That's why if an action is inside a renderer with ignore_updates
    # we won't fire that action. Otherwise good luck debugging.
    def set_ui_checked(self, value: bool) -> None:
        self.checked = value

        @action
        def select_nodes_down(node):
            node.selected = value

            for child in node.children:
                select_nodes_down(child)

        @action
        def select_nodes_up(node):
            if not node.parent:
                return

            node.parent.selected = value
            select_nodes_up(node.parent)

        @action
        def select_node_value(node):
            select_nodes_down(node)
            select_nodes_up(node)

        select_node_value(self.item)  # normally this should be an emit


class TestNestedRender(unittest.TestCase):
    """
    A simple "tree" test.
    """

    def test_nested_render(self):
        """
        Test if tree rendering works correctly.
        """
        model = TreeItem(None, "root")
        child1 = TreeItem(model, "child1")
        child2 = TreeItem(model, "child2")

        @render
        def render_widget_item(tree_node: TreeWidgetNode):
            def update_labels():
                tree_node.label = tree_node.item.name
                tree_node.set_ui_checked(tree_node.item.selected)

            render_call(update_labels, ignore_updates=True)

            for child in tree_node.item.children:
                render_widget_item(TreeWidgetNode(tree_node, child))

        root_node = TreeWidgetNode(None, model)
        render_widget_item(root_node)

        root_node.children[1].set_ui_checked(False)

        self.assertFalse(model.selected)
        self.assertTrue(child1.selected)
        self.assertFalse(child2.selected)

        self.assertFalse(root_node.checked)
        self.assertTrue(root_node.children[0].checked)
        self.assertFalse(root_node.children[1].checked)


if __name__ == '__main__':
    unittest.main()
