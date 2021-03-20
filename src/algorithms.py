from queue import PriorityQueue

class AStar: 
    @staticmethod
    def astar(game_state, start, goal, heuristic):
        toVisit = PriorityQueue() # Coords
        f_cost = dict() # Coord : Cost
        g_cost = dict() # Coord : Cost

        toVisit.put((0, start))
        