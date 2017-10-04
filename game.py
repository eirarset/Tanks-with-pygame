import pygame, sys
from pygame.locals import *

# Tanks
# By Eirik Aarseth

FPS = 25
WINDOWHEIGHT = 575
WINDOWWITH = 1024
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
    pygame.display.set_caption("Tanks with pygame")

    red_img = pygame.image.load('tank10.png')
    red_tank_img = pygame.transform.scale(red_img, (TANKWITH, TANKHEIGHT))
    blue_img = pygame.image.load('blue-tank.png')
    blue_tank_img = pygame.transform.scale(blue_img, (TANKWITH, TANKHEIGHT))
    bomb_image = pygame.image.load('bomb.png')
    bomb_img = pygame.transform.scale(bomb_image, (BOMBWITH, BOMBHEIGHT))
    explosion_full = pygame.image.load('explosion.png')
    explosion_img = pygame.transform.scale(explosion_full, (EXPLOSIONWITH, EXPLOSIONHEIGHT))
    heart_img = pygame.image.load('heart.png')
    heart = pygame.transform.scale(heart_img, (HEARTHEIGHT, HEARTWITH))
    blue_heart = pygame.transform.flip(heart, True, False)
    arrow_img = pygame.image.load('arrow.png')
    arrow = pygame.transform.scale(arrow_img, (ARROWLENGTH, ARROWWITH))
    background = pygame.image.load('background.png')

    blue_lives  = 5
    red_lives = 5
    red_x = 0
    red_moving = False
    blue_x = WINDOWWITH-TANKWITH
    blue_moving = False
    bomb = False
    explosion = False
    explosionx = 0
    explosiony = 0
    explosioncount = 0
    bombspeed = 0
    direction = ''
    red_turn = True
    bomb_x_speed = 0
    bomb_y_speed = 0


    while True:

        SCREEN.blit(background, (0, 0))


        if red_moving:
            if direction == 'r':
                red_x+=10
                if red_x >  blue_x - TANKWITH:
                    red_x = blue_x - TANKWITH

            elif direction == 'l':
                red_x-=10
                if red_x < 0:
                    red_x = 0

        elif blue_moving:
            if direction == 'r':
                blue_x+=10
                if  blue_x > WINDOWWITH - TANKWITH:
                    blue_x = WINDOWWITH-TANKWITH
            elif direction == 'l':
                blue_x-=10
                if  blue_x < red_x + TANKWITH:
                    blue_x = red_x + TANKWITH


        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == KEYDOWN:
                keys = pygame.key.get_pressed()

                if keys[K_LEFT]:
                    if red_turn:
                        blue_moving = False
                        red_moving = True
                        direction = 'l'
                        red_x -= 1
                    else:
                        red_moving = False
                        blue_moving = True
                        direction = 'l'
                elif keys[K_RIGHT]:
                    if red_turn:
                        blue_moving = False
                        red_moving = True
                        direction = 'r'
                        red_x += 1
                    else:
                        red_moving = False
                        blue_moving = True
                        direction = 'r'
                        blue_x += 1
                elif keys[K_SPACE]:
                    if bomb:
                        continue
                    bomb = True
                    if red_turn:
                        bombx = red_x + 10

                    else:
                        bombx = blue_x
                    bomby = WINDOWHEIGHT * (2 / 3) - TANKHEIGHT

                    rotation = 0
                    rotate_up = True
                    stop = False

                    while True: #Set direction and power
                        SCREEN.blit(background, (0, 0))
                        if red_turn:
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
                        else:
                            if rotate_up:
                                if rotation <= -90:
                                    rotate_up = False
                                else:
                                    rotation -= 2
                            else:
                                if rotation >= 0:
                                    rotate_up = True
                                else:
                                    rotation += 2
                        SCREEN.blit(red_tank_img, (red_x, WINDOWHEIGHT * (2 / 3) - TANKHEIGHT * (2 / 3)))
                        SCREEN.blit(blue_tank_img, (blue_x, WINDOWHEIGHT * (2 / 3) - TANKHEIGHT * (2 / 3)))


                        new_arrow = pygame.transform.rotate(arrow, rotation)
                        new_rect = new_arrow.get_rect()
                        if red_turn:
                            new_rect.bottomleft = (bombx, bomby+30)
                        else:
                            new_rect.bottomright = (bombx, bomby+30)
                        SCREEN.blit(new_arrow, new_rect)

                        for ev in pygame.event.get():
                            if ev.type == QUIT:
                                pygame.quit()
                                sys.exit()
                            elif ev.type == KEYDOWN:
                                keys = pygame.key.get_pressed()
                                if keys[K_SPACE]:
                                    bomb_y_speed = 15 * rotation+1
                                    bomb_x_speed = (90 / rotation) *3
                                    if not red_turn:
                                        bomb_x_speed *= -1
                                    stop = True
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
                            SCREEN.blit(blue_heart, (blue_lives_x, 10))
                            blue_lives_x -= HEARTWITH + 3
                        pygame.display.update()
                        FPSCLOCK.tick(FPS)
                        if stop:
                            break


                    arrow = pygame.transform.rotate(arrow, 180)
                    bombspeed = 18


                    if red_turn:
                        red_turn = False
                    else:
                        red_turn = True
            else:
                red_moving = False
                blue_moving = False


        if explosion:
            explosioncount += 1
            if explosioncount >= FPS/2:
                explosion = False
            else:
                SCREEN.blit(explosion_img, (explosionx-30, explosiony-30))


        if bomb: #If bomb/shot fired
            if bomby > WINDOWHEIGHT * (2 / 3) - 20:
                if bombx > red_x - 30 and bombx < red_x + 30:
                    red_lives -= 1
                if bombx >  blue_x - 30 and bombx < blue_x + 30:
                    blue_lives -= 1
                if blue_lives <= 0 or red_lives <= 0:
                    game_over()
                bomb = False
                explosion = True
                explosionx = bombx
                explosiony = bomby
                explosioncount = 0
            else:
                if not red_turn:
                    bombx += bomb_x_speed
                else:
                    bombx -= bomb_x_speed
                bomby -= (bombspeed - BOMBGRAVITY)
                bombspeed -= 1

            SCREEN.blit(bomb_img, (bombx, bomby))

        #Showes lives remaining
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
            SCREEN.blit(blue_heart, (blue_lives_x, 10))
            blue_lives_x -= HEARTWITH + 3



        SCREEN.blit(red_tank_img, (red_x, WINDOWHEIGHT * (2 / 3) - TANKHEIGHT * (2 / 3)))
        SCREEN.blit(blue_tank_img, (blue_x, WINDOWHEIGHT * (2 / 3) - TANKHEIGHT * (2 / 3)))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def game_over():
    game_over_img = pygame.image.load('GameOver.png')
    game_over = pygame.transform.scale(game_over_img, (WINDOWWITH, int(WINDOWHEIGHT/2)))
    restart_img = pygame.image.load('restartText.png')
    restart_rect = restart_img.get_rect()
    restart_rect.centerx = WINDOWWITH/2
    restart_rect.centery = WINDOWHEIGHT/3*2 
    while True:
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                if(keys[K_r]):
                    main()
        SCREEN.blit(game_over, (0, 0))
        SCREEN.blit(restart_img, restart_rect)
        pygame.display.update()
        FPSCLOCK.tick(FPS)



main()
