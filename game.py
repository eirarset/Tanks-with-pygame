import pygame, sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((500, 400), 0 , 32)

#Farger
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE = (  0,   0, 255)
HIMMELBLAA = (204  , 229, 255)
JORDBRUN = (205,133,63)

XKANT = 500
YKANT = 400



FPS = 25
fpsCLock = pygame.time.Clock()

Img = pygame.image.load('tank10.png')
TANKBREDDE = 40
TANKHOYDE = 40
tankImg = pygame.transform.scale(Img, (TANKBREDDE, TANKHOYDE))
x = 0
retning = 'r'


while True:

    screen.fill(HIMMELBLAA)
    pygame.draw.rect(screen, JORDBRUN, (0, 250, 500, 200))

    if retning == 'r':
        x += 3
        if x >= XKANT-TANKBREDDE:
            retning = 'l'
            tankImg = pygame.transform.flip(tankImg, True, False)
    elif retning == 'l':
        x-= 3
        if x <= 0:
            retning = 'r'
            tankImg = pygame.transform.flip(tankImg, True, False)

    screen.blit(tankImg, (x, 220))

    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
            sys.exit()


    pygame.display.update()
    fpsCLock.tick(FPS)