from mopyx import model, render
import unittest


@model
class Model:
    def __init__(self):
        self.selectionIndex = -1


root_model = Model()


class UI:
    def __init__(self):
        self.selection = root_model.selectionIndex
        self.render()

    @render(ignore_updates=True)
    def render(self):
        self.set_selection(root_model.selectionIndex)

    def set_selection(self, index):
        root_model.selectionIndex = index


class TestIgnoreUpdates(unittest.TestCase):
    """
    Test if circular deps can be broken with
    ignore_updates.
    """

    def test_ignore_updates(self):
        """
        Create an UI that updates.
        """
        ui = UI()
        ui.set_selection(1)


if __name__ == '__main__':
    unittest.main()
