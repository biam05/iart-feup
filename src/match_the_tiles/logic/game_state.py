from collections import defaultdict

from match_the_tiles.model.tile_data import WallData, BlockData, GoalData
from utils.utils import Coords
from utils.utils import CoordswithColor
import itertools

from enum import Enum
import sys

class Move(Enum):
    SWIPE_LEFT = 0
    SWIPE_DOWN = 1
    SWIPE_RIGHT = 2
    SWIPE_UP = 3

    def __str__(self):
        if self.name == "SWIPE_DOWN": return "Down"
        if self.name == "SWIPE_LEFT": return "Left"
        if self.name == "SWIPE_RIGHT": return "Right"
        if self.name == "SWIPE_UP": return "Up"

class CommonGameState:
    def __init__(self, walls : list, goals : list, rows : int, cols : int):
        """
        Constructor
        - List walls : List of coordinates of the walls (i.e. [x, y])
        - List goals : List of coordinates and colors of the goals (i.e. [x, y, color])
        - Int rows : Number of rows in the game board
        - Int cols : Number of cols in the game board
        """
        self.walls = list()
        for wall in walls:
            self.walls.append(WallData(Coords(wall[0], wall[1])))

        self.goals = list()
        for goal in goals:
            self.goals.append(GoalData(Coords(goal[0], goal[1]), goal[2]))

        self.rows = rows
        self.cols = cols
        self.proccessdict={}
        self.allWalls=walls

    #starts here
    def addExtraWalls(self,walls,cols,rows):
        i=0
        extrawalls=walls
        while i!=cols:
            extrawalls.extend([[-1,i],[cols,i]])
            extrawalls.extend([[i,-1],[i,rows]])
            i=i+1
        return extrawalls

    def get_goal_surrouding_walls(self,rows,cols,defaultwalls,goals):
        counter=1
        finaldict={}
        
        
        for goal in goals:
            walls=self.addExtraWalls(defaultwalls,cols,rows)
            for wall in walls:
                coord=CoordswithColor(wall[0],wall[1],goal[2])
                finaldict[coord]=[sys.maxsize,sys.maxsize,sys.maxsize,sys.maxsize]

            obstacleN = list(filter(lambda el: el[0] == goal[0]-1 and el[1] == goal[1], walls))
            if len(obstacleN):
                finaldict = self.updateDict(1,finaldict,0,obstacleN[0][0],obstacleN[0][1],goal[2])
                walls=[x for x in walls if x not in obstacleN]

            obstacleS = list(filter(lambda el: el[0] == goal[0]+1 and el[1] == goal[1], walls))
            if len(obstacleS):
                finaldict = self.updateDict(0,finaldict,0,obstacleS[0][0],obstacleS[0][1],goal[2])
                walls=[x for x in walls if x not in obstacleS]

            obstacleW = list(filter(lambda el: el[1] == goal[1]-1 and el[0] == goal[0], walls))
            if len(obstacleW):
                finaldict = self.updateDict(2,finaldict,0,obstacleW[0][0],obstacleW[0][1],goal[2])
                walls=[x for x in walls if x not in obstacleW]


            obstacleE = list(filter(lambda el: el[1] == goal[1]+1 and el[0] == goal[0], walls))
            if len(obstacleE):
                finaldict = self.updateDict(3,finaldict,0,obstacleE[0][0],obstacleE[0][1],goal[2])
                walls=[x for x in walls if x not in obstacleE]

            
            
            obstacles=[obstacleN,obstacleS,obstacleW,obstacleE]
            finaldict=self.insert_vips(goal, walls, rows, cols,obstacles,finaldict,counter)
        self.proccessdict=finaldict
        self.allWalls=self.addExtraWalls(defaultwalls,cols,rows)
        

    def insert_vips(self,goal, walls, rows, cols,obstacles, finaldict,counter):
        new_E_walls=[]
        new_W_walls=[]
        new_N_walls=[]
        new_S_walls=[]
        
        for wall in obstacles[0]:#N
            E_walls=list(filter(lambda el: el[1] == wall[1]+1 and el[0] > wall[0] and self.is_it_a_plane_is_it_a_bird_no_its_a_wall(2,walls,el,wall), walls))#0 for horizontal right, 1 for horizontal left, 2 for vertical up, 3 for vertical down
            W_walls=list(filter(lambda el: el[1] == wall[1]-1 and el[0] > wall[0] and self.is_it_a_plane_is_it_a_bird_no_its_a_wall(2,walls,el,wall), walls))
            new_E_walls.extend(E_walls)
            new_W_walls.extend(W_walls)
            
        for wall in obstacles[1]:#S
            E_walls=list(filter(lambda el: el[1] == wall[1]+1 and el[0] < wall[0] and self.is_it_a_plane_is_it_a_bird_no_its_a_wall(3,walls,el,wall), walls))
            W_walls=list(filter(lambda el: el[1] == wall[1]-1 and el[0] < wall[0] and self.is_it_a_plane_is_it_a_bird_no_its_a_wall(3,walls,el,wall), walls))
            new_E_walls.extend(E_walls)
            new_W_walls.extend(W_walls)

        for wall in obstacles[2]:#W
            N_walls=list(filter(lambda el: el[0] == wall[0]-1 and el[1] > wall[1] and self.is_it_a_plane_is_it_a_bird_no_its_a_wall(0,walls,wall,el), walls))
            S_walls=list(filter(lambda el: el[0] == wall[0]+1 and el[1] > wall[1] and self.is_it_a_plane_is_it_a_bird_no_its_a_wall(0,walls,wall,el), walls))
            new_N_walls.extend(N_walls)
            new_S_walls.extend(S_walls)

        for wall in obstacles[3]:#E
            N_walls=list(filter(lambda el: el[0] == wall[0]-1 and el[1] < wall[1] and self.is_it_a_plane_is_it_a_bird_no_its_a_wall(1,walls,wall,el), walls))
            S_walls=list(filter(lambda el: el[0] == wall[0]+1 and el[1] < wall[1] and self.is_it_a_plane_is_it_a_bird_no_its_a_wall(1,walls,wall,el), walls))
            new_N_walls.extend(N_walls)
            new_S_walls.extend(S_walls)

        new_N_walls.sort()
        new_N_walls=list(k for k,_ in itertools.groupby(new_N_walls))
        new_S_walls.sort()
        new_S_walls=list(k for k,_ in itertools.groupby(new_S_walls))
        new_E_walls.sort()
        new_E_walls=list(k for k,_ in itertools.groupby(new_E_walls))
        new_W_walls.sort()
        new_W_walls=list(k for k,_ in itertools.groupby(new_W_walls))
        for wall in new_N_walls:
            finaldict = self.updateDict(1,finaldict,counter,wall[0],wall[1],goal[2])

        for wall in new_S_walls:
            finaldict = self.updateDict(0,finaldict,counter,wall[0],wall[1],goal[2])

        for wall in new_E_walls:
            finaldict = self.updateDict(3,finaldict,counter,wall[0],wall[1],goal[2])

        for wall in new_W_walls:
            finaldict = self.updateDict(2,finaldict,counter,wall[0],wall[1],goal[2])
            

        counter=counter+1
        walls=[x for x in walls if x not in new_E_walls]
        walls=[x for x in walls if x not in new_W_walls]
        walls=[x for x in walls if x not in new_N_walls]
        walls=[x for x in walls if x not in new_S_walls]

        obstacles=[new_N_walls,new_S_walls,new_W_walls,new_E_walls]
        if((not new_N_walls) and (not new_S_walls) and (not new_E_walls) and (not new_W_walls)):
            return finaldict
        
        result=self.insert_vips(goal, walls, rows, cols,obstacles,finaldict,counter)
        return result
    
    def updateDict(self,orientation,finaldict,counter,x,y,goal):
        coord=CoordswithColor(x,y,goal)
        previous=finaldict.get(coord)
        previous[orientation]=counter
        finaldict.update({coord:previous})
        return finaldict

    def is_it_a_plane_is_it_a_bird_no_its_a_wall(self,orientation,walls,element,chosenwall):
        for wall in walls:
            if orientation==0:
                if(wall[1]>chosenwall[1] and wall[0]==chosenwall[0]):
                    if(element[1]>=wall[1]):
                        return False
            if orientation==1:
                if(wall[1]<chosenwall[1] and wall[0]==chosenwall[0]):
                    if(element[1]<=wall[1]):
                        return False
            if orientation==2:
                if(wall[0]>chosenwall[0] and wall[1]==chosenwall[1]):
                    if(element[0]>=wall[0]):
                        return False
            if orientation==3:
                if(wall[0]<chosenwall[0] and wall[1]==chosenwall[1]):
                    if(element[0]<=wall[0]):
                        return False
        return True
    #ends here

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
    
    def __repr__(self):
        out = ""
        matrix = self.getGameStateMatrix()
        for i in matrix:
            out += "\n"
            for j in i:
                out += j + "\t"
        out += "\n"
        return out

    """
    Makes A Matrix with the board
    """
    def getGameStateMatrix(self):
        matrix = []
        for i in range(self.common_gs.rows):
            line = []
            for j in range(self.common_gs.cols):
                coord = Coords(i, j)
                tipo = "."
                for block in self.blocks:
                    if coord == block.coords:
                        tipo = block.color
                        break
                for goal in self.common_gs.goals:
                    if tipo != ".": break
                    if coord == goal.coords:
                        tipo = goal.color
                        break
                for wall in self.common_gs.walls:
                    if tipo != ".": break
                    if coord == wall.coords:
                        tipo = "#"
                        break
                line.append(tipo)
            matrix.append(line)
        return matrix

    """
       Makes A Dictionary with the board
    """
    def getGameStateDictionary(self):
        d = defaultdict(list)
        for block in self.blocks:
            d[block.coords].append(block.color)
        for goal in self.common_gs.goals:
            d[goal.coords].append(goal.color)
        for wall in self.common_gs.walls:
            d[wall.coords].append("#")
        return d

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
        return self.nMoves

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

    Returns the estimate number of moves needed to finish the game 
    """
    def estimate_moves_left(self):
        moves = 0

        for block in self.blocks:
            local_moves = sys.maxsize
            block_x = block.coords.x
            block_y = block.coords.y
            colinear_goals = filter(lambda el: el.color.upper() == block.color.upper() and (el.coords.x == block.coords.x or el.coords.y == block.coords.y), self.common_gs.goals)
            # colinear
            if colinear_goals:
                for goal in colinear_goals:
                    goal_x = goal.coords.x
                    goal_y = goal.coords.y
                    if goal_x == block_x and goal_y == block_y:
                        local_moves = min(local_moves, 0)
                        break
                    obstacles = filter(lambda el: el != block and el.in_between(goal, block), self.blocks + self.common_gs.walls)
                    # has an obstacle between the block and the goal
                    if obstacles:
                        local_moves = min(local_moves, 3)
                    else:
                        print(block_x, block_y, goal_x, goal_y)
                        if (goal_x == block_x and (goal_y == 0 or goal_y == self.common_gs.cols - 1)) or (goal_y == block_y and (goal_x == 0 or goal_x == self.common_gs.rows - 1)):
                            local_moves = min(local_moves, 1)
                        else:
                            obstacles = filter(lambda el: self.is_wall_stopping_block_at_goal(block, goal, el), self.common_gs.walls)
                            local_moves = min(local_moves, 1 if obstacles else 2)
            # non-colinear
            else:
                local_moves = min(local_moves, 2)

            moves = max(moves, local_moves)
        return moves


    def choose_path(self):
        value=[sys.maxsize,sys.maxsize,sys.maxsize,sys.maxsize]
        walls=self.common_gs.allWalls
        for block in self.blocks:
            #Check if block to the north
            wallTOnorth=next(filter(lambda el: el[0] == block.coords.x-1 and el[1] == block.coords.y,walls),False)
            if wallTOnorth:
                coord=CoordswithColor(wallTOnorth[0],wallTOnorth[1],block.color.upper())
                allValues=self.common_gs.proccessdict.get(coord)
                value[0]=min(value[0],allValues[1])
                

            #Check if block to the south
            wallTOsouth=next(filter(lambda el: el[0] == block.coords.x+1 and el[1] == block.coords.y,walls),False)
            if wallTOsouth:
                coord=CoordswithColor(wallTOsouth[0],wallTOsouth[1],block.color.upper())
                allValues=self.common_gs.proccessdict.get(coord)
                value[1]=min(value[1],allValues[0])

            #Check if block to the east
            wallTOeast=next(filter(lambda el: el[0] == block.coords.x and el[1] == block.coords.y+1,walls),False)
            if wallTOeast:
                coord=CoordswithColor(wallTOeast[0],wallTOeast[1],block.color.upper())
                allValues=self.common_gs.proccessdict.get(coord)
                value[2]=min(value[2],allValues[3])

            #Check if block to the west
            wallTOwest=next(filter(lambda el: el[0] == block.coords.x and el[1] == block.coords.y-1,walls),False)
            if wallTOwest:
                coord=CoordswithColor(wallTOwest[0],wallTOwest[1],block.color.upper())
                allValues=self.common_gs.proccessdict.get(coord)
                value[3]=min(value[3],allValues[2])
        return min(value)

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

    def __eq__(self, other):
        self_blocks = sorted(self.blocks, key=lambda el: (el.coords.x, el.coords.y))
        other_blocks = sorted(other.blocks, key=lambda el: (el.coords.x, el.coords.y))
        return all(map(lambda x, y: x == y, self_blocks, other_blocks))

    def __hash__(self):
        return hash(tuple(sorted(self.blocks, key=lambda el: (el.coords.x, el.coords.y,))))