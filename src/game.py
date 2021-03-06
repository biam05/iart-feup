import pygame, sys
from pygame.locals import *

pygame.init()

DISPLAYSURF = pygame.display.set_mode((256, 256), 0, 32)

catImg = pygame.image.load('cat.png')

while True:
    DISPLAYSURF.fill((255, 255, 255))

    DISPLAYSURF.blit(catImg, (0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
