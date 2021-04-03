import sys

from solver import solver

def run_algorithm(levels, advanced, algorithm):
    levels_sufix = "adv" if advanced else "normal"
    sys.stdout = open(algorithm + levels_sufix + ".csv", "w")

    print("Level, Expanded Nodes, Number of Moves, Moves")
    for level in levels:
        _, time, solution, nMoves, _, _, expanded_nodes = solver(level, advanced, algorithm)

        print()