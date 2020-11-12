from .AbstractSelector import AbstractSelector


class AnyOfSelector(AbstractSelector):
    def __init__(self, *selectors):
        if not selectors:
            raise Exception("You need to pass a list of selectors that the "
                            "AnyOfSelector will try to use when matching.")

        self.selectors = selectors
