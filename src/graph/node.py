class Node:
    """
    Constructor
    - GameState game_state  : current game_state
    - Node parent           : parent node
    - Node edge             : operation used to obtain current state from parent 
    - Boolean use_heuristic : use heuristics to estimate cost left

    """
    def __init__(self, game_state, parent=None, edge=None, use_heuristic=False):
        self.game_state = game_state
        self.parent = parent
        self.edge = edge
        self.use_heuristic = use_heuristic

    def move(self, pos, new_pos):
        obj = self.matrix[pos[0]][pos[1]].block
        self.matrix[pos[0]][pos[1]].set_block("")
        self.matrix[new_pos[0]][new_pos[1]].set_block(obj) 

    def eval_node(self):
        return self.game_state.cost