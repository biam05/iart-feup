class Node:
    def __init__(blocks):
        self.blocks = block

    def move(self, pos, new_pos):
        obj = self.matrix[pos[0]][pos[1]].block
        self.matrix[pos[0]][pos[1]].set_block("")
        self.matrix[new_pos[0]][new_pos[1]].set_block(obj) 

    def swipe_left(self, walls):
        self.blocks.sort(key=lambda el: el[1])
        for i in range(len(self.blocks)):
            block = self.blocks[i]
            walls = sorted(filter(lambda el: el[0] == block[0] and el[1] < block[1], self.walls + self.blocks[:i]), key=lambda el: -el[1])
            new_col = walls[0][1] + 1 if walls else 0
            self.move(block, (block[0], new_col))
            self.blocks[i][1] = new_col
    
    def swipe_right(self, walls):
        self.blocks.sort(key=lambda el: -el[1])
        for i in range(len(self.blocks)):
            block = self.blocks[i]
            walls = sorted(filter(lambda el: el[0] == block[0] and el[1] > block[1], self.walls + self.blocks[:i]), key=lambda el: el[1])
            new_col = walls[0][1] - 1 if walls else (self.cols - 1)
            self.move(block, (block[0], new_col))
            self.blocks[i][1] = new_col

    def swipe_up(self, walls):
        self.blocks.sort(key=lambda el: el[0])
        for i in range(len(self.blocks)):
            block = self.blocks[i]
            walls = sorted(filter(lambda el: el[1] == block[1] and el[0] < block[0], self.walls + self.blocks[:i]), key=lambda el: -el[0])
            new_row = walls[0][0] + 1 if walls else 0
            self.move(block, (new_row, block[1]))
            self.blocks[i][0] = new_row

    def swipe_down(self, walls):
        self.blocks.sort(key=lambda el: -el[0])
        for i in range(len(self.blocks)):
            block = self.blocks[i]
            walls = sorted(filter(lambda el: el[1] == block[1] and el[0] > block[0], self.walls + self.blocks[:i]), key=lambda el: el[0])
            new_row = walls[0][0] - 1 if walls else (self.rows -1)
            self.move(block, (new_row, block[1]))
            self.blocks[i][0] = new_row