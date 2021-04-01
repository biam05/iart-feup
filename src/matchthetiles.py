import pygame
import sys
from pygame.locals import *
from match_the_tiles.logic.reader import get_level
from utils.utils import Coords

mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Match The Tiles')
WIDTH = HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
click = False


def write(text, x, y, color, size, screen):
    font = pygame.font.SysFont("Arial", size)
    text = font.render(text, True, pygame.Color(color))
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)


def getColor(color):
    if color == "g":
        return 0, 255, 0
    elif color == "w":
        return 255, 255, 255
    elif color == "b":
        return 0, 0, 255
    elif color == "r":
        return 255, 0, 0
    elif color == "y":
        return 255, 255, 0
    elif color == "p":
        return 255, 0, 127
    else:
        return 100, 100, 100


def drawBlock(x, y, color):
    block = pygame.Rect(x, y, 100, 100)
    c = getColor(color)
    pygame.draw.rect(screen, c, block)
    for i in range(4): # borders
        pygame.draw.rect(screen, (0,0,0), (x-i,y-i,155,155), 1)


def drawGoal(x, y, color):
    c = getColor(color)
    pygame.draw.circle(screen, c, (x, y), 25, 70)


def drawboard(gamestate):
    matrix = gamestate.getGameStateMatrix()
    d = gamestate.getGameStateDictionary()
    x = 150
    y = 150
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            drawBlock(x, y, 'w')
            coord = Coords(i, j)
            chars = d[coord]
            for char in chars:
                if char.lower() == char:
                    drawBlock(x, y, char.lower())
                elif char.upper() == char:
                    drawGoal(x + 50, y + 50, char.lower())
            x = x + 100
        y = y + 100
        x = 150

def main_menu():
    global click
    while True:
        screen.fill((0, 0, 0))
        write("MATCH THE TILES", WIDTH // 2, 100, (255, 255, 255), 80, screen)
        # Mouse positions
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(150, 200, 400, 100)  # button to solver
        button_2 = pygame.Rect(150, 350, 400, 100)  # button to play normal
        button_3 = pygame.Rect(150, 500, 400, 100)  # button to play advanced
        pygame.draw.rect(screen, (0, 204, 255), button_1)
        pygame.draw.rect(screen, (0, 204, 255), button_2)
        pygame.draw.rect(screen, (0, 204, 255), button_3)
        write("SOLVER", WIDTH // 2, 250, (0, 0, 0), 50, screen)
        write("PLAY NORMAL", WIDTH // 2, 400, (0, 0, 0), 50, screen)
        write("PLAY ADVANCED", WIDTH // 2, 550, (0, 0, 0), 50, screen)

        if button_1.collidepoint((mx, my)):
            if click:
                solver()
        if button_2.collidepoint((mx, my)):
            if click:
                play("1", False)
        if button_3.collidepoint((mx, my)):
            if click:
                play("1", True)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


def solver():
    running = True
    while running:
        screen.fill((0, 0, 0))

        write("SOLVER", WIDTH // 2, HEIGHT // 2 - 100, (255, 255, 255), 50, screen)
        write("NOT IMPLEMENTED YET", WIDTH // 2, HEIGHT // 2 + 50, (255, 255, 255), 50, screen)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)


def play(level, advanced):
    nmoves = 0
    running = True
    finishedGame = False
    next = False
    restart = False
    game_state = get_level(level, advanced)
    while running:
        screen.fill((0, 0, 0))
        if advanced:
            write("Level " + level + " Advanced", WIDTH // 2, 60, (255, 255, 255), 60, screen)
        else:
            write("Level " + level + " Advanced", WIDTH // 2, 60, (255, 255, 255), 60, screen)
        write("Number of Moves: " + str(nmoves), WIDTH // 2, 120, (255, 255, 255), 30, screen)
        drawboard(game_state)
        if game_state.is_game_over():
            finishedGame = True
        if finishedGame:
            if advanced:
                write("Finished level " + level + " Advanced!", WIDTH // 2, 600, (255, 255, 255), 50, screen)
            else:
                write("Finished level " + level + "!", WIDTH // 2, 600, (255, 255, 255), 50, screen)
            write("Press Y to Play next Level or R to Restart", WIDTH // 2, 660, (255, 255, 255), 30, screen)
        else:
            write("Move: Arrow Keys", WIDTH // 2, 600, (255, 255, 255), 40, screen)
            write("Restart: R    Hint: H", WIDTH // 2, 650, (255, 255, 255), 30, screen)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_r:
                    running = False
                    restart = True
                if finishedGame:
                    if event.key == K_y:
                        running = False
                        next = True
                else:
                    if event.key == K_LEFT:
                        game_state = game_state.swipe_left()
                        nmoves = nmoves + 1
                    if event.key == K_RIGHT:
                        game_state = game_state.swipe_right()
                        nmoves = nmoves + 1
                    if event.key == K_UP:
                        game_state = game_state.swipe_up()
                        nmoves = nmoves + 1
                    if event.key == K_DOWN:
                        game_state = game_state.swipe_down()
                        nmoves = nmoves + 1
                    if event.key == K_h:
                        print("Not Implemented Yet (Hint)")

        pygame.display.update()
        mainClock.tick(60)
        if restart:
            play(level, advanced)
        if next:
            nextlevel = int(level) + 1
            play(str(nextlevel), advanced)


main_menu()
