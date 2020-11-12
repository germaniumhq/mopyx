import webcolors, re

RGB_PARSER = re.compile(r'^rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\);?$')
RGBA_PARSER = re.compile(r'^rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\);?$')


class Color(object):
    """
    A class that supports parsing of colors, that are most likely
    returned by a get_style() call.
    """
    def __init__(self, definition, opacity=None):
        if not isinstance(definition, str):
            raise Exception("Unable to parse color %s" % definition)

        color_definition = definition.lower()
        self.opacity = float(1)

        if color_definition == "transparent":
            self.opacity = 0.0
            self.value = '#000000'
        elif color_definition.startswith("rgb("):
            m = RGB_PARSER.match(color_definition)
            color_rgb =(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            self.value = webcolors.rgb_to_hex(color_rgb)
        elif color_definition.startswith("rgba("):
            m = RGBA_PARSER.match(color_definition)
            color_rgb =(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            self.value = webcolors.rgb_to_hex(color_rgb)
            self.opacity = float(m.group(4))
        elif color_definition.startswith("#"):
            self.value = webcolors.normalize_hex(color_definition)
        else:
            self.value = webcolors.rgb_to_hex(webcolors.html5_parse_legacy_color(color_definition))

        if opacity is not None:
            self.opacity = opacity

    def __eq__(self, other):
        """
        Check if the values are equal. Both colors having 0 opacity count as
        being equals.
        :param other:
        :return:
        """
        if not isinstance(other, self.__class__):
            return False

        if self.opacity == other.opacity and self.opacity == 0:
            return True

        return self.value == other.value

    def __str__(self):
        return "Color(%s, opacity: %f)" % (self.value, self.opacity)
