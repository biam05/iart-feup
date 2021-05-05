# Match the Tiles (G12)

## Project Group

| Name                                    | Number      |
| :-------------------------------------- | :---------- | 
| Beatriz Costa Silva Mendes              | up201806551 |
| Nuno Guilherme Amaral Santos            | up201405774 |
| Telmo Alexandre Espírito Santo Baptista | up201806554 |

## Dependencies
Outside the default libraries included in Python, it was used the library `numpy`, and such the library must be installed before running our program.
The library can be installed using `pip install numpy`.

It was also used the library `pygame` to build the graphic interface. This library can also be installed with `pip install pygame`.

## How to Run

Run the command `python matchthetiles.py` inside the folder `src` and a menu containing the graphic interface should be displayed.
To run the statistics module, that generates the files containing the analysis of each algorithm and heuristic studied, run the file `statistic.py` inside the `src` folder using `python statistics.py`

## The Solver

The `Solver` menu displays all the available levels to test and after choosing a level, a new menu is presented with all the search algorithms implemented (BFS, DFS, UCS, Greedy and A*).
After all these selections, it's presented the initial board (it is playable using the arrow keys) and data about the search (time elapsed, number of moves, moves, expanded nodes, blocks and goals).

## How to Play

Swipe (Up, Down, Left, Right) using the arrow keys to move the tiles. You should place all colored tiles onto the designated spots with the same color. The moves are synchronized, thus you must use existing fixed tiles to create gaps between tiles and solve the puzzle.

In Normal Mode there are 20 available levels and in Advanced Mode there are 22 available levels. 


