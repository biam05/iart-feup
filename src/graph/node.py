class Node:
    """
    Constructor
    - GameState game_state  : current game_state
    - Node parent           : parent node
    - Boolean use_heuristic : use heuristics to estimate cost left

    """
    def __init__(self, game_state, parent=None, use_heuristic=False):
        self.game_state = game_state
        self.parent = parent
        self.use_heuristic = use_heuristic
    
    """
    Less than operator
    - Node other : Other node
    
    Returns true if node on the left is lesser than the node on the right
    """
    def __lt__(self, other):
        return self.eval_node() < other.eval_node()

    """
    Evaluates the value of the node based on the GameState

    Returns the value of the node
    """
    def eval_node(self):
        return self.game_state.cost