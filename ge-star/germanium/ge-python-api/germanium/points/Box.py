from germanium.impl._load_script import load_script
from .Point import Point


class Box(object):
    def __init__(self, selector):
        self._selector = selector
        self._box = None

    def top_left(self, adjust_x=0, adjust_y=0):
        if not self._box:
            self.get_box()

        return Point(self._box['left'] + adjust_x,
                     self._box['top'] + adjust_y)

    def top_center(self, adjust_x=0, adjust_y=0):
        if not self._box:
            self.get_box()

        return Point(self._box['center'] + adjust_x,
                     self._box['top'] + adjust_y)

    def top_right(self, adjust_x=0, adjust_y=0):
        if not self._box:
            self.get_box()

        return Point(self._box['right'] + adjust_x,
                     self._box['top'] + adjust_y)

    def middle_left(self, adjust_x=0, adjust_y=0):
        if not self._box:
            self.get_box()

        return Point(self._box['left'] + adjust_x,
                     self._box['middle'] + adjust_y)

    def middle_right(self, adjust_x=0, adjust_y=0):
        if not self._box:
            self.get_box()

        return Point(self._box['right'] + adjust_x,
                     self._box['middle'] + adjust_y)

    def bottom_left(self, adjust_x=0, adjust_y=0):
        if not self._box:
            self.get_box()

        return Point(self._box['left'] + adjust_x,
                     self._box['bottom'] + adjust_y)

    def bottom_center(self, adjust_x=0, adjust_y=0):
        if not self._box:
            self.get_box()

        return Point(self._box['center'] + adjust_x,
                     self._box['bottom'] + adjust_y)

    def bottom_right(self, adjust_x=0, adjust_y=0):
        if not self._box:
            self.get_box()

        return Point(self._box['right'] + adjust_x,
                     self._box['bottom'] + adjust_y)

    def center(self, adjust_x=0, adjust_y=0):
        if not self._box:
            self.get_box()

        return Point(self._box['center'] + adjust_x,
                     self._box['middle'] + adjust_y)

    def width(self):
        if not self._box:
            self.get_box()

        return self._box['width']

    def height(self):
        if not self._box:
            self.get_box()

        return self._box['height']

    def left(self):
        if not self._box:
            self.get_box()

        return self._box['left']

    def right(self):
        if not self._box:
            self.get_box()

        return self._box['right']

    def top(self):
        if not self._box:
            self.get_box()

        return self._box['top']

    def bottom(self):
        if not self._box:
            self.get_box()

        return self._box['bottom']

    def get_box(self):
        from germanium.static import S, js
        code = load_script(__name__, 'box.min.js')

        target_element = S(self._selector).element()

        if not target_element:
            raise Exception("The passed selector (%s) for finding "
                            "the bounding box didn't matched any elements." % self._selector)

        top, right, bottom, left, \
        center, middle, width, height = js(code, target_element)

        self._box = {
            "top": top,
            "right": right,
            "bottom": bottom,
            "left": left,
            "center": center,
            "middle": middle,
            "width": width,
            "height": height
        }

        return self
