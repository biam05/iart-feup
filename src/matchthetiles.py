import pygame
import sys
from pygame.locals import *
from match_the_tiles.logic.reader import get_level
from utils.utils import Coords
from solver import solver

mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Match The Tiles')
WIDTH = HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
click = False


def scrollX(screenSurf, offsetX):
    width, height = screenSurf.get_size()
    copySurf = screenSurf.copy()
    screenSurf.blit(copySurf, (offsetX, 0))
    if offsetX < 0:
        screenSurf.blit(copySurf, (width + offsetX, 0), (0, 0, -offsetX, height))
    else:
        screenSurf.blit(copySurf, (0, 0), (width - offsetX, 0, offsetX, height))


def scrollY(screenSurf, offsetY):
    width, height = screenSurf.get_size()
    copySurf = screenSurf.copy()
    screenSurf.blit(copySurf, (0, offsetY))
    if offsetY < 0:
        screenSurf.blit(copySurf, (0, height + offsetY), (0, 0, width, -offsetY))
    else:
        screenSurf.blit(copySurf, (0, 0), (0, height - offsetY, width, offsetY))


def write(text, x, y, color, size, surface):
    font = pygame.font.SysFont("Arial", size)
    text = font.render(text, True, pygame.Color(color))
    text_rect = text.get_rect(center=(x, y))
    surface.blit(text, text_rect)


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
    elif color == "o":
        return 255, 100, 0
    else:
        return 100, 100, 100


def drawBlock(x, y, color):
    block = pygame.Rect(x, y, 100, 100)
    c = getColor(color)
    pygame.draw.rect(screen, c, block)
    for i in range(4):  # borders
        pygame.draw.rect(screen, (0, 0, 0), (x - i, y - i, 155, 155), 1)


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


def drawButtonLevels():
    buttons = []
    x = 120
    y = 120
    for i in range(7):
        for j in range(6):
            button = pygame.Rect(x, y, 60, 60)
            buttons.append(button)
            x = x + 80
        y = y + 80
        x = 120

    return buttons


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
                click = False
                solverMenu()
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


