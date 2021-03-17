class Tile:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_wall = False
        self.block = ""
        self.goal = ""

    def __repr__(self):
        if (self.is_wall):
            return " WALL "
        
        if (self.block == "" and self.goal == ""):
            return " EMPTY "
        out = "["
        if (self.block != ""):
            out += f" BLOCK[{self.block}] "
        if (self.goal != ""):
            out += f" GOAL[{self.goal}] "
        out += "]"
        return out

    def set_wall(self):
        self.is_wall = True
    
    def set_empty(self):
        self.block = ""
        self.goal = ""

    def set_block(self, color):
        self.block = color
    
    def set_goal(self, color):
        self.goal = color

    def is_tile_wall(self):
        return self.is_wall

    def is_empty(self):
        return not self.is_wall and (self.block == "" and self.goal == "")

    def has_block(self):
        return self.block != ""
    
    def has_goal(self):
        return self.goal != ""

    def get_block(self):
        return self.block

    def block_matches_goal(self):
        return not self.is_empty and (self.block == self.goal)