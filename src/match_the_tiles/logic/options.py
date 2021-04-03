from dataclasses import dataclass
from typing import Callable


@dataclass
class HeuristicOptions:
<<<<<<< HEAD
    estimate_moves : bool = True
    collisions : bool = False
    euc_dist : bool = True
    man_dist : bool = False
    dist_func : Callable[[list], float] = min
    node_func : Callable[[list], float] = min
=======
    estimate_moves: bool = True
    collisions: bool = False
    euc_dist: bool = False
    man_dist: bool = False
    dist_func: Callable[[list], float] = min
    node_func: Callable[[list], float] = min
>>>>>>> cbe990c6cedb7d199829bf188d4b6b973530d212

    def __str__(self):
        value = []
        if self.estimate_moves:
            value.append("EM")
        if self.collisions:
            value.append("COL")
        if self.euc_dist:
            value.append("EDIST")
        if self.man_dist:
            value.append("MDIST")
        if self.euc_dist or self.man_dist:
            value.append(f"DF({self.dist_func.__name__})")
            value.append(f"NF({self.node_func.__name__})")
        return "-".join(value)
