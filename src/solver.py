from match_the_tiles.logic.reader import get_level, read_file
from graph.graph import Graph

from datetime import datetime

algorithms = {
    "bfs": lambda graph, initial: graph.bfs(initial),
    "dfs": lambda graph, initial: graph.dfs(initial),

    "ucs": lambda graph, initial: graph.uniform_cost_search(initial),
    "a-star": lambda graph, initial: graph.a_star(initial),
    "greedy": lambda graph, initial: graph.greedy(initial)
}

def solver(level_no, advanced, algorithm):
    game_state = get_level(level_no, advanced=advanced)

    graph = Graph(game_state)
    start_time = datetime.now()
    
    end_node = algorithms[algorithm](graph, game_state)
    end_time = datetime.now()

    path = []
    if end_node:
        path = graph.rebuild_path(end_node)
    else:
        print("No Solution")
        return

    elapsed_time = end_time-start_time

    return [algorithm, elapsed_time.total_seconds(), path,
            len(path), end_node.game_state.common_gs.goals, end_node.game_state.blocks,
            graph.expanded_nodes]

print(solver(15, True, "dfs"))