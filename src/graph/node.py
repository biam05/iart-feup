class Node:
    def __init__(self, game_state, path=None, parent=None, use_heuristic=False, nodecost=True):
        """
        Constructor
        - GameState game_state  : current game_state
        - Node parent           : parent node
        - Boolean use_heuristic : use heuristics to estimate cost left
        - Boolean nodecost      : use node cost to estimate cost left

        """
        self.game_state = game_state
        self.parent = parent
        self.use_heuristic = use_heuristic
        self.nodecost = nodecost
        self.path = []
        if path:
            self.path = path

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
        result = 0
        if self.nodecost:
            result += self.game_state.eval_game_state()
        if self.use_heuristic:
            result += self.game_state.calc_heuristic()
        return result
