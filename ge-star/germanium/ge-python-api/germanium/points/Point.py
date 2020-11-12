class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def adjust_x(self, x):
        return Point(self.x + x, self.y)

    def adjust_y(self, y):
        return Point(self.x, self.y + y)
