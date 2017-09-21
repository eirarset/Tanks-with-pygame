# Tanks
# By Eirik Årseth

import pygame, sys
from pygame.locals import *

FPS = 30
WINDOWHEIGHT = 480
WINDOWWITH = 640
TANKWITH = 40
TANKHEIGHT = 40
BOMBWITH = 15
BOMBHEIGHT = 15
BOMBGRAVITY = 5
EXPLOSIONWITH = 100
EXPLOSIONHEIGHT = 100
HEARTHEIGHT = 50
HEARTWITH = 50
ARROWLENGTH = 200
ARROWWITH = 50



#COLORS
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE = (  0,   0, 255)
SKYBLUE = (150  , 200, 255)
BROWN_EARTH = (205,133,63)

red_lives = 5
blue_lives = 5

def main():

    global SCREEN, red_lives, blue_lives, FPSCLOCK

    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOWWITH, WINDOWHEIGHT), 0, 32)
    FPSCLOCK = pygame.time.Clock()
    blue_lives  = 5
    red_lives = 5
    pygame.display.set_caption("Tanks with pygame")




    redImg = pygame.image.load('tank10.png')
    redtankImg = pygame.transform.scale(redImg, (TANKWITH, TANKHEIGHT))
    blueImg = pygame.image.load('blue-tank.png')
    blueTankImg = pygame.transform.scale(blueImg, (TANKWITH, TANKHEIGHT))
    bombImage = pygame.image.load('bomb.png')
    bombimg = pygame.transform.scale(bombImage, (BOMBWITH, BOMBHEIGHT))
    explosionfull = pygame.image.load('explosion.png')
    explosionimg = pygame.transform.scale(explosionfull, (EXPLOSIONWITH, EXPLOSIONHEIGHT))
    heartImg = pygame.image.load('heart.png')
    heart = pygame.transform.scale(heartImg, (HEARTHEIGHT, HEARTWITH))
    arrowImg = pygame.image.load('arrow.png')
    arrow = pygame.transform.scale(arrowImg, (ARROWLENGTH, ARROWWITH))


    redX = 0
    redMoving = False
    blueX = WINDOWWITH-TANKWITH
    blueMoving = False
    bomb = False
    explosion = False
    explosionx = 0
    explosiony = 0
    explosioncount = 0
    bombspeed = 0
    direction = ''
    redTurn = True
    bomb_x_speed = 0
    bomb_y_speed = 0


    while True:

        SCREEN.fill(SKYBLUE)
        pygame.draw.rect(SCREEN, BROWN_EARTH, (0, (WINDOWHEIGHT / 3) * 2, WINDOWWITH, WINDOWHEIGHT / 3))



        if redMoving:
            if direction == 'r':
                redX+=10
                if redX > blueX - TANKWITH:
                    redX = blueX - TANKWITH

            elif direction == 'l':
                redX-=10
                if redX < 0:
                    redX = 0

        elif blueMoving:
            if direction == 'r':
                blueX+=10
                if blueX > WINDOWWITH - TANKWITH:
                    blueX = WINDOWWITH-TANKWITH
            elif direction == 'l':
                blueX-=10
                if blueX < redX + TANKWITH:
                    blueX = redX + TANKWITH


        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == KEYDOWN:
                keys = pygame.key.get_pressed()

                if keys[K_LEFT]:
                    if redTurn:
                        blueMoving = False
                        redMoving = True
                        direction = 'l'
                        redX -= 1
                    else:
                        redMoving = False
                        blueMoving = True
                        direction = 'l'
                elif keys[K_RIGHT]:
                    if redTurn:
                        blueMoving = False
                        redMoving = True
                        direction = 'r'
                        redX += 1
                    else:
                        redMoving = False
                        blueMoving = True
                        direction = 'r'
                        blueX += 1
                elif keys[K_SPACE]:
                    if bomb:
                        continue
                    bomb = True
                    if redTurn:
                        bombx = redX + 10
                    else:
                        bombx = blueX
                    bomby = WINDOWHEIGHT * (2 / 3) - TANKHEIGHT

                    rotation = 0
                    rotate_up = True
                    stop = False

                    while True: #Set direction
                        SCREEN.fill(SKYBLUE)
                        pygame.draw.rect(SCREEN, BROWN_EARTH, (0, (WINDOWHEIGHT / 3) * 2, WINDOWWITH, WINDOWHEIGHT / 3))
                        if rotate_up:
                            if rotation >= 90:
                                rotate_up = False
                            else:
                                rotation += 2
                        else:
                            if rotation <= 0:
                                rotate_up = True
                            else:
                                rotation -= 2
                        SCREEN.blit(redtankImg, (redX, WINDOWHEIGHT * (2 / 3) - TANKHEIGHT * (2 / 3)))
                        SCREEN.blit(blueTankImg, (blueX, WINDOWHEIGHT * (2 / 3) - TANKHEIGHT * (2 / 3)))

                        new_arrow = pygame.transform.rotate(arrow, rotation)
                        new_rect = new_arrow.get_rect()
                        new_rect.bottomleft = (bombx, bomby+30)
                        SCREEN.blit(new_arrow, new_rect)

                        for ev in pygame.event.get():
                            if ev.type == QUIT:
                                pygame.quit()
                                sys.exit()
                            elif ev.type == KEYDOWN:
                                keys = pygame.key.get_pressed()
                                if keys[K_SPACE]:
                                    bomb_y_speed = 10 * rotation+1
                                    bomb_x_speed = (90 / rotation) *2
                                    stop = True
                        pygame.display.update()
                        FPSCLOCK.tick(FPS)
                        if stop:
                            break







                    bombspeed = 18
                    if redTurn:
                        redTurn = False
                    else:
                        redTurn = True
            else:
                redMoving = False
                blueMoving = False

        if explosion:
            explosioncount += 1

            if explosioncount >= FPS/2:
                explosion = False
            else:
                SCREEN.blit(explosionimg, (explosionx-30, explosiony-30))
        if bomb:
            if bomby > WINDOWHEIGHT * (2 / 3) - 20:
                if bombx > redX - 10 and bombx < redX + 10:
                    red_lives -= 1
                if bombx > blueX - 40 and bombx < blueX + 40:
                    blue_lives -= 1
                if blue_lives <= 0 or red_lives <= 0:
                    game_over()
                bomb = False
                explosion = True
                explosionx = bombx
                explosiony = bomby
                explosioncount = 0
            else:
                if not redTurn:
                    bombx += bomb_x_speed
                else:
                    bombx -= bomb_x_speed
                bomby -= (bombspeed - BOMBGRAVITY)
                bombspeed -= 1

            SCREEN.blit(bombimg, (bombx, bomby))


        red_lives_show = red_lives
        red_lives_x = 10
        while red_lives_show > 0:
            red_lives_show -= 1
            SCREEN.blit(heart, (red_lives_x, 10))
            red_lives_x += HEARTWITH + 3
        blue_lives_show = blue_lives
        blue_lives_x = WINDOWWITH - HEARTWITH - 10
        while blue_lives_show > 0:
            blue_lives_show -= 1
            SCREEN.blit(heart, (blue_lives_x, 10))
            blue_lives_x -= HEARTWITH + 3



        SCREEN.blit(redtankImg, (redX, WINDOWHEIGHT * (2 / 3) - TANKHEIGHT * (2 / 3)))
        SCREEN.blit(blueTankImg, (blueX, WINDOWHEIGHT * (2 / 3) - TANKHEIGHT * (2 / 3)))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def game_over():
    game_over_img = pygame.image.load('GameOver.png')
    game_over = pygame.transform.scale(game_over_img, (WINDOWWITH, int(WINDOWHEIGHT/2)))
    while True:
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit()
                sys.exit()
        SCREEN.blit(game_over, (0, 0))
        pygame.display.update()
        FPSCLOCK.tick(FPS)



main()







