class Tile:
    def __init__(self, row, col, is_wall):
        self.row = row
        self.col = col
        self.is_wall = is_wall
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

    def is_wall(self):
        return self.is_wall

    def is_empty(self):
        return not self.is_wall and (self.block == "" and self.goal == "")

    def has_block(self):
        return self.block != ""
    
    def has_goal(self):
        return self.goal != ""

    def block_matches_goal(self):
        return not self.is_empty and (self.block == self.goal)