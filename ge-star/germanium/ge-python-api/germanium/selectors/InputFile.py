
from .Element import Element


class InputFile(Element):
    """
    Just a selector that finds a file input
    """
    def __init__(self, *args, **kw):
        extra_xpath = "[@type='file']"

        super(InputFile, self).__init__("input",
                                        extra_xpath=extra_xpath,
                                        *args,
                                        **kw)
