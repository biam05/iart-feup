from utils.utils import Coords

class BlockData:
    """
    Constructor
    - Coords coords : Coordinates of the block
    - String color : Color of the block
    """
    def __init__(self, coords : Coords, color : str):
        self.coords = coords
        self.color = color

    """
    Changes coordinates of the block
    - Coords new_coords : New value for coordinates of the block
    """
    def move(self, new_coords : Coords):
        self.coords = new_coords
    
    def __repr__(self):
        return f"BLOCK[{self.coords.x}, {self.coords.y}, {self.color}]"

    def __str__(self):
        return f"BLOCK[{self.coords.x}, {self.coords.y}, {self.color}]"

    def __eq__(self, other):
        return self.coords == other.coords and self.color == other.color

class GoalData:
    """
    Constructor
    - Coords coords : Coordinates of the goal
    - String color : Color of the goal
    """
    def __init__(self, coords : Coords, color : str):
        self.coords = coords
        self.color = color
    
    """
    Checks if the goal color matches the block
    - BlockData block : block to be matched
    """
    def match_block(self, block):
        return (self.coords == block.coords) and (self.color == block.color)

    def __repr__(self):
        return f"GOAL[{self.coords.x}, {self.coords.y}, {self.color}]"

    def __str__(self):
        return f"GOAL[{self.coords.x}, {self.coords.y}, {self.color}]"

class WallData:
    """
    Constructor
    - Coords coords : Coordinates of the wall
    - String color : Color of the wall
    """
    def __init__(self, coords : Coords):
        self.coords = coords
    
    def __repr__(self):
        return f"WALL[{self.coords.x}, {self.coords.y}]"

    def __str__(self):
        return f"WALL[{self.coords.x}, {self.coords.y}]"
