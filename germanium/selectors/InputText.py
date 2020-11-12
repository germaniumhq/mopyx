from .Element import Element


class InputText(Element):
    """
    Just a selector that finds an input text by its placeholder.
    Matches all the HTML5 types that will yield an input that allows
    text input.
    """

    def __init__(self, placeholder=None, *args, **kw):
        text_types = [
            "date",
            "datetime",
            "datetime-local",
            "email",
            "month",
            "number",
            "password",
            "search",
            "tel",
            "text",
            "time",
            "url",
            "week"
        ]
        type_condition = " ".join(map(lambda it: "@type='%s' or" % it,
                                      text_types))
        extra_xpath = "[%s not(@type)]" % type_condition

        if placeholder is not None:
            extra_xpath += "[@placeholder = '%s']" % placeholder

        super(InputText, self).__init__("input",
                                        extra_xpath=extra_xpath,
                                        *args,
                                        **kw)
