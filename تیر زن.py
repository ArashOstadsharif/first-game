from typing import Counter
import pygame
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_UP, K_x
pygame.init()
screen = pygame.display.set_mode((400,400))
pygame.draw.circle(screen,(200,0,0),(200,380),20,5)
def move(x,a,b,bullets):
    cooldown = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed()
        if keys[K_RIGHT]:
            a = 4
        if keys[pygame.K_LEFT]:
            a = -4
        if keys[K_LEFT] and keys[K_RIGHT]:
            a = 0
        if keys[K_DOWN]:
            b = -4
        if keys[pygame.K_UP]:
            b = 4
        if keys[K_DOWN] and keys[K_UP]:
            b = 0
        if keys[K_x]:
            if cooldown == 0:
                bullets.append(x)
                cooldown = 10
        screen.fill((0,0,0))
        copy = list(x)
        if abs(a) == abs(b):
            a = a/1.5
            b = b / 1.5
        copy[0] += a
        copy[1] -= b
        if copy[1] > 380:
            copy[1] = 380
        if copy[0] < 20:
            copy[0] = 20
        x = tuple(copy)
        pygame.draw.circle(screen,(200,0,0),(x),20,5)
        Counter = 0
        dl = []
        for i in bullets:
            pygame.draw.circle(screen,(0,200,0),(i),5,5)
            copy = list(bullets[Counter])
            copy[1] -= 8
            if copy[1] == 0:
                dl.append(Counter)
            bullets[Counter] = tuple(copy)
            Counter += 1
        dl.reverse()
        for i in dl:
            bullets.pop(i)
        pygame.display.update()
        a = 0
        b = 0
        if cooldown > 0:
          cooldown -= 1
        pygame.time.wait(50)
x=(200,380)
move(x,0,0,[])