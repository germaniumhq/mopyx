from .AbstractSelector import AbstractSelector


class Text(AbstractSelector):
    """
    Just a selector that finds the text in the page.
    """
    def __init__(self, text, exact=False, trim=False):
        super(Text, self).__init__()
        self.searched_text = text
        self.exact_match = exact
        self.trim_text = trim

    def get_selectors(self):
        raise Exception("Not implemented. A locator should be constructed "
                        "for it. If you just called Text(...) it's a bug in "
                        "Germanium, and please report it.")
