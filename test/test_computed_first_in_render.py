from mopyx import computed, render, model
import unittest


@model
class RootModel:
    def __init__(self):
        self.access_computed = False

    @computed
    def calculated_value(self) -> str:
        return "calculated"


root_model = RootModel()


class Ui:
    def __init__(self,
                 root_model: RootModel):
        self.root_model = root_model
        self.render_ui()

    @render
    def render_ui(self):
        if not self.root_model.access_computed:
            return

        # computed properties are allowed to be invoked during the rendering,
        # so if it's an initial rendering, and already inside rendering, they should
        # not register themselves for rerendering.
        self.root_model.calculated_value


class TestComputedFirstRender(unittest.TestCase):
    def test_compute_first_render(self):
        Ui(root_model)

        root_model.access_computed = True


if __name__ == '__main__':
    unittest.main()
