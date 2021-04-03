from graph.node import Node
from collections import defaultdict
from copy import deepcopy
from queue import PriorityQueue

class Graph:
    """
    Constructor
    - 
    """
    def __init__(self, gamestate):
        self.graph = defaultdict(list)
        self.nodes = defaultdict(Node)
        self.nodes.default_factory = lambda: None
        self.initial = gamestate
        self.expanded_nodes = 0

    """
    Adds edge from the source node to dest node
    - Node source   : parent node
    - Node dest     : child node
    """
    def add_edge(self, source, dest, heuristics=False, nodecost=True):
        node = self.nodes[dest]
        if node is None:
            node = Node(dest, parent=source, use_heuristic=heuristics, nodecost=nodecost)
            self.nodes[dest] = node
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
    def __blind_search(self, start, algorithm):
        visited = defaultdict(bool)

        start_node = Node(start)
        queue = [start_node]

        visited[start] = True

        self.expanded_nodes = 0

        while queue:
            current = queue.pop(0)

            self.expanded_nodes += 1

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

    def bfs(self, start):
        return self.__blind_search(start, self.__bfs)

    """
    Performs a directed search using the algorithm specified
    - GameState start : starting GameState
    - Function algorithm : Function that decides which node to expand next
    """
    def __directed_search(self, start, heuristics=False, nodecost=True):
        visited = defaultdict(bool)

        queue = PriorityQueue()
        queue.put(Node(start, use_heuristic=heuristics, nodecost=nodecost))

        visited[start] = True
        self.expanded_nodes = 0

        while queue:
            current = queue.get()

            self.expanded_nodes += 1

            if current.game_state.is_game_over():
                return current

            for edge in self.get_edges(current):
                node = self.add_edge(current.game_state, edge, heuristics=heuristics, nodecost=nodecost)

                if visited[node.game_state]:
                    continue
                queue.put(node)
                visited[node.game_state] = True

        return None
    
    def uniform_cost_search(self, start):
        return self.__directed_search(start, heuristics=False, nodecost=True)

    def a_star(self, start):
        return self.__directed_search(start, heuristics=True, nodecost=True)

    def greedy(self, start):
        return self.__directed_search(start, heuristics=True, nodecost=False)

    def rebuild_path(self, node):
        path = list()
        if node.game_state.move:
            path.append(node.game_state.move)
        parent_gs = node.parent
        parent_node = self.nodes[parent_gs]

        while parent_node:
            if parent_node.game_state.move:
                path.append(parent_node.game_state.move)
            parent_gs = parent_node.parent
            if parent_gs == None:
                break
            parent_node = self.nodes[parent_gs]
            break
        path.reverse()
        return path