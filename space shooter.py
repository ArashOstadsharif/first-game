from typing import Counter
import pygame
from pygame import event
from pygame import key
from pygame import mixer
from pygame.constants import K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE, K_UP, K_f, K_m, K_s, K_x
import copy
pygame.init()
w = 1000
h = 1000
bs = pygame.image.load("black_screen.PNG")
bg = pygame.image.load("bg.PNG")
p_button = pygame.image.load("p_button.PNG")
q_button = pygame.image.load("q_button.PNG")
allhitbox = []
allss = []
hover = pygame.mixer.Sound("hover.mp3")
click = pygame.mixer.Sound("click.mp3")
bgmusic = mixer.music.load('bg_music.OGG')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
muted = True
class bullets:
    all = []
    def __init__(self,ob):
        self.rect = None
        self.x = ob.x +(ob.image.get_width()//2)
        self.y = ob.y 
        self.facing = ob.facing
class p_bullet(bullets):
    def __init__(self, ob):
        super().__init__(ob)
        self.damage = 2
        self.image = pygame.image.load("b_p.PNG")
        self.sound = pygame.mixer.Sound('b_p_s.wav')
        self.damages = pygame.mixer.Sound('b_p_d.mp3')
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x,self.y)
        self.damages.set_volume(0.5)
        self.x -= self.image.get_width()//2
        self.y -= self.image.get_height()+1
        self.vel = 14
        self.cooldown = 6
        self.all.append(self)
class b_bullet(bullets):
    def __init__(self, ob):
        super().__init__(ob)
        self.damage = 3.34
        self.image = pygame.image.load("b_b.PNG")
        self.sound = pygame.mixer.Sound('b_b_s.wav')
        self.damages = pygame.mixer.Sound('b_b_d.mp3')
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x,self.y)
        self.x -= self.image.get_width()//2
        self.y += ob.image.get_height()+1
        self.vel = 8
        self.cooldown = 18 
        self.all.append(self)

class player:
    def __init__(self):
        self.image = pygame.image.load("ss.PNG")
        self.x = 250
        self.y = 250
        self.x_midle = self.image.get_width()/2 + self.x
        self.y_midle = self.image.get_height()/2 + self.y
        self.vel = 10
        self.persentage = 0.6
        self.hitbox_h_w = [85,65] 
        self.hitbox = (self.x,self.y,self.image.get_width(),self.image.get_height())
        self.showhitbox = False
        self.facing = [0,-1]
        self.shield = shield(self)
        self.health = 10
        self.maxhealth = 10
        self.healthbarcolor = (0,255,0)
        allhitbox.append([self.hitbox,self])
        allss.append(self)
    def draw_hitbox(self):
        pygame.draw.rect(screen,(255,0,0),self.hitbox,1)
class shield:
    def __init__(self,o):
        self.image = pygame.image.load('shield.PNG')
        self.image.set_alpha(100)
        self.x = o.x
        self.y = o.y-90
        self.time = 300
        self.enable = False
class enenmy:
    def __init__(self):
        self.image = pygame.image.load('boss.PNG')
        self.x = screen.get_width()//2 - self.image.get_width()//2
        self.y = -40
        self.x_midle = self.image.get_width()/2 + self.x
        self.y_midle = self.image.get_height()/2 + self.y
        self.hitbox = (self.x,self.y,self.image.get_width(),self.image.get_height())
        self.facing = [0,1]
        self.vel = 6
        self.folow = False
        self.health = 100
        self.maxhealth = 100
        self.healthbarcolor = (255,0,0)
        self.shield = shield(self)
        allhitbox.append([self.hitbox,self])
        allss.append(self)
    def draw_hitbox(self):
        pygame.draw.rect(screen,(255,0,0),self.hitbox,1)
class buttons():
    def __init__(self,x,y,image,scale):
        self.scale = scale
        image = pygame.transform.scale(image,(image.get_width()*scale,image.get_height()*scale))
        self.image = image
        self.himage = pygame.transform.scale(self.image,((self.image.get_width()+10),(self.image.get_height())+10))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.hovered = False
    def draw(self,alpha):
        self.image.set_alpha(alpha)
        p = pygame.mouse.get_pos()
        if self.rect.collidepoint(p):
            if not(self.hovered):
                hover.play()
            self.hovered = True
            if pygame.mouse.get_pressed()[0] or self.clicked:
                self.clicked = True
                screen.blit(self.image,(self.rect.x,self.rect.y))
            else:
                screen.blit(self.himage,(self.rect.x,self.rect.y))
        else:
            self.hovered = False
            screen.blit(self.image,(self.rect.x,self.rect.y))
