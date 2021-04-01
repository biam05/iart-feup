from match_the_tiles.logic.reader import get_level, read_file
from graph.graph import Graph
from match_the_tiles.logic.game_state import GameState
import match_the_tiles.logic.reader


def game(level_no, advanced):
    game_state = get_level(level_no, advanced=advanced)
    
    while(not game_state.is_game_over()):        
        print(game_state)
        direction = get_valid_input()
        if direction == "L":
            game_state = game_state.swipe_left()  
            print("Move: Left")
        elif direction == "U":
            game_state = game_state.swipe_up()
            print("Move: Up")
        elif direction == "R":
            game_state = game_state.swipe_right()  
            print("Move: Right")
        elif direction == "D":
            game_state = game_state.swipe_down()  
            print("Move: Down")
        elif direction == "H":
            print("Hints not Implemented Yet")
            
    print(game_state)
    print("Finished Level")

def get_valid_input():
    while(True):
        direction = input("L(eft) U(p) R(ight) D(own) or H(int): ")
        if direction.upper() in ["L", "U", "R", "D", "H"] :
            return direction.upper() 


game(1, False)