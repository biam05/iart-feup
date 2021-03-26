from graph.node import Node
from collections import defaultdict
from copy import deepcopy
import queue

class Graph:
    """
    Constructor
    - 
    """
    def __init__(self, gamestate):
        self.graph = defaultdict(list)

    """
    Adds edge from the source node to dest node
    - Node source   : parent node
    - Node dest     : child node
    """
    def add_edge(self, source, dest):
        node = Node(dest, parent=source)
        self.graph[source].append(node)
        return node
    
    def get_edges(self, node):
        edges = []
        edges.append(node.game_state.swipe_left())
        edges.append(node.game_state.swipe_right())
        edges.append(node.game_state.swipe_up())
        edges.append(node.game_state.swipe_down())
        return edges
    
    """
    Performs a blind search using the algorithm specified
    - GameState start : startinga GameState
    - Function algorithm : Function that decides which node to expand next
    """
    def blind_search(self, start, algorithm):
        visited = defaultdict(bool)

        start_node = Node(start)
        queue = [start_node]

        visited[start] = True

        while queue:
            current = queue.pop(0)

            if current.game_state.is_game_over():
                return current

            for edge in self.get_edges(current):
                node = self.add_edge(current.game_state, edge)
                
                algorithm(queue, node, visited)

        return None

    @staticmethod
    def __bfs(queue, node, visited):
        if visited[node.game_state]:
            return
        queue.append(node)
        visited[node.game_state] = True


    """
    Performs a directed search using the algorithm specified
    - GameState start : startinga GameState
    - Function algorithm : Function that decides which node to expand next
    """
    def directed_search(self, start, algorithm):

        return None

"""
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
    
