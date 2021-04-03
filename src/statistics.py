import sys

from solver import solver
from solver import algorithms
import numpy as np

N_TRIALS = 20

def run_algorithm(levels, algorithm):
    print(algorithm)
    print(f"Level, Expanded Nodes ({algorithm}), Time ({algorithm}), Number of Moves ({algorithm}), Moves")
    for level in levels:
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
        run_algorithm(range(1, 43), alg)

if __name__ == "__main__":
    run_algorithms()