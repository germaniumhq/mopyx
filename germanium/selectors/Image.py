from .Element import Element


class Image(Element):
    def __init__(self, alt=None, exact_attributes=None, *args, **kwargs):
        _exact_attributes = {}

        if exact_attributes:
            _exact_attributes.update(exact_attributes)

        _exact_attributes["alt"] = alt

        super(Image, self).__init__("img", exact_attributes=_exact_attributes, *args, **kwargs)
