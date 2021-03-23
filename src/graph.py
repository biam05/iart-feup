from node import Node
class Graph:
    def __init__(walls, goals, gamestate): # gamestate -> node
        self.walls = walls
        self.goals = goals
        self.gamestate = gamestate
    
    def is_game_over(self):
        n_goals = goals.len()
        n_correct_goals = 0
        for goal in self.goals:
            goal_x = goal[0]
            goal_y = goal[1]
            goal_color = goal[2]
            for block in self.gamestate:
                block_x = block[0]
                block_y = block[1]
                block_color = block[2]
                if goal_x == block_x and goal_y == block_y and goal_color == block_color:
                    n_correct_goals += 1
                    break
        if n_correct_goals == n_goals:
            return True
        return False

    
