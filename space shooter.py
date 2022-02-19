
from typing import Counter
import pygame
from pygame import event
from pygame import key
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_UP, K_s, K_x
bg = pygame.image.load("bg.JPG")
class bullets:
    all = []
    def __init__(self,ob):
        self.x = ob.x +(ob.image.get_width()//2)
        self.y = ob.y
        self.facing = ob.facing
class p_bullet(bullets):
    def __init__(self, ob):
        super().__init__(ob)
        self.damage = 1
        self.image = pygame.image.load("b_p.PNG")
        self.x -= self.image.get_width()//2
        self.vel = 8
        self.cooldown = 8
        self.all.append(self)

class player:
    def __init__(self):
        self.image = pygame.image.load("ss.PNG")
        self.x = 250
        self.y = 250
        self.x_midle = self.image.get_width()//2 + self.x
        self.y_midle = self.image.get_height()//2 + self.y
        self.vel = 6
        self.persentage = 0.6
        self.hitbox_h_w = [85,65] 
        self.hitbox = (self.x,self.y,self.image.get_width(),self.image.get_height())
        self.showhitbox = False
        self.facing = 1
    def draw_hitbox(self):
        pygame.draw.rect(screen,(255,0,0),self.hitbox,1)
class enenmy:
    def __init__(self):
        self.image = pygame.image.load('boss.PNG')
        self.x = screen.get_width()//2 - self.image.get_width()//2
        self.y = -40
        self.x_midle = self.image.get_width()//2 + self.x
        self.y_midle = self.image.get_height()//2 + self.y
        self.hitbox = (self.x,self.y,self.image.get_width(),self.image.get_height())
        self.facing = 2
        self.vel = 6
        self.health = 100
    def draw_hitbox(self):
        pygame.draw.rect(screen,(255,0,0),self.hitbox,1)
def draw ():
    p.hitbox = ((p.x+5,p.y+5,p.hitbox_h_w[0],p.hitbox_h_w[1]))
    e.hitbox = (e.x,e.y,e.image.get_width(),e.image.get_height())
    screen.blit(bg,(0,0))
    if p.showhitbox:
        p.draw_hitbox()
        e.draw_hitbox()
    if e.x_midle > p.x_midle:
        e.x_midle -= e.vel
        e.x -= e.vel
    elif e.x_midle < p.x_midle:
        e.x_midle += e.vel
        e.x += e.vel
    for bullet in bullets.all:
        if bullet.facing > 0:
            if bullet.facing == 2:
                bullet.y += bullet.vel
            else:
                bullet.y -=bullet.vel
        else:
            if bullet.facing == -2:
                bullet.x += bullet.vel
            else:
                bullet.x -=bullet.velx
        screen.blit(bullet.image,(bullet.x,bullet.y))
        if bullet.x == 0 or bullet.x >(screen.get_width()) or bullet.y < 0 or bullet.y>screen.get_height():
            del(bullet)
    if e.x_midle > p.x_midle:
        if abs(e.x_midle) - abs(p.x_midle) < e.vel:
            e.x_midle = p.x_midle
            e.x = e.x_midle - e.image.get_width()//2
    screen.blit(e.image,(e.x,e.y))
    screen.blit(p.image ,(p.x,p.y))
    pygame.display.update()

pygame.init()
screen = pygame.display.set_mode((500,500))
run = True
p= player()
e = enenmy()
cooldownsh = 0
cooldownb = 0
while run:
    x = 0
    y = 0
    pygame.time.wait(1000//30)
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[K_s] and cooldownsh == 0:
        if p.showhitbox:
            p.showhitbox = False
        else:
            p.showhitbox = True
        cooldownsh = 6
    if keys[K_DOWN] and p.y+p.vel < screen.get_height()-74:
        y += p.vel
    if keys[K_UP] and p.y-p.vel > 0:
        y -= p.vel
    if keys[K_RIGHT] and p.x+p.vel < screen.get_width()-93:
        x += p.vel
    if keys[K_LEFT] and p.x-p.vel > 0:
        x -= p.vel
    if keys[K_x] and cooldownb == 0:
        p_bullet(p)
        cooldownb = bullets.all[-1].cooldown
    if abs(x)+abs(y) == p.vel*2:
        x *= p.persentage
        y *= p.persentage
    p.x += x
    p.x_midle += x
    p.y += y
    p.y_midle += y
    draw()
    if cooldownsh > 0:
        cooldownsh -= 1
    if cooldownb > 0:
        cooldownb -= 1
pygame.quit()