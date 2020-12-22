from typing import Set

from mopyx import model, action

from .SystrayItem import SystrayItem

from germanium_build_monitor.model import Settings


@model
class Systray:
    def __init__(self):
        self.requests = []
        self.items = []

    @action
    def add_request(self, item: SystrayItem):
        self.requests.insert(0, item)

    @action
    def flush_requests(self):
        unique_requests = []
        request_keys: Set[str] = set()

        for request in self.requests:
            if request.key not in request_keys:
                request_keys.add(request.key)
                unique_requests.append(request)

        for i in reversed(range(len(self.items))):
            if self.items[i].key in request_keys:
                del self.items[i]

        self.requests = []

        for request in unique_requests:
            self.items.insert(0, request)

        if len(self.items) > Settings.settings.systray_items_count:
            del self.items[Settings.settings.systray_items_count:]

