from src.match_the_tiles.logic.reader import get_level, read_file
from graph.graph import Graph
from match_the_tiles.logic.game_state import GameState
import match_the_tiles.logic.reader

def solver(level_no):
    gameState = get_level(level_no)
    graph = Graph(gameState)
