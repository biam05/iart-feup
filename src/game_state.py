from tile import Tile

class GameState:
    def __init__(self, rows, cols, walls, blocks, goals):
        self.matrix = []
        
        self.walls = walls
        self.blocks = blocks
        self.goals = goals
        
        self.rows = rows
        self.cols = cols

        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(Tile(i, j))
            self.matrix.append(row)

        for wall in self.walls:
            row = wall[0]
            col = wall[1]
            self.matrix[row][col].set_wall()

        for block in self.blocks:
            row = block[0]
            col = block[1]
            color = block[2]
            self.matrix[row][col].set_block(color)

        for goal in self.goals:
            row = goal[0]
            col = goal[1]
            color = goal[2]
            self.matrix[row][col].set_goal(color)
    
    def is_game_over(self):
        for goal in self.goals:
            tile = self.matrix[goal[0]][goal[1]]
            if (not tile.block_matches_goal):
                return False
        return True

    def move(self, pos, new_pos):
        obj = self.matrix[pos[0]][pos[1]].block
        self.matrix[pos[0]][pos[1]].set_block("")
        self.matrix[new_pos[0]][new_pos[1]].set_block(obj) 

    def swipe_left(self):
        self.blocks.sort(key=lambda el: el[1])
        for i in range(len(self.blocks)):
            block = self.blocks[i]
            walls = sorted(filter(lambda el: el[0] == block[0] and el[1] < block[1], self.walls + self.blocks[:i]), key=lambda el: -el[1])
            new_col = walls[0][1] + 1 if walls else 0
            self.move(block, (block[0], new_col))
            self.blocks[i][1] = new_col

    def swipe_right(self):
        self.blocks.sort(key=lambda el: -el[1])
        for i in range(len(self.blocks)):
            block = self.blocks[i]
            walls = sorted(filter(lambda el: el[0] == block[0] and el[1] > block[1], self.walls + self.blocks[:i]), key=lambda el: el[1])
            new_col = walls[0][1] - 1 if walls else (self.cols - 1)
            self.move(block, (block[0], new_col))
            self.blocks[i][1] = new_col

    def swipe_up(self):
        self.blocks.sort(key=lambda el: el[0])
        for i in range(len(self.blocks)):
            block = self.blocks[i]
            walls = sorted(filter(lambda el: el[1] == block[1] and el[0] < block[0], self.walls + self.blocks[:i]), key=lambda el: -el[0])
            new_row = walls[0][0] + 1 if walls else 0
            self.move(block, (new_row, block[1]))
            self.blocks[i][0] = new_row

    def swipe_down(self):
        self.blocks.sort(key=lambda el: -el[0])
        for i in range(len(self.blocks)):
            block = self.blocks[i]
            walls = sorted(filter(lambda el: el[1] == block[1] and el[0] > block[0], self.walls + self.blocks[:i]), key=lambda el: el[0])
            new_row = walls[0][0] - 1 if walls else (self.rows -1)
            self.move(block, (new_row, block[1]))
            self.blocks[i][0] = new_row

    def __repr__(self):
        out = "["
        for i in range(self.rows):
            out += "\n["
            for j in range(self.cols):
                obj = self.matrix[i][j]
                if (obj.is_empty()):
                    out += "%30s" % "EMPTY"
                elif (obj.is_tile_wall()):
                    out += "%30s" % "WALL"
                else:
                    temp = "["
                    if obj.has_block():
                        temp += f"BLOCK[{obj.block} "
                    if obj.has_goal():
                        temp += f"GOAL[{obj.goal}]"
                    temp += "]"
                    out += "%30s" % temp
            out += "]"
        out += "\n]\n"
        return out
