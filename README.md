# MoPyX

MoPyX is a MobX/Vue inspired reactive model driven UI library. UI Toolkit independent.

## Demo

![PySide2 MoPyX Demo](https://raw.githubusercontent.com/germaniumhq/mopyx-sample/master/demo.gif)

Demo project is here: [https://github.com/germaniumhq/mopyx-sample](https://github.com/germaniumhq/mopyx-sample)

## Installation

```sh
pip install mopyx
```

## Usage

```py
from mopyx import render, render_call, model, action


@model
class RootModel:
    def __init__(self):
        self.name = "initial name"        # Whenever `name`, `desc` or `title` change,
        self.desc = "initial description" # a rerender will be triggered. This is
        self.title = "initial title"      # mapped in the actual rendering. Changing
        self.other = "initial other"      # `other` will not trigger a rerender.


class UpdateModelService:
    # Each model change is a tiny action that should trigger a rerender. To cluster
    # multiple actions together you can use `@action`. When the topmost `@action`
    # returns only then the affected renderers will be invoked.
    @action
    def update_title_and_description(title, description):
        self.model.title = title
        self.model.desc = description


class UiLabel:  # a basic label in any toolkit
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

    # MoPyX will know about this rendering. Here it learns that from the
    # model `name`, `desc`, and `title` are needed for the rendering.
    # After this render whenever any of the model properties change,
    # the `@render` method will be invoked automatically.
    @render
    def update_data(self):
        render_call(lambda: self.name.set_label(self.model.name))
        render_call(lambda: self.description.set_label(self.model.desc))

        self.title = self.model.title
```

You decorate your UI rendering functions with `@render`, or invoke them with
`render_call`. MoPyX will map what render method used what properties in the
model.

You decorate your model classes with `@model`. Whenever properties change in the
model, the `@render` function will be called again, but only for the UI components
that are affected by the model action. This will happen for every property in the
model.

In the example above, if the name changes, then only the `set_label` will be
invoked on the label, because it's registered as a subcomponent rendering. If
both `title`  and `name` change simultaneously into an `@action` MoPyX will
call only the top `update_data` rendering.

If they're not wrapped in an action, every property is considered an action, so
two renderings will trigger. To improve performance you can wrap multiple model
updates into a single `@action`. An action method can call other methods,
including other `@action` ones, then when the top most `@action` returns the
rendering will be invoked.

In order to optimize the number of UI updates, only the relevant `@render`
functions will be called, not always the topmost one.

If there is a component that's too difficult to have its own `@render` for
updates, you can also call the updates for that specific component using
`render_call()` that will just wrap the given callable into a `@render`. For
example if there is a `Label` component of some sort, you can just wrap it in
`render_call`s:

```py
render_call(lambda: self.name.set_label(self.model.name))
```

## List

If one of the properties is a list, the list will be replaced with a special
implementation, that will also notify its changes on the top property.

```py
@model
class RootModel:
    def __init__(self):
        self.items = []


class UiComponent:
    @render
    def update_ui(self):
        for item in self.items:
            self.render_sub_component(item)


model = RootModel()
ui = UiComponent(model)


model.items.append("new item")  # this will trigger the update_ui rerender.
```

## ignore_updates

If the renderer will call a value that sets something in the UI that will make
the UI trigger an event, that will in turn might land in an action (model
updates are also actions), you can disable the rendering using the
`ignore_updates` attribute. This will supress _all action invocations_ from
that rendering method, including _all model updates_.

This is great for onchange events for input edits, or tree updates such as
selected nodes that otherwise would enter an infinite recursion.

