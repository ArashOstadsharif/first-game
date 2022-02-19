import pygame
from pygame.constants import K_LEFT, K_RIGHT, K_SPACE, K_UP
pygame.init()
screen = pygame.display.set_mode((400,400))
pygame.draw.circle(screen,(200,0,0),(200,380),20,5)
def move(x,a,jumping,grounded):
    r = 1
    l = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed()
        if keys[K_RIGHT]:
            if keys[pygame.K_SPACE] and grounded == 1:
                r = 2
            a = 4*r
            l = 1
        if keys[pygame.K_LEFT]:
            if keys[pygame.K_SPACE] and grounded == 1:
                l = 2
            a = -4*l
            r = 1
        if keys[K_LEFT] and keys[K_RIGHT]:
            a = 0
        if keys[pygame.K_SPACE]:
            if grounded == 1:
                grounded = 2
                jumping = 12 
        screen.fill((0,0,0))
        copy = list(x)
        copy[0] += a/(grounded)
        copy[1] -= jumping
        if copy[1] > 380:
            copy[1] = 380
            jumping = 0
            grounded = 1
            l = 1
            r = 1
        x = tuple(copy)
        pygame.draw.circle(screen,(200,0,0),(x),20,5)
        if jumping > 0.5:
            jumping -= 0.5
        if jumping == 0.5:
            jumping = -1
        if jumping < 0:
            jumping -= 1.5
        if jumping == 10:
            keys = pygame.key.get_pressed()
            if not keys[K_SPACE]:
                jumping = 1
        if jumping == 6:
            keys = pygame.key.get_pressed()
            if not keys[K_SPACE]:
                jumping = 0.5

        pygame.display.update()
        a = 0
        pygame.time.wait(50)
x=(200,380)
grounded = 1
jumping = 0
move(x,0,0,1)