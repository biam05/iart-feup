from dataclasses import dataclass


@dataclass
class Coords:
    """
    - x : Row value
    - y : Column value
    """
    x: int
    y: int

    """
    Checks if two Coords are equal
    """

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    """
    X Setter
    """

    def setX(self, x):
        self.x = x

    """
    Y Setter
    """

    def setY(self, y):
        self.y = y

    """
    Checks if Coords is in between
    """

    def in_between(self, c1, c2):
        if self.x == c1.x and self.x == c2.x:
            return (self.y > c1.y and self.y < c2.y) or (self.y < c1.y and self.y > c2.y)
        if self.y == c1.y and self.y == c2.y:
            return (self.x > c1.x and self.x < c2.x) or (self.x < c1.x and self.x > c2.x)
        return False


    def __hash__(self):
        return hash((self.x, self.y))