def reset(pa,q):
    for i in bullets.all:
        del(i)
    bullets.all = []
    for i in allss:
        allss.pop(allss.index(i))
        del(i)
    for i in allhitbox:
        allhitbox.pop(allhitbox.index(i))
        del(i)
    del(pa)
    del(q)
    global p
    p = player()
    global e
    e = enenmy()
    global cooldownsh
    global cooldownb
    global cooldownbb
    cooldownsh = 0
    cooldownb = 0
    cooldownbb = 0
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
def button_animation(pa,q,alpha):
    while alpha > 0:
        pygame.time.wait(1)
        screen.fill((0,0,0))
        pa.draw(alpha)
        q.draw(alpha)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        alpha -= 1
    return True
def button():
    scale = 0.5
    pa = buttons(w//2-(p_button.get_width()*scale)//2,h//2-((p_button.get_height()//2*scale))-10,p_button,scale)
    q = buttons(w//2-(q_button.get_width()*scale)//2,h//2+((q_button.get_height()//2*scale))+10,q_button,scale)
    alpha = 0
    while True:
        pygame.time.wait(2)
        screen.fill((0,0,0) )
        pa.draw(alpha)
        q.draw(alpha)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        if q.clicked:
            click.play()
            button_animation(pa,q,alpha)
            return False
        if pa.clicked:
            reset(pa,q)
            click.play()
            a = button_animation(pa,q,alpha)
            if not(a):
                return False
            return True
        if alpha < 200:
            alpha += 1
def loose():
    pygame.mixer.music.stop()
    for i in range (50):
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                return False
        bs.set_alpha(i)
        screen.blit(bs,(0,0))
        pygame.display.update()
    font = pygame.font.SysFont('comicsans',100,True)
    text = font.render("You Lost!",1,(255,0,0))
    alpha = 0
    if not muted:
        pygame.mixer.Sound('lose.mp3').play()
    while alpha < 200:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                return False 
        screen.fill((0,0,0))
        text.set_alpha(alpha)
        screen.blit(text,((screen.get_width()//2)-(text.get_width()//2),(screen.get_height()//2)-(text.get_height()//2)))
        pygame.display.update()
        alpha += 1
        pygame.time.wait(1)
    for i in range (100):
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                return False
        pygame.time.wait(1)
    while alpha > 0:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                return False
        screen.fill((0,0,0))
        text.set_alpha(alpha)
        screen.blit(text,((screen.get_width()//2)-(text.get_width()//2),(screen.get_height()//2)-(text.get_height()//2)))
        pygame.display.update()
        alpha -= 1
        pygame.time.wait(1)

    return button()
def win():
    if not muted:
        pygame.mixer.Sound('win.wav').play()
    pygame.mixer.music.stop()
    for i in range (50):
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                return False
        bs.set_alpha(i)
        screen.blit(bs,(0,0))
        pygame.display.update()
    font = pygame.font.SysFont('comicsans',100,True)
    text = font.render("You won!",1,(0,255,0))
    alpha = 0
    while alpha < 200:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                return False 
        screen.fill((0,0,0))
        text.set_alpha(alpha)
        screen.blit(text,((screen.get_width()//2)-(text.get_width()//2),(screen.get_height()//2)-(text.get_height()//2)))
        pygame.display.update()
        alpha += 1
        pygame.time.wait(11)
    for i in range (100):
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                return False
        pygame.time.wait(11)
    while alpha > 0:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                return False
        screen.fill((0,0,0))
        text.set_alpha(alpha)
        screen.blit(text,((screen.get_width()//2)-(text.get_width()//2),(screen.get_height()//2)-(text.get_height()//2)))
        pygame.display.update()
        alpha -= 1
        pygame.time.wait(11)
    return button()
def draw ():
    screen.fill((0,0,0))
    screen.blit(bg,(0,0))
    if p.showhitbox:
        p.draw_hitbox()
        e.draw_hitbox()
    if e.health > 0:
        pygame.draw.line(screen,e.healthbarcolor,(0,0),((e.maxhealth*10)-(e.maxhealth-e.health)*10,0),20)
    if p.health > 0:
        pygame.draw.line(screen,p.healthbarcolor,(0,20),((p.maxhealth*10)-(p.maxhealth-p.health)*10,20),20)
    for bullet in bullets.all:
        screen.blit(bullet.image,(bullet.x,bullet.y))
    screen.blit(e.image,(e.x,e.y))
    screen.blit(p.image ,(p.x,p.y))
    if e.shield.enable:
        screen.blit(e.shield.image,(e.shield.x,e.shield.y))
    pygame.display.update()
def inside(hitbox,bullet):
     hitbox = list(hitbox[0])
     bullet = [bullet.x,bullet.y,bullet.image.get_height(),bullet.image.get_height()]
     if hitbox[2] < bullet[2]:
        x = copy(bullet)
        bullet[0],bullet[2] = hitbox[0],bullet[2]
        hitbox[0],hitbox[2] = x[0],x[2]
     if hitbox[3] < bullet[3]:
        x = copy(bullet)
        bullet[1],bullet[3] = hitbox[1],bullet[3]
        hitbox[1],hitbox[3] = x[1],x[3]
     if bullet[0] <= (hitbox[0] + hitbox[2]) and bullet[0]+bullet[2] >= hitbox[0] :
          if bullet[1] <= (hitbox[1] + hitbox[3]) and bullet[1]+bullet[3] >= hitbox[1] :
             return True
screen = pygame.display.set_mode((w,h))
run = True
p= player()
e = enenmy()
cooldownsh = 0
cooldownb = 0
cooldownbb = 0
pygame.display.set_caption('space shooter')
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
    if keys[K_ESCAPE] and cooldownsh == 0:
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    paused = False
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        paused = False
        cooldownsh = 6
    if keys[K_m] and cooldownsh == 0:
        if muted:
            muted = False
        else:
            muted = True
        cooldownsh = 6
    if keys[K_DOWN] :
        if p.y+p.vel < screen.get_height()-p.image.get_height():
           y += p.vel
        else:
            p.y = screen.get_height() - p.image.get_height()
            p.y_midle = screen.get_height() - p.image.get_height()/2
    if keys[K_UP] :
        if  p.y-p.vel > e.y + e.image.get_height():
            y -= p.vel
        else:
            p.y = e.y + e.image.get_height()
            p.y_midle = (e.y + e.image.get_height())+p.image.get_height()/2
    if keys[K_RIGHT] :
        if p.x+p.vel < screen.get_width()-p.image.get_width():
            x += p.vel
        else:
            p.x = screen.get_width() - p.image.get_width()
            p.x_midle = screen.get_width() - p.image.get_width()/2
    if keys[K_LEFT] :
        if p.x-p.vel > 0:
            x -= p.vel
        else:
            p.x = 0
            p.x_midle = p.image.get_width()/2
    if keys[K_x] and cooldownb == 0:
        p_bullet(p)
        cooldownb = bullets.all[-1].cooldown
        if not(muted):
            bullets.all[-1].sound.play()
    if abs(x)+abs(y) == p.vel*2:
        x *= p.persentage
        y *= p.persentage
    p.x += x
    p.x_midle += x
    p.y += y
    p.y_midle += y
    for bullet in bullets.all:
        bullet.x += bullet.facing[0] * bullet.vel
        bullet.y += bullet.facing[1] * bullet.vel
        bullet.rect.topleft = (x,y)
        index = bullets.all.index(bullet)
        if bullet.x == 0 or bullet.x >(screen.get_width()) or bullet.y < 0 or bullet.y>screen.get_height():
            del(bullet)
            bullets.all.pop(index)
        else:
            for hitbox in allhitbox:
                if inside(hitbox,bullet):
                    if not (hitbox[1].shield.enable):
                        hitbox[1].health -= bullet.damage
                    if not muted:
                        bullet.damages.play()
                    del(bullet)
                    bullets.all.pop(index)
                    break
    if e.folow:
        if (abs(e.x_midle - p.x_midle) < e.vel*p.persentage)  and (((not(keys[K_RIGHT or K_LEFT] or (keys[K_LEFT] and keys[K_RIGHT]))))):
            e.x_midle = p.x_midle
            e.x = e.x_midle - e.image.get_width()/2
        elif e.x_midle > p.x_midle:
            e.x_midle -= e.vel
            e.x -= e.vel
        elif e.x_midle < p.x_midle:
            e.x_midle += e.vel
            e.x += e.vel     
    p.hitbox = ((p.x+5,p.y+5,p.hitbox_h_w[0],p.hitbox_h_w[1]))
    e.hitbox = (e.x,e.y,e.image.get_width(),e.image.get_height())
    e.shield.x = e.x
    e.shield.y = e.y - 90
    e.shield.hitbox = e.hitbox
    x = (p.x_midle - e.x_midle)
    y = (p.y - (e.y+e.image.get_height()))
    xn = 1
    yn = 1
    if x != abs(x):
        xn = -1
        x = abs(x)
    if y != abs(y):
        yn = -1
        y = abs(y)
    e.facing = [x/(x+y) *xn,y/(x+y)*yn]
    if cooldownbb == 0:
        b_bullet(e)
        if not muted:
            bullets.all[-1].sound.play()
        cooldownbb = bullets.all[-1].cooldown
    draw()
    if cooldownsh > 0:
        cooldownsh -= 1
    if cooldownb > 0:
        cooldownb -= 1
    if cooldownbb > 0:
        cooldownbb -= 1
    e.shield.time -= 1
    if e.shield.time == 0:
        e.folow = True
        e.shield.enable = True
    if e.shield.time == -300:
        e.folow = False
        e.shield.enable = False
        e.shield.time = 300
    allhitbox = [[p.hitbox,p],[e.hitbox,e]]
    if e.health <= 0:
        run = win()
    if p.health <= 0:
        run = loose()
    if muted:
        pygame.mixer.music.set_volume(0)
    else:
        pygame.mixer.music.set_volume(0.5)
pygame.quit()