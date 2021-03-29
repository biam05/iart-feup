from match_the_tiles.logic.game_state import GameState, CommonGameState

def get_level(level_no):
    file_name = "levels/" + level_no
    game_state = read_file(file_name)

def read_file(file_name):
    file = open(file_name, 'r')

    lines = file.readlines()