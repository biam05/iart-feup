from copy import deepcopy
from collections import OrderedDict

INF = float('inf')

class AStar:
    @staticmethod
    def astar(game_state, heuristic):
        toVisit = dict() # Coords
        visited = list() # Coords
        f_cost = dict() # Coord : Cost
        g_cost = dict() # Coord : Cost

        f_cost[game_state] = 0
        g_cost[game_state] = 0
        toVisit[game_state] = f_cost.get(game_state, INF)

        move_map = dict()
        move_set = list()

        while toVisit:
            pair = [(key,value) for key, value in sorted(toVisit.items(), key=lambda item: item[1])][0]

            current = pair[0]
            toVisit.pop(current)
            visited.append(current)
            move_set.append(move_map.get(current, "INITIAL"))
            
            if (current.is_game_over()):
                break

            for i in range(4):
                new_game_state = deepcopy(game_state)
                move = ""
                if i == 0: # swipe down
                    new_game_state.swipe_down()
                    move = "DOWN"
                elif i == 1: # swipe up
                    new_game_state.swipe_up()
                    move = "UP"
                elif i == 2: #swipe left
                    new_game_state.swipe_left()
                    move = "LEFT"
                elif i == 3: # swipe right
                    new_game_state.swipe_right()
                    move = "RIGHT"
                if new_game_state in visited:
                    continue

                heuristic_value = heuristic(new_game_state)
                temp_cost = g_cost.get(game_state, INF) + heuristic_value

                if g_cost.get(new_game_state, INF) > temp_cost:
                    g_cost[new_game_state] = temp_cost
                    f_cost[new_game_state] = g_cost[new_game_state] +  heuristic_value
                    move_map[new_game_state] = move
                    
                    toVisit[new_game_state] = f_cost.get(new_game_state, INF)

                    
