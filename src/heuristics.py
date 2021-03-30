from game_state import *
import math

"""
Calculate the euclidean distance between blocks and goals
-> game_state : GameState
-> dist_func : Function - operation to perform on the collection of distances from all the blocks
-> node_func : Function - operation to perform on the collection of distances from a specific block
"""
def euclidean_distance(game_state, dist_func, node_func):
    dists = []
    for block in game_state.blocks:
        color_block = game_state.matrix[block[0]][block[1]].block
        node_dists = []
        for goal in game_state.goals:
            color_goal = game_state.matrix[goal[0]][goal[1]].goal
            if color_block == color_goal:
                # d = sqrt((x2-x1)**2 + (y2-y1)**2)
                dnode = math.sqrt(math.pow((block[0]-goal[0]),2)+math.pow((block[1]-goal[1]),2))
                node_dists.append(dnode)
        d = node_func(node_dists)
        dists.append(d)
    return dist_func(dists)

"""
Calculate the manhattan distance between blocks and goals
-> game_state : GameState
-> dist_func : Function - operation to perform on the collection of distances from all the blocks
-> node_func : Function - operation to perform on the collection of distances from a specific block
"""
def manhattan_distance(game_state):
    sum_dist = 0