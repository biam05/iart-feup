class Node:
    def __init__(self, game_state, parent=None, use_heuristic=False):
        """
        Constructor
        - GameState game_state  : current game_state
        - Node parent           : parent node
        - Boolean use_heuristic : use heuristics to estimate cost left

        """
        self.game_state = game_state
        self.parent = parent
        self.use_heuristic = use_heuristic
    
    def __lt__(self, other):
        """
        Less than operator
        - Node other : Other node
        
        Returns true if node on the left is lesser than the node on the right
        """
        return self.eval_node() < other.eval_node()

    def eval_node(self):
        """
        Evaluates the value of the node based on the GameState

        Returns the value of the node
        """
        return self.game_state.eval_game_state() #+ self.game_state.