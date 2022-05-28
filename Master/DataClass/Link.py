class Link(object):
    def __init__(self, point = None, up=False, left=False, right=False, down=False):
        self.coordinate = point
        self.up = up
        self.left = left
        self.right = right
        self.down = down

    def __eq__(self, other):
        return self.coordinate == other.coordinate