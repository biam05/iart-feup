from match_the_tiles.logic.game_state import GameState, CommonGameState

def get_level(level_no):
    file_name = "levels/" + level_no
    game_state = read_file(file_name)
    return game_state

def read_file(file_name):

    file = open(file_name, 'r')

    lines = file.readlines()

    x = 0
    y = 0
    rows = lines.len()
    cols = lines[0].len()
    walls = []
    goals = []
    blocks = []
    for line in lines:
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
        y = 0

    commonGameState = CommonGameState(walls, goals, rows, cols)
    return GameState(commonGameState, blocks)