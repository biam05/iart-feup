from tile import Tile
from enum import Enum
from copy import deepcopy
import sys

"""
Checks if point t is in between p1 and p2
"""
def in_between(p1, p2, t):
    if (p1[0] == p2[0] and p1[0] == t[0]):
        return (t[1] > p1[1] and t[1] < p2[1]) or (t[1] < p1[1] and t[1] > p2[1])
    elif (p1[1] == p2[1] and p1[1] == t[1]):
        return (t[0] > p1[0] and t[0] < p2[0]) or (t[0] < p1[0] and t[0] > p2[0])
    return False

class Move(Enum):
    SWIPE_LEFT = 0
    SWIPE_DOWN = 1
    SWIPE_RIGHT = 2
    SWIPE_UP = 3


class GameState:
    """
    Constructor
    - List[List] blocks     : list of coordinates of all movable blocks
    - Move move             : Move that generated the game state
    - Int nMoves            : Number of moves since starting GameState
    """
    def __init__(self, blocks, move=None, nMoves = 0):
        self.blocks = blocks
        self.move = move
        self.nMoves = nMoves
        self.points = -1
    
    def eval_game_state(self, matrix, goals, walls):
        if (self.points == -1):
            for goal in goals:
                goal_x = goal[0]
                goal_y = goal[1]
                goal_color = goal[2]
                for block in self.blocks:
                    obstacles = filter(lambda el: el != block, self.blocks + walls)
                    block_x = block[0]
                    block_y = block[1]
                    block_color = block[2]
                    if goal_color == block_color:
                        if goal_x == block_x and goal_y == block_y: # block matches goal
                            self.points += 1
                        elif goal_x == block_x and goal_y != block_y: # same row but different column
                            self.points += 2
                            for obstacle in obstacles:
                                # wall between goal and block
                                if obstacle[0] == goal_x and ((obstacle[0] > goal_x and obstacle[0] < block_x)or(obstacle[0] < goal_x and obstacle[0] > block_x)): 
                                    self.points += 2
                                    break
                        elif goal_y == block_y and goal_x != block_x: # same column but different row
                            self.points += 2 
                            for obstacle in obstacles:
                                # wall between goal and block
                                if obstacle[1] == goal_y and ((obstacle[1] > goal_y and obstacle[1] < block_y)or(obstacle[1] < goal_y and obstacle[1] > block_y)): 
                                    self.points += 2 
                                    break

        return self.nMoves + self.points # evaluate based on current state

    def is_wall_stopping_block_at_goal(block, goal, wall):
        if goal[0] == block[0]:
            if (goal[1] > wall[1] and wall[1] == goal[1] + 1) or (goal[1] < wall[1] and wall[1] == goal[1] - 1):
                return True
            
        elif goal[1] == block[1]:
            if (goal[0] > block[0] and goal[0] + 1 == wall[0]) or (goal[0] < block[0] and goal[0] - 1 == wall[0]):
                return True
        return False

    def estimate_moves_left(self, goals, walls, rows, cols):
        moves = 0

        for block in self.blocks:
            local_moves = sys.maxint
            block_x = block[0]
            block_y = block[1]
            colinear_goals = filter(lambda el: el[2] == block[2] and (el[0] == block[0] or el[1] == block[1]), goals)
            # colinear
            if (colinear_goals):
                for goal in colinear_goals:
                    goal_x = goal[0]
                    goal_y = goal[1]
                    if goal_x == block_x and goal_y == block_y:
                        local_moves = min(local_moves, 0)
                        break
                    obstacles = filter(lambda el: el != block and in_between(goal, block, el)), self.blocks + walls)
                    # has an obstacle between the block and the goal
                    if obstacles:
                        local_moves = min(local_moves, 4)
                    else:
                        if (goal_x == block_x and (goal_y == 0 or goal_y == cols - 1)) or (goal_y == block_y and (goal_x == 0 or goal_x == rows - 1)):
                            local_moves = min(local_moves, 1)
                        else:
                            obstacles = filter(lambda el: self.is_wall_stopping_block_at_goal(block, goal, el), walls)
                            local_moves = min(local_moves, 1 if obstacles else 2)
            # non-colinear
            else:
                matching_goals = filter(lambda el: el[2] == block[2], goals)
                for goal in matching_goals:
                    # horizontal move

                    # vertical move
                    colinear_walls_with_move = filter(lambda el: el[1] == block_y and ((el[0] <= goal_x - 1 and goal_x < block_x) or (el[0] >= goal_x + 1 and goal_x > block_x))
                    closest_wall = min(, key=lambda el: abs(el[0] - block_x))


    def swipe_left(self, walls):
        new_blocks = deepcopy(self.blocks)
        new_blocks.sort(key=lambda el: el[1])
        for i in range(len(self.blocks)):
            block = new_blocks[i]
            walls = sorted(filter(lambda el: el[0] == block[0] and el[1] < block[1], self.walls + self.blocks[:i]), key=lambda el: -el[1])
            new_col = walls[0][1] + 1 if walls else 0
            new_blocks[i][1] = new_col
        
        return GameState(new_blocks, Move.SWIPE_LEFT, self.nMoves)

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

    def __eq__(self, other):
        return self.matrix == other.matrix

