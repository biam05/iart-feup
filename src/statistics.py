import sys

from match_the_tiles.logic.options import HeuristicOptions

from solver import solver
from solver import algorithms
import numpy as np

N_TRIALS = 20

heuristics = [
    HeuristicOptions(estimate_moves=True, collisions=False, euc_dist=False, man_dist=False, dist_func=min, node_func=min),
    HeuristicOptions(estimate_moves=False, collisions=True, euc_dist=False, man_dist=False, dist_func=min, node_func=min),
    HeuristicOptions(estimate_moves=False, collisions=False, euc_dist=True, man_dist=False, dist_func=min, node_func=min),
    HeuristicOptions(estimate_moves=False, collisions=False, euc_dist=False, man_dist=True, dist_func=min, node_func=min),
    HeuristicOptions(estimate_moves=True, collisions=True, euc_dist=True, man_dist=True, dist_func=min, node_func=min),
    HeuristicOptions(estimate_moves=True, collisions=True, euc_dist=False, man_dist=False, dist_func=min, node_func=min),
    HeuristicOptions(estimate_moves=False, collisions=False, euc_dist=True, man_dist=False, dist_func=min, node_func=np.mean),
    HeuristicOptions(estimate_moves=False, collisions=False, euc_dist=False, man_dist=True, dist_func=min, node_func=np.mean),
    HeuristicOptions(estimate_moves=False, collisions=False, euc_dist=True, man_dist=False, dist_func=np.mean, node_func=min),
    HeuristicOptions(estimate_moves=False, collisions=False, euc_dist=False, man_dist=True, dist_func=np.mean, node_func=min),
    HeuristicOptions(estimate_moves=False, collisions=False, euc_dist=True, man_dist=False, dist_func=np.mean, node_func=np.mean),
    HeuristicOptions(estimate_moves=False, collisions=False, euc_dist=False, man_dist=True, dist_func=np.mean, node_func=np.mean),
    HeuristicOptions(estimate_moves=True, collisions=False, euc_dist=True, man_dist=False, dist_func=np.mean, node_func=np.mean),
    HeuristicOptions(estimate_moves=True, collisions=False, euc_dist=False, man_dist=True, dist_func=np.mean, node_func=np.mean),
    HeuristicOptions(estimate_moves=True, collisions=False, euc_dist=True, man_dist=False, dist_func=min, node_func=min),
    HeuristicOptions(estimate_moves=True, collisions=False, euc_dist=False, man_dist=True, dist_func=min, node_func=min)
]

def run_algorithm(algorithm):
    print(algorithm)
    print(f"Level, Expanded Nodes ({algorithm}), Time ({algorithm}), Number of Moves ({algorithm}), Moves")
    for level in range(1, 43):
        n_level = level - 20 if level > 20 else level
        level_suffix = "A" if level > 20 else ""
        times = []
        solution = []
        nMoves = -1
        expanded_nodes = -1
        for _ in range(N_TRIALS):
            _, time, solution, nMoves, _, _, expanded_nodes = solver(n_level, level > 20, algorithm)
            times.append(time)

        print(", ".join(map(str, [str(n_level) + level_suffix, expanded_nodes, np.mean(times), nMoves, solution])))

def run_algorithms():
    sys.stdout = open("statistics/algorithms.csv", "w+")
    for alg in algorithms.keys():
        run_algorithm(alg)

def run_heuristic(options):
    print(options)
    print(f"Level, Expanded Nodes ({options}), Time ({options}), Number of Moves ({options}), Difference to Optimal ({options}), Moves")
    for level in range(1, 43):
        n_level = level - 20 if level > 20 else level
        level_suffix = "A" if level > 20 else ""
        times = []
        solution = []
        nMoves = -1
        expanded_nodes = -1
        for _ in range(N_TRIALS):
            _, time, solution, nMoves, _, _, expanded_nodes = solver(n_level, level > 20, "a-star", options)
            times.append(time)

        _, _, _, optimal_moves, _, _, _ = solver(n_level, level > 20, "bfs")

        print(", ".join(map(str, [str(n_level) + level_suffix, expanded_nodes, np.mean(times), nMoves, nMoves - optimal_moves, solution])))

def run_heuristics():
    sys.stdout = open("statistics/heuristics.csv", "w+")
    for options in heuristics:
        run_heuristic(options)

if __name__ == "__main__":
    run_algorithms()
    run_heuristics()