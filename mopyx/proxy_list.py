from typing import List

from mopyx.decorator_action import action


class ListModelProxy(list):
    """
    Tracks items in a list for changes. Whenever the list changes, triggers the
    parent model property as changed.
    """

    def __init__(self, model, property_name: str, target: List) -> None:
        super().__init__(list(target))
        self._mopyx_model = model
        self._mopyx_property_name = property_name

    def __getitem__(self, i):
        self._mopyx_model._mopyx_register_active_renderers(self._mopyx_property_name)
        return super().__getitem__(i)

    def __getslice__(self, i, j):
        self._mopyx_model._mopyx_register_active_renderers(self._mopyx_property_name)
        return super().__getslice__(i, j)

    @action
    def __setitem__(self, *argv, **kw):
        result = super().__setitem__(*argv, **kw)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)
        return result

    @action
    def __setslice__(self, *argv, **kw):
        result = super().__setslice__(*argv, **kw)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)
        return result

    @action
    def __delitem__(self, *argv, **kw):
        result = super().__delitem__(*argv, **kw)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)
        return result

    @action
    def __delslice__(self, *argv, **kw):
        result = super().__delslice__(*argv, **kw)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)
        return result

    @action
    def append(self, *argv, **kw):
        result = super().append(*argv, **kw)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)
        return result

    @action
    def clear(self, *argv, **kw):
        current_len = len(self)

        result = super().clear(*argv, **kw)

        if current_len:
            self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)

        return result

    @action
    def extend(self, *argv, **kw):
        result = super().extend(*argv, **kw)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)
        return result

    @action
    def insert(self, *argv, **kw):
        result = super().insert(*argv, **kw)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)
        return result

    @action
    def pop(self, *argv, **kw):
        result = super().pop(*argv, **kw)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)
        return result

    @action
    def remove(self, *argv, **kw):
        result = super().remove(*argv, **kw)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)
        return result

    @action
    def reverse(self, *argv, **kw):
        result = super().reverse(*argv, **kw)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)
        return result

    @action
    def sort(self, *argv, **kw):
        result = super().sort(*argv, **kw)
        self._mopyx_model._mopyx_register_refresh(self._mopyx_property_name)
        return result
