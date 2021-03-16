import pygame, sys
from pygame.locals import *
from game_state import GameState

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

test_state = [
    [1, 1, 0, 1],
    [0, 1, [2, "purple"], 0],
    [[3, "purple"], 1, [2, "purple"], 1],
    [0, 0, 0, [3, "purple"]]
]

game_state = GameState(test_state)

print(game_state)

game_state.swipe_down()

print(game_state)

"""
def grid(block_size, centered=False):
    real_block_size = block_size+1
    width = WINDOW_WIDTH // real_block_size
    height = WINDOW_HEIGHT // real_block_size
    offset_x = 0
    offset_y = 0
    if (centered):
        offset_x = (SCREEN.get_width() - real_block_size*width)//2
        offset_y = (SCREEN.get_height() - real_block_size*height)//2

    for x in range(width):
        for y in range(height):
            rect = pygame.Rect(offset_x + x * real_block_size, offset_y + y * real_block_size, block_size, block_size)
            pygame.draw.rect(SCREEN, (200, 200, 200), rect, 1)

def main():
    global SCREEN
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Match-the-Tiles')

    while True:
        grid(32, True)
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        pygame.display.flip()

if __name__ == '__main__': main()
"""