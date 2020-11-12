from .AbstractSelector import AbstractSelector


class StaticElement(AbstractSelector):
    def __init__(self, static_element):
        super(StaticElement, self).__init__()
        self.static_element = static_element
