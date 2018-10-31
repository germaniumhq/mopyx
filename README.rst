mopyx
=====

mopyx is a MobX/Vue inspired reactive model driven UI library. UI
Toolkit independent.

Installation
------------

.. code:: sh

    pip install mopyx

Usage
-----

.. code:: py

    from mopyx import render, render_call, model


    @model
    class RootModel:
        def __init__(self):
            self.name = "initial name"
            self.desc = "initial description"
            self.title = "initial title"


    class UiLabel:
        def __init__(self):
            self.label = None

        def set_label(self, label):
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
            render_call(lambda: self.name.set_label(self.model.name))
            render_call(lambda: self.description.set_label(self.model.desc))

            self.title = self.model.title

You decorate you model classes with ``@model``. Whenever properties
change in the model, the ``@render`` function will be called again, but
only for the components that are affected by the model update.

In order to partition the number of UI updates, only the relevant
``@render`` functions will be called, not always the topmost one.

If there is a component that's too difficult to have its own ``@render``
for updates, you can also call the updates for that specific component
using ``render_call()`` that will just wrap the given callable into a
``@render``. For example if there is a ``Label`` component of some sort,
you can just wrap it in ``render_call``\ s.
