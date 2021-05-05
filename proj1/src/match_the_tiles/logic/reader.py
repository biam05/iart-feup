from match_the_tiles.logic.game_state import GameState, CommonGameState


def get_level(level_no, advanced=False):
    sub_dir = "advanced" if advanced else "normal"
    file_name = f"levels/{sub_dir}/{level_no}"
    game_state = read_file(file_name)
    return game_state


def read_file(file_name):
    try:
        file = open(file_name, 'r')
    except:
        print("No More Levels")
        return False

    lines = file.readlines()

    rows = len(lines)
    cols = len(lines[0]) - 1
    walls = []
    goals = []
    blocks = []
    x = 0
    for line in lines:
        y = 0
        for char in line:
            if char == '#':
                walls.append([x, y])
            elif char.isalpha():
                if char.isupper():
                    goals.append([x, y, char])
                else:
                    blocks.append([x, y, char])
            y += 1
        x += 1

    commonGameState = CommonGameState(walls, goals, rows, cols)
    commonGameState.get_goal_surrounding_walls(rows, cols, walls, goals)
    return GameState(commonGameState, blocks)
