from game_state import *

"""
Calculate the euclidean distance between blocks and goals
-> game_state : GameState
-> dist_func : Function - operation to perform on the collection of distances from all the blocks
-> node_func : Function - operation to perform on the collection of distances from a specific block
"""
def euclidean_distance(game_state, dist_func, node_func):
    dists = []
    for block in game_state.blocks:
        node_dists = []
        for goal in game_state.goals:

"""
Calculate the manhattan distance between blocks and goals
-> game_state : GameState
-> dist_func : Function - operation to perform on the collection of distances from all the blocks
-> node_func : Function - operation to perform on the collection of distances from a specific block
"""
def manhattan_distance(game_state):
    sum_dist = 0