def solverMenu():
    global click
    running = True
    while running:
        screen.fill((0, 0, 0))
        level = 1
        mx, my = pygame.mouse.get_pos()
        write("Choose a Level (A - Advanced)", WIDTH // 2, 60, (255, 255, 255), 60, screen)
        buttons = drawButtonLevels()
        for button in buttons:
            pygame.draw.rect(screen, (0, 204, 255), button)
            if level > 20:
                write(str(level - 20) + "A", button.x + 30, button.y + 30, (0, 0, 0), 30, screen)
            else:
                write(str(level), button.x + 30, button.y + 30, (0, 0, 0), 30, screen)
            level = level + 1

        for i in range(len(buttons)):
            if buttons[i].collidepoint((mx, my)):
                if click:
                    level = i + 1
                    click = False
                    if level > 20:
                        solverSearchMethod(level - 20, True)
                    else:
                        solverSearchMethod(level, False)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


def play(level, advanced):
    nmoves = 0
    running = True
    finishedGame = False
    next = False
    restart = False
    no_more_levels = False
    game_state = get_level(level, advanced)
    if not game_state:
        no_more_levels = True
    while running:
        screen.fill((0, 0, 0))
        if no_more_levels:
            write("No More Levels", WIDTH // 2, HEIGHT // 2, (255, 255, 255), 60, screen)
        else:
            if advanced:
                write("Level " + level + " Advanced", WIDTH // 2, 60, (255, 255, 255), 60, screen)
            else:
                write("Level " + level, WIDTH // 2, 60, (255, 255, 255), 60, screen)
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
                    ngame_state = game_state
                    if event.key == K_LEFT:
                        ngame_state = game_state.swipe_left()
                    if event.key == K_RIGHT:
                        ngame_state = game_state.swipe_right()
                    if event.key == K_UP:
                        ngame_state = game_state.swipe_up()
                    if event.key == K_DOWN:
                        ngame_state = game_state.swipe_down()
                    if event.key == K_h:
                        gl = game_state.swipe_left()
                        gr = game_state.swipe_right()
                        gu = game_state.swipe_up()
                        gd = game_state.swipe_down()
                        nl = gl.calc_heuristic()
                        nr = gr.calc_heuristic()
                        nu = gu.calc_heuristic()
                        nd = gd.calc_heuristic()
                        better = min(nl, nr, nu, nd)
                        if better == nl:
                            hint("L")
                        elif better == nr:
                            hint("R")
                        elif better == nu:
                            hint("U")
                        elif better == nd:
                            hint("D")
                    if ngame_state != game_state:
                        nmoves = nmoves + 1
                    game_state = ngame_state

        pygame.display.update()
        mainClock.tick(60)
        if restart:
            play(level, advanced)
        if next:
            nextlevel = int(level) + 1
            play(str(nextlevel), advanced)


def hint(direction):
    running = True
    hint = ""
    while running:
        screen.fill((0, 0, 0))

        write("Hint", WIDTH // 2, 60, (255, 255, 255), 60, screen)

        if direction == "R":
            hint = "Swipe Right"
        elif direction == "L":
            hint = "Swipe Left"
        elif direction == "U":
            hint = "Swipe Up"
        elif direction == "D":
            hint = "Swipe Down"

        write(hint, WIDTH // 2, HEIGHT // 2, (255, 255, 255), 60, screen)

        write("Press Esc to go back to the game", WIDTH // 2, 600, (255, 255, 255), 40, screen)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)


def solverSearchMethod(level, advanced):
    global click
    running = True
    while running:
        screen.fill((0, 0, 0))
        mx, my = pygame.mouse.get_pos()
        write("Solver - Search Method", WIDTH // 2, 60, (255, 255, 255), 60, screen)
        if advanced:
            write("Level " + str(level) + " Advanced", WIDTH // 2, 120, (255, 255, 255), 30, screen)
        else:
            write("Level " + str(level), WIDTH // 2, 120, (255, 255, 255), 30, screen)

        button_1 = pygame.Rect(135, 160, 430, 90)
        button_2 = pygame.Rect(135, 260, 430, 90)
        button_3 = pygame.Rect(135, 360, 430, 90)
        button_4 = pygame.Rect(135, 460, 430, 90)
        button_5 = pygame.Rect(135, 560, 430, 90)
        pygame.draw.rect(screen, (0, 204, 255), button_1)
        pygame.draw.rect(screen, (0, 204, 255), button_2)
        pygame.draw.rect(screen, (0, 204, 255), button_3)
        pygame.draw.rect(screen, (0, 204, 255), button_4)
        pygame.draw.rect(screen, (0, 204, 255), button_5)
        write("BFS", WIDTH // 2, 205, (0, 0, 0), 50, screen)
        write("DFS", WIDTH // 2, 305, (0, 0, 0), 50, screen)
        write("Uniform Cost Search", WIDTH // 2, 405, (0, 0, 0), 50, screen)
        write("A*", WIDTH // 2, 505, (0, 0, 0), 50, screen)
        write("Greedy", WIDTH // 2, 605, (0, 0, 0), 50, screen)

        if button_1.collidepoint((mx, my)):
            if click:
                solveLevel(level, advanced, "bfs")
        if button_2.collidepoint((mx, my)):
            if click:
                solveLevel(level, advanced, "dfs")
        if button_3.collidepoint((mx, my)):
            if click:
                solveLevel(level, advanced, "ucs")
        if button_4.collidepoint((mx, my)):
            if click:
                solveLevel(level, advanced, "a-star")
        if button_5.collidepoint((mx, my)):
            if click:
                solveLevel(level, advanced, "greedy")

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


def solveLevel(level, advanced, method):
    title = ""
    data = []
    running = True
    loading = True
    finished = False
    if method == "a-star":
        title = "Solver - A*"
    elif method == "bfs":
        title = "Solver - BFS"
    elif method == "dfs":
        title = "Solver - DFS"
    elif method == "ucs":
        title = "Solver -  UCS"
    elif method == "greedy":
        title = "Solver -  Greedy"
    game_state = get_level(level, advanced)
    while running:
        screen.fill((0, 0, 0))
        write(title, WIDTH // 2, 60, (255, 255, 255), 60, screen)
        if advanced:
            write("Level " + str(level) + " Advanced", WIDTH // 2, 120, (255, 255, 255), 30, screen)
        else:
            write("Level " + str(level), WIDTH // 2, 120, (255, 255, 255), 30, screen)
        if loading:
            write("Loading...", WIDTH // 2, HEIGHT // 2, (255, 255, 255), 60, screen)
            pygame.display.update()
            data = solver(level, advanced, method)
            loading = False
        else:
            drawboard(game_state)
            write("Elapsed Time: " + str(data[1]) + "s    Number of Moves: " + str(data[3]),
                  WIDTH // 2, 575, (255, 255, 255), 20, screen)
            write("Goals: " + " ".join(str(x) for x in data[4]), WIDTH // 2,
                  600, (255, 255, 255), 20, screen)
            write("Blocks Final Positions: " + " ".join(str(x) for x in data[5]), WIDTH // 2,
                  625, (255, 255, 255), 20, screen)
            write("Expanded Nodes: " + str(data[6]), WIDTH // 2,
                  650, (255, 255, 255), 20, screen)
            write("Moves: " + " ".join(str(x) for x in data[2]), WIDTH // 2,
                  675, (255, 255, 255), 20, screen)

        if game_state.is_game_over():
            finished = True

        pressed = pygame.key.get_pressed()
        # handle scrolling
        if pressed[pygame.K_w]:
            scrollY(screen, 2)
        elif pressed[pygame.K_s]:
            scrollY(screen, -2)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if not loading and not finished:
                    if event.key == K_LEFT:
                        game_state = game_state.swipe_left()
                    if event.key == K_RIGHT:
                        game_state = game_state.swipe_right()
                    if event.key == K_UP:
                        game_state = game_state.swipe_up()
                    if event.key == K_DOWN:
                        game_state = game_state.swipe_down()

        pygame.display.update()
        mainClock.tick(60)


main_menu()
