class Tile:
    
    def __init__(self, row, col, is_wall):
        self.row = row
        self.col = col
        self.is_wall = is_wall
        self.block = ""
        self.goal = ""