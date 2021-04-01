from match_the_tiles.logic.reader import get_level, read_file
from graph.graph import Graph

from datetime import datetime

algorithms = {
    "bfs": lambda graph, initial: graph.bfs(initial),

    "ucs": lambda graph, initial: graph.uniform_cost_search(initial),
    "a-star": lambda graph, initial: graph.a_star(initial)
}

def solver(level_no, advanced, algorithm):
    game_state = get_level(level_no, advanced=advanced)

    graph = Graph(game_state)
    start_time = datetime.now()
    
    end_node = algorithms[algorithm](graph, game_state)

    end_time = datetime.now()

    path = graph.rebuild_path(end_node)

    elapsed_time = end_time-start_time

    print(f"Running algorithm {algorithm}")
    print(f"Elapsed time - {elapsed_time.total_seconds()}s")
    print(f"Move list - {path}")
    print(f"Number of moves - {len(path)}")
    print(f"Goals - {end_node.game_state.common_gs.goals}")
    print(f"Blocks final positions - {end_node.game_state.blocks}")    
    print(f"Expanded Nodes - PLACEHOLDER")

    return [algorithm, elapsed_time.total_seconds(), path,
            len(path), end_node.game_state.common_gs.goals, end_node.game_state.blocks,
            2]

solver(16, True, "bfs")

