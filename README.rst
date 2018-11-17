MoPyX
=====

MoPyX is a MobX/Vue inspired reactive model driven UI library. UI
Toolkit independent.

Reactive UI is a concept of having the UI automatically update as a
reaction to changes being done in the backend model. This happens
without manually registering listeners, and the reactive framework
keeping track of what parts of the model affect what parts of the
application..

Demo
----

.. figure:: https://raw.githubusercontent.com/germaniumhq/mopyx-sample/master/demo.gif
   :alt: PySide2 MoPyX Demo

   PySide2 MoPyX Demo

Full demo project source is here:
https://github.com/germaniumhq/mopyx-sample

@model
------

You decorate your model classes with ``@model``. All the properties of
that class will be monitored for changes. Whenever one of those
properties will change, the affected renderers (only the renderer
functions that used that property) will be re-invoked on model changes.

.. code:: py

    @model
    class FormModel:
        def __init__(self):
            self.first_name = "John"
            self.last_name "Doe"

@render
-------

You decorate your UI rendering functions with ``@render``, or invoke
them with ``render_call``. MoPyX will map what render method used what
properties in the model. The parameters for the function will be also
recorded and sent to the renderer function.

.. code:: py

    class UiForm:
        def __init__(self):
            # ...
            self.render_things()

        @render
        def render_things(self):
            self.first_name_label.set_text(self.model.first_name)
            self.last_name_label.set_text(self.model.last_name)

Whenever either ``first_name`` or ``last_name`` change in our model,
``render_things`` will be invoked again.

In order to optimize the number of UI updates, only the relevant
``@render`` functions will be called, not always the topmost one.

So you could break down the previous ``@render`` method into two
methods:

.. code:: py

    @render
    def render_things(self):
        self.render_first_name()
        self.render_last_name()

    @render
    def render_first_name(self):
        self.first_name_label.set_text(self.model.first_name)

    @render
    def render_last_name(self):
        self.last_name_label.set_text(self.model.last_name)

Now if only the ``first_name`` changes in the model, the set\_text for
the ``last_name`` will not be invoked. This happens automatically, and
only the needed renderers will be invoked.

To type less, ``render_call()`` will just wrap the given callable into a
``@render``. For example we can rewrite our renderer to be shorter:

.. code:: py

    @render
    def render_things(self):
        render_call(lambda: self.first_name_label.set_text(self.model.first_name))
        render_call(lambda: self.last_name_label.set_text(self.model.last_name))

``@render`` methods are not allowed to do model changes while running.
If setting an UI value will trigger a model change, read the
``ignore_updates`` section.

@action
-------

If they're not wrapped in an action, every property is also an action,
so after the property change, a rendering will trigger. To improve
performance you can wrap multiple model updates into a single
``@action``. An action method can call other methods, including other
``@action``\ s.

When when the top most ``@action`` finishes the rendering will be
invoked. MoPyX will find out what renderers need to be called, and what
computed properties should be updated, in order to get the UI into a
consistent state.

Internally all the properties setters in the ``@model`` classes are
wrapped in ``@action``\ s.

.. code:: py

    @action  # withonut this would trigger a render after each assignment
    def change_model(self):
        self.first_name = "Jane"
        self.last_name = "Mary"

@computed
---------

You can also create properties on the model using the ``@computed``
decorator. This works similarly with a regular python ``@property`` but
it will be invoked only when one of the other properties it depends on
(including from other MoPyX models) change. Otherwise calling this
property will return the previously computed value.

This is great for difficult to compute properties. Have a list that must
be accessed as sorted, but comes from the data store as unsorted? You
can wrap it in a ``@computed`` method. Again, note that the
``@computed`` method will only be invoked when the used properties by
that ``@computed`` method will change:

.. code:: py

    @model
    class RootModel:
        def __init__(self):
            self.backend_data = []

        @action
        def fetch_data(self):
            self.backend_data = fetch_data_from_service()

        @computed
        def first_five_items(self):
            # will only be invoked when self.backend_data changes
            result = list(self.backend_data)

            result.sort()
            result = result[0:5]

            return result

    class UiRenderer:
        # ...
        @render
        def render_items(self):
            # will be invoked only when first_five_items changes
            for item in self.root_model.first_five_items:
                self.render_item(item)

``@computed`` properties are not allowed to change the state of the
object.

List
----

If one of the properties is a list, the list will be replaced with a
special implementation, that will also notify its changes on the top
property.

.. code:: py

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

ignore\_updates
---------------

If the renderer will call a value that sets something in the UI that
will make the UI trigger an event, that will in turn might land in an
action (model updates are also actions), you can disable the rendering
using the ``ignore_updates`` attribute. This will suppress *all action
invocations* from that rendering method, including *all model updates*.

This is great for onchange events for input edits, or tree updates such
as selected nodes that otherwise would enter an infinite recursion.

Debugging
---------

To check what goes on, you can export in your environment:

-  ``MOPYX_DEBUG`` - this will print the rendering process on the
   console.
-  ``MOPYX_THREAD_CHECK`` - this will throw an exception if the thread
   for ``@render`` methods change.
