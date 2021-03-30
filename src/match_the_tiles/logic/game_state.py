from match_the_tiles.model.tile_data import WallData, BlockData, GoalData
from utils.utils import Coords

from enum import Enum
from copy import deepcopy
import sys

class Move(Enum):
    SWIPE_LEFT = 0
    SWIPE_DOWN = 1
    SWIPE_RIGHT = 2
    SWIPE_UP = 3

class CommonGameState:
    """
    Constructor
    - List walls : List of coordinates of the walls (i.e. [x, y])
    - List goals : List of coordinates and colors of the goals (i.e. [x, y, color])
    - Int rows : Number of rows in the game board
    - Int cols : Number of cols in the game board
    """
    def __init__(self, walls : list, goals : list, rows : int, cols : int):
        self.walls = list()
        for wall in walls:
            self.walls.append(WallData(Coords(wall[0], wall[1])))

        self.goals = list()
        for goal in goals:
            self.goals.append(GoalData(Coords(goal[0], goal[1]), goal[2]))

        self.rows = rows
        self.cols = cols

class GameState:
    """
    Constructor
    - CommonGameState common_gs : GameState containing the non-movable tiles
    - List blocks : List of coordinates and colors of the blocks (i.e. [x, y, color])
    - Move move : Move that originated GameState, None if initial
    - Int nMoves : Number of moves since initial state
    """
    def __init__(self, common_gs, blocks, move=None, nMoves=0):
        self.common_gs = common_gs
        self.blocks = list()
        for block in blocks:
            self.blocks.append(BlockData(Coords(block[0], block[1]), block[2]))
        self.move = move
        self.nMoves = nMoves
        self.points = -1

    """
    Makes a copy of the list of blocks
    """
    def make_blocks_copy(self):
        copy_blocks = list()
        for block in self.blocks:
            copy_blocks.append(BlockData(Coords(block.coords.x, block.coords.y), block.color))

        return copy_blocks
    
    @staticmethod
    def blocks_as_list(blocks):
        block_l = list()
        for block in blocks:
            block_l.append([block.coords.x, block.coords.y, block.color])

        return block_l

    """
    Evaluates GameState value
    """
    def eval_game_state(self):
        if (self.points == -1):
            for goal in self.common_gs.goals:
                goal_x = goal.coords.x
                goal_y = goal.coords.y
                goal_color = goal.color
                for block in self.blocks:
                    obstacles = filter(lambda el: el != block, self.blocks + self.common_gs.walls)
                    block_x = block.coords.x
                    block_y = block.coords.y
                    block_color = block.color
                    if goal_color == block_color:
                        if goal_x == block_x and goal_y == block_y: # block matches goal
                            self.points += 1
                        elif goal_x == block_x and goal_y != block_y: # same row but different column
                            self.points += 2
                            for obstacle in obstacles:
                                # wall between goal and block
                                if obstacle[0] == goal_x and ((obstacle.coords.x > goal_x and obstacle.coords.x < block_x)or(obstacle.coords-x < goal_x and obstacle.coords.x > block_x)): 
                                    self.points += 2
                                    break
                        elif goal_y == block_y and goal_x != block_x: # same column but different row
                            self.points += 2 
                            for obstacle in obstacles:
                                # wall between goal and block
                                if obstacle.coords.y == goal_y and ((obstacle.coords.y > goal_y and obstacle.coords.y < block_y)or(obstacle.coords.y < goal_y and obstacle.coords.y > block_y)): 
                                    self.points += 2 
                                    break

        return self.nMoves + self.points # evaluate based on current state

    """
    Checks if there's a wall adjacent to the goal on the direction the block is moving
    - Coords block : Coordinates of the block
    - Coords goal : Coordinates of the goal
    - Coords wall : Coordinates of the wall
    Returns if the wall is adjacent to the goal in the direction the block would be moving, thus stopping the block in the goal
    """
    @staticmethod
    def is_wall_stopping_block_at_goal(block, goal, wall):
        if goal.coords.x == block.coords.x:
            if (goal.coords.y > wall.coords.y and wall.coords.y == goal.coords.y + 1) or (goal.coords.y < wall.coords.y and wall.coords.y == goal.coords.y - 1):
                return True
            
        elif goal.coords.y == block.coords.y:
            if (goal.coords.x > block.coords.x and goal.coords.x + 1 == wall.coords.x) or (goal.coords.x < block.coords.x and goal.coords.x - 1 == wall.coords.x):
                return True
        return False

    """
    Estimates the number of moves needed to finish the game from a GameState
    - Coords[] goals : List of coordinates of the goals
    - Coords[] walls : List of coordinates of the walls
    - Int rows : Number of rows on the game board
    - Int cols : Number of columns on the game board

    Returns the estimate number of moves needed to finish the game 
    """
    def estimate_moves_left(self, goals, walls, rows, cols):
        moves = 0

        for block in self.blocks:
            local_moves = sys.maxint
            block_x = block.coords.x
            block_y = block.coords.y
            colinear_goals = filter(lambda el: el.color == block.color and (el.coords.x == block.coords.x or el.coords.y == block.coords.y), goals)
            # colinear
            if (colinear_goals):
                for goal in colinear_goals:
                    goal_x = goal.coords.x
                    goal_y = goal.coords.y
                    if goal_x == block_x and goal_y == block_y:
                        local_moves = min(local_moves, 0)
                        break
                    obstacles = filter(lambda el: el != block and el.in_between(goal, block), self.blocks + walls)
                    # has an obstacle between the block and the goal
                    if obstacles:
                        local_moves = min(local_moves, 3)
                    else:
                        if (goal_x == block_x and (goal_y == 0 or goal_y == cols - 1)) or (goal_y == block_y and (goal_x == 0 or goal_x == rows - 1)):
                            local_moves = min(local_moves, 1)
                        else:
                            obstacles = filter(lambda el: self.is_wall_stopping_block_at_goal(block, goal, el), walls)
                            local_moves = min(local_moves, 1 if obstacles else 2)
            # non-colinear
            else:
                matching_goals = filter(lambda el: el.color == block.color, goals)
                for goal in matching_goals:
                    """
                    # horizontal move

                    # vertical move
                    colinear_walls_with_move = filter(lambda el: el[1] == block_y and ((el[0] <= goal_x - 1 and goal_x < block_x) or (el[0] >= goal_x + 1 and goal_x > block_x)))
                    closest_wall = min(, key=lambda el: abs(el[0] - block_x))
                    """

    """
    Swipe Left Operation - Moves the movable blocks in the GameState to the left

    Returns the new GameState generated by that operation
    """
    def swipe_left(self):
        new_blocks = self.make_blocks_copy()
        new_blocks.sort(key=lambda el: el.coords.y)
        for i in range(len(new_blocks)):
            block = new_blocks[i]
            walls = sorted(filter(lambda el: el.coords.x == block.coords.x and el.coords.y < block.coords.y, new_blocks[:i] + self.common_gs.walls), key=lambda el: -el.coords.y)
            new_col = walls[0].coords.y + 1 if walls else 0
            new_blocks[i].coords.setY(new_col)
        
        return GameState(self.common_gs, self.blocks_as_list(new_blocks), move=Move.SWIPE_LEFT, nMoves=(self.nMoves + 1))

    """
    Swipe Right Operation - Moves the movable blocks in the GameState to the right

    Returns the new GameState generated by that operation
    """
    def swipe_right(self):
        new_blocks = self.make_blocks_copy()
        new_blocks.sort(key=lambda el: -el.coords.y)
        for i in range(len(new_blocks)):
            block = new_blocks[i]
            walls = sorted(filter(lambda el: el.coords.x == block.coords.x and el.coords.y > block.coords.y, new_blocks[:i] + self.common_gs.walls), key=lambda el: el.coords.y)
            new_col = walls[0].coords.y - 1 if walls else (self.common_gs.cols - 1)
            new_blocks[i].coords.setY(new_col)
        
        return GameState(self.common_gs, self.blocks_as_list(new_blocks), move=Move.SWIPE_RIGHT, nMoves=(self.nMoves + 1))

    """
    Swipe Up Operation - Moves the movable blocks in the GameState upwards

    Returns the new GameState generated by that operation
    """
    def swipe_up(self):
        new_blocks = self.make_blocks_copy()
        new_blocks.sort(key=lambda el: el.coords.x)
        for i in range(len(new_blocks)):
            block = new_blocks[i]
            walls = sorted(filter(lambda el: el.coords.y == block.coords.y and el.coords.x < block.coords.x, new_blocks[:i] + self.common_gs.walls), key=lambda el: -el.coords.x)
            new_row = walls[0].coords.x + 1 if walls else 0
            new_blocks[i].coords.setX(new_row)
        
        return GameState(self.common_gs, self.blocks_as_list(new_blocks), move=Move.SWIPE_UP, nMoves=(self.nMoves + 1))

    """
    Swipe Down Operation - Moves the movable blocks in the GameState downwards

    Returns the new GameState generated by that operation
    """
    def swipe_down(self):
        new_blocks = self.make_blocks_copy()
        new_blocks.sort(key=lambda el: -el.coords.x)
        for i in range(len(new_blocks)):
            block = new_blocks[i]
            walls = sorted(filter(lambda el: el.coords.y == block.coords.y and el.coords.x > block.coords.x, new_blocks[:i] + self.common_gs.walls), key=lambda el: el.coords.x)
            new_row = walls[0].coords.x - 1 if walls else (self.common_gs.rows - 1)
            new_blocks[i].coords.setX(new_row)
        
        return GameState(self.common_gs, self.blocks_as_list(new_blocks), move=Move.SWIPE_DOWN, nMoves=(self.nMoves + 1))

    """
    Checks if game state is in final state, each block must match in one goal

    Returns true if represents a final state, false otherwise
    """
    def is_game_over(self):
        for block in self.blocks:
            found = False
            for goal in self.common_gs.goals:
                if block.color.lower() == goal.color.lower() and block.coords == goal.coords:
                    found = True
                    break
            if (not found):
                return False
        return True