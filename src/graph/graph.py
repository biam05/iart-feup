from node import Node
from collections import defaultdict
from copy import deepcopy
import queue

class Graph:
    """
    Constructor
    - 
    """
    def __init__(self, walls, goals, gamestate): # gamestate -> node
        self.walls = walls
        self.goals = goals
        self.graph = defaultdict(list)

    """
    Adds edge from the source node to dest node
    - Node source   : parent node
    - Node dest     : child node
    """
    def add_edge(self, source, dest):
        self.graph[source].append(None)
    
    def is_game_over(self, gamestate):
        n_goals = self.goals.len()
        n_correct_goals = 0
        for goal in self.goals:
            goal_x = goal[0]
            goal_y = goal[1]
            goal_color = goal[2]
            for block in gamestate:
                block_x = block[0]
                block_y = block[1]
                block_color = block[2]
                if goal_x == block_x and goal_y == block_y and goal_color == block_color:
                    n_correct_goals += 1
                    break
        if n_correct_goals == n_goals:
            return True
        return False
    
    def bfs(self, node):
        visited = []
        queue = []
        visited.append(node)
        queue.append(node)
        while queue:
            s = queue.pop(0)
            if self.is_game_over(self, s):
                return s
            neighbours = self.get_neighbours(self, node)[s]
            for neighbour in neighbours:
                if neighbour not in visited:
                    visited.append(neighbour)
                    queue.append(neighbour)

    def ucs(self, node):
        visited = set()
        q = queue.ProrityQueue()
        q.put((0,node,[node]))
        while not q.empty():
            cost, current_node, path = q.get()
            visited.add(current_node)
            if self.is_game_over(self, current_node):
                return path
            else:
                neighbours = self.get_neighbours(self, node)[current_node]
                for neighbour in neighbours:
                    if neighbour not in visited:
                        q.put((cost, neighbour))
    
    def get_neighbours(self, node):
        neighbours = []
        neighbours.append(self.swipe_left(self, node))
        neighbours.append(self.swipe_right(self, node))
        neighbours.append(self.swipe_up(self, node))
        neighbours.append(self.swipe_down(self, node))
        return neighbours

    def swipe_left(self, gamestate):
        node = deepcopy(gamestate)
        node.parent = gamestate
        node.blocks.sort(key=lambda el: el[1])
        for i in range(len(node.blocks)):
            block = node.blocks[i]
            self.walls = sorted(filter(lambda el: el[0] == block[0] and el[1] < block[1], self.walls + node.blocks[:i]), key=lambda el: -el[1])
            new_col = node.walls[0][1] + 1 if self.walls else 0
            self.move(block, (block[0], new_col))
            node.blocks[i][1] = new_col
        return node
    
    def swipe_right(self, gamestate):
        node = deepcopy(gamestate)
        node.parent = gamestate
        node.blocks.sort(key=lambda el: -el[1])
        for i in range(len(node.blocks)):
            block = node.blocks[i]
            self.walls = sorted(filter(lambda el: el[0] == block[0] and el[1] > block[1], self.walls + node.blocks[:i]), key=lambda el: el[1])
            new_col = self.walls[0][1] - 1 if self.walls else (self.cols - 1)
            self.move(block, (block[0], new_col))
            node.blocks[i][1] = new_col
        return node

    def swipe_up(self, gamestate):
        node = deepcopy(gamestate)
        node.parent = gamestate
        node.blocks.sort(key=lambda el: el[0])
        for i in range(len(node.blocks)):
            block = node.blocks[i]
            self.walls = sorted(filter(lambda el: el[1] == block[1] and el[0] < block[0], self.walls + node.blocks[:i]), key=lambda el: -el[0])
            new_row = self.walls[0][0] + 1 if self.walls else 0
            self.move(block, (new_row, block[1]))
            node.blocks[i][0] = new_row
        return node

    def swipe_down(self, gamestate):
        node = deepcopy(gamestate)
        node.parent = gamestate
        node.blocks.sort(key=lambda el: -el[0])
        for i in range(len(node.blocks)):
            block = node.blocks[i]
            self.walls = sorted(filter(lambda el: el[1] == block[1] and el[0] > block[0], self.walls + node.blocks[:i]), key=lambda el: el[0])
            new_row = self.walls[0][0] - 1 if self.walls else (self.rows -1)
            self.move(block, (new_row, block[1]))
            node.blocks[i][0] = new_row
        return node




    
