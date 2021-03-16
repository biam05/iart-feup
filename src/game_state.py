class GameState:
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    GOAL = 3

    def __init__(self, matrix):
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])

        self.walls = []
        self.goals = []
        self.blocks = []

        for i in range(self.rows):
            for j in range(self.cols):
                obj = matrix[i][j]
                if (obj == self.WALL):
                    self.walls.append((i, j))
                elif (isinstance(obj, list)):
                    if (obj[0] == self.BLOCK):
                        self.blocks.append([i, j])
                    elif (obj[0] == self.GOAL):
                        self.goals.append((i, j))

    def move(self, pos, new_pos):
        obj = self.matrix[pos[0]][pos[1]]
        self.matrix[pos[0]][pos[1]] = self.EMPTY
        self.matrix[new_pos[0]][new_pos[1]] = obj 

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
                if (obj == self.EMPTY):
                    out += " EMPTY\t\t"
                if (obj == self.WALL):
                    out += " WALL\t\t"
                elif (isinstance(obj, list)):
                    if (obj[0] == self.BLOCK):
                        out += f" BLOCK[{obj[1]}]\t\t"
                    elif (obj[0] == self.GOAL):
                        out += f" GOAL[{obj[1]}]\t\t"
            out += "\t]"
        out += "\n]\n"
        return out
