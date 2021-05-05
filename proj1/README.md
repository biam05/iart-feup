# Match the Tiles (G12)

## Project Group
| Name                                    | Number      |
| :-------------------------------------- | :---------- | 
| Beatriz Costa Silva Mendes              | up201806551 |
| Nuno Guilherme Amaral Santos            | up201405774 |
| Telmo Alexandre Espírito Santo Baptista | up201806554 |


## Game description
> specification of the work to be performed (definition of the game or optimization problem to be solved)

> Swipe (Up, Down, Left, Right) to move the tiles. You should place all colored tiles onto the designated spots with the same color. The moves are synchronized, thus you must use existing fixed tiles to create gaps between tiles and solve the puzzle.

*Match the Tiles* consists of swiping the colored tiles into their designated spots with the same color. 

### Rules
- All movable tiles move as a group
- You can only swipe up, down, left or right
- Tile color and goal color must all match to beat the game
- Tiles must not go over obstacles

## Formulation of the problem as search problem
> formulation of the problem as a search problem (~~state representation~~, ~~initial state~~, ~~objective test~~, operators (names, preconditions, effects and costs), heuristics/evaluation function)

- **States**: Specifies the position of each colored tile, the spots, the empty spaces and the obstacles
- **Initial State**: Generated game
- **Successor Operators**: generates valid states thar result from execution. There are the four actions (move the colored tiles left, right, up and down)
- **Objective Test**: checks whether the state corresponds to the objective configuration (all the colored tiles are in their designated spots)
- **Solution Cost**: Each step costs 1, the cost of the solution being the
number of steps to solve the problem

- **Operators**
    1. **Move Colored Tiles to the Left**
       - **Preconditions**: the colored tile that will be moved can't have an obstacle directly to it's left
       - **Effects**: the colored tiles move to the left
       - **Costs**: 1
    2. **Move  Colored Tiles to the Right**
       - **Preconditions**: the colored tile that will be moved can't have an obstacle directly to it's right
       - **Effects**: the colored tiles move to the right
       - **Costs**: 1
    3. **Move Colored Tiles to the Top**
       - **Preconditions**: the colored tile that will be moved can't have an obstacle directly on top of it
       - **Effects**: the colored tiles move to the top
       - **Costs**: 1
    4. **Move  Colored Tiles to the Bottom**
       - **Preconditions**: the colored tile that will be moved can't have an obstacle directly below it
       - **Effects**: the colored tiles move to the bottom
       - **Costs**: 1


- **Heuristics**

```py
def h():
cost = 0  
for each moved_tile:
    cost += dist(tile, goals) 
```

## Implementation
> implementation work already carried out (programming language, development environment, data structures, file structure, among others)
- Programming Language: Python
- Used Libraries: Pygame, TBD

## References
[Google Play - Match the Tiles](https://play.google.com/store/apps/details?id=net.bohush.match.tiles.color.puzzle&hl=pt_PT&gl=US)
[Match Tiles - Sliding Puzzle Game](https://www.youtube.com/watch?v=_6Yzx5eVVUs&ab_channel=ViktorBohush)
