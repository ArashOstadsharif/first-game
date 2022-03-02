from cmath import rect
from queue import Empty
from re import T
from tokenize import Triple
from typing import Counter
import pygame
from pygame import K_e, K_h, K_n, event
from pygame import key
from pygame import mixer
from pygame.constants import K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE, K_UP, K_f, K_m, K_p, K_q, K_s, K_x, K_z
import copy
pygame.init()
w = 1920
h = 1000
bs = pygame.image.load("black_screen.PNG")
bg = pygame.image.load("bg.PNG")
p_button = pygame.image.load("p_button.PNG")
q_button = pygame.image.load("q_button.PNG")
e_button = pygame.image.load("e_button.PNG")
m_button = pygame.image.load("m_button.PNG")
h_button = pygame.image.load("h_button.PNG")
s_loose = pygame.mixer.Sound('lose.mp3')
s_win = pygame.mixer.Sound('win.wav')
allhitbox = []
allss = []
hover = pygame.mixer.Sound("hover.mp3")
click = pygame.mixer.Sound("click.mp3")
bgmusic = mixer.music.load('bg_music.OGG')
pygame.mixer.music.set_volume(0.0)
pygame.mixer.music.play(-1)
class bullets:
    all = []
    def __init__(self,ob):
        self.ss = ob
        self.rect = None
        self.x = ob.x +(ob.image.get_width()//2)
        self.y = ob.y 
        self.facing = ob.facing
class p_bullet(bullets):
    def __init__(self, ob):
        super().__init__(ob)
        self.damage = 3
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
        self.y += ob.image.get_height()
        self.vel = 8
        self.cooldown = 18 
        self.all.append(self)

class player:
    def __init__(self):
        self.image = pygame.image.load("ss.PNG")
        self.x = w//2 -  self.image.get_width()//2
        self.y = h - self.image.get_height()
        self.x_midle = self.image.get_width()/2 + self.x
        self.y_midle = self.image.get_height()/2 + self.y
        self.vel = 10
        self.persentage = 0.6
        self.hitbox_h_w = [85,65] 
        self.hitbox = (self.x,self.y,self.image.get_width(),self.image.get_height())
        self.showhitbox = False
        self.bps = 5
        self.facing = [0,-1]
        self.shieldbarcolor = (0,0,200)
        self.shieldimg =pygame.image.load('p_shield.PNG')
        self.shieldtime = 50
        self.shield_eanable_time = 0
        self.shield = shield(self)
        self.health = 100
        self.maxhealth = 100
        self.healthbarcolor = (0,255,0)
        allhitbox.append([self.hitbox,self])
        self.b_damage = 1
        self.b_vel = 14
        self.b_cooldown = 6
        self.b_bounce = False
        allss.append(self)
    def draw_hitbox(self):
        pygame.draw.rect(screen,(255,0,0),self.hitbox,1)
class shield:
    def __init__(self,o):
        self.image = o.shieldimg
        self.image.set_alpha(100)
        self.x = o.x
        self.y = o.y
        self.mntime = o.shield_eanable_time
        self.mxtime = o.shieldtime
        self.time = o.shieldtime
        self.enable = False
class enenmy:
    def __init__(self):
        self.image = pygame.image.load('boss.PNG')
        self.x = screen.get_width()//2 - self.image.get_width()//2
        self.y = -40
        self.x_midle = self.image.get_width()/2 + self.x
        self.y_midle = self.image.get_height()/2 + self.y
        self.hitbox = (self.x,self.y,self.image.get_width(),self.image.get_height())
        self.bps = 3
        self.facing = [-1,0]
        self.vel = 6
        self.folow = False
        self.health = 497
        self.maxhealth = 497
        self.healthbarcolor = (255,0,0)
        self.shieldimg =pygame.image.load('shield.PNG')
        self.shieldtime = 300
        self.shield_eanable_time = 0
        self.shield = shield(self)
        allhitbox.append([self.hitbox,self])
        self.b_damage = 3
        self.b_vel = 18
        self.b_cooldown = 8
        self.b_bounce = False
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
        if self.rect.collidepoint(p) and alpha == 200:
            if not(self.hovered):
                hover.set_volume(1)
                if muted:
                    hover.set_volume(0)
                hover.play()    
            self.hovered = True
            if pygame.mouse.get_pressed()[0] or self.clicked:
                self.clicked = True
                screen.blit(self.image,(self.rect.x,self.rect.y))
            else:
                screen.blit(self.himage,(self.rect.x-(self.himage.get_width()-self.image.get_width())//2,self.rect.y- (self.himage.get_height()-self.image.get_height())//2))
        else:
            self.hovered = False
            screen.blit(self.image,(self.rect.x,self.rect.y))
    def sdraw(self,alpha):
        self.image.set_alpha(alpha)
        screen.blit(self.image,(self.rect.x,self.rect.y))
class epmty():
    def sdraw(self,x):
        pass
def reset(pa,q,hard = epmty()):
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
    del(hard)
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
    if muted:
        pygame.mixer.music.set_volume(0.0)
def button_animation(pa,q,alpha,hard = epmty()):
    while alpha > 0:
        pygame.time.wait(1)
        screen.fill((0,0,0))
        pa.sdraw(alpha)
        q.sdraw(alpha)
        hard.sdraw(alpha)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        alpha -= 1
    return True
def d_medium():
    p.vel = 10
    p.bps = 3
    p.health = 20
    p.maxhealth = 20
    p.shield.mxtime = 70
    p.shield.time = 70
    p.b_damage = 3
    p.b_vel = 16
    p.b_cooldown = 6
    e.vel = 6
    e.bps = 1
    e.health = 600
    e.maxhealth = 600
    e.shield.mntime = -400
    e.shield.mxtime = 300
    e.shield.time = 300
    e.b_damage = 3
    e.b_vel = 10
    e.b_cooldown = 8
def d_easy():
    p.vel = 12
    p.bps = 5
    p.health = 30
    p.maxhealth = 30
    p.shield.mxtime = 100
    p.shield.time = 100
    p.b_damage = 3
    p.b_vel = 20
    p.b_cooldown = 4
    e.vel = 4
    e.bps = 1
    e.health = 600
    e.maxhealth = 600
    e.shield.mntime = -300
    e.shield.mxtime = 300
    e.shield.time = 300
    e.b_damage = 3
    e.b_vel = 8
    e.b_cooldown = 10


def d_hard():
    p.vel = 9
    p.bps = 1
    p.health = 15
    p.maxhealth = 15
    p.shield.mxtime = 50
    p.shield.time = 50
    p.b_damage = 3
    p.b_vel = 12
    p.b_cooldown = 7
    e.vel = 7
    e.bps = 3
    e.health = 600
    e.maxhealth = 600
    e.shield.mntime = -400
    e.shield.mxtime = 200
    e.shield.time = 200
    e.b_damage = 2.5
    e.b_vel = 10
    e.b_cooldown = 7
    e.b_bounce = True
def start(e):
    global muted
    muted = e
    cooldownsh = 0
    scale = 0.5
    easy = buttons(w//2-(p_button.get_width()*scale)//2,h//2-((e_button.get_height()*scale))-((m_button.get_height()*scale))//2 - 20,e_button,scale)
    medium = buttons(w//2-(q_button.get_width()*scale)//2,h//2-((m_button.get_height()*scale))//2,m_button,scale)
    hard = buttons(w//2-(q_button.get_width()*scale)//2,h//2+((e_button.get_height()*scale))-((m_button.get_height()*scale))//2 + 20,h_button,scale)
    alpha = 0
    while True:
        keys = pygame.key.get_pressed()
        if keys[K_SPACE] and cooldownsh == 0:
            if muted:
                muted = False
            else:
                muted = True
            cooldownsh = 20
        pygame.time.wait(2)
        screen.fill((0,0,0) )
        easy.draw(alpha)
        medium.draw(alpha)
        hard.draw(alpha)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == K_e:
                    easy.clicked = True
                if event.key == K_m:
                    medium.clicked = True
                if event.key == K_h:
                    hard.clicked = True
        if medium.clicked:
            click.play()
            if muted:
                click.set_volume(0)  
            d_medium()
            pygame.mixer.music.play(-1)
            return button_animation(easy,medium,alpha,hard)
        if easy.clicked:
            click.play()
            if muted:
                click.set_volume(0) 
            d_easy()
            pygame.mixer.music.play(-1)
            return button_animation(easy,medium,alpha,hard)
        if hard.clicked:
            click.play()
            if muted:
                click.set_volume(0) 
            d_hard()
            pygame.mixer.music.play(-1)
            return button_animation(easy,medium,alpha,hard)
        if alpha < 200:
            alpha += 1
        if cooldownsh > 0:
            cooldownsh -= 1
def button(e):
    global muted
    muted = e
    cooldownsh = 0
    scale = 0.5
    pa = buttons(w//2-(p_button.get_width()*scale)//2,h//2-((p_button.get_height()//2*scale))-10,p_button,scale)
    q = buttons(w//2-(q_button.get_width()*scale)//2,h//2+((q_button.get_height()//2*scale))+10,q_button,scale)
    alpha = 0
    while True:
        keys = pygame.key.get_pressed()
        if keys[K_SPACE] and cooldownsh == 0:
            if muted:
                muted = False
            else:
                muted = True
            cooldownsh = 20
        pygame.time.wait(2)
        screen.fill((0,0,0) )
        pa.draw(alpha)
        q.draw(alpha)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == K_p:
                    pa.clicked = True
                if event.key == K_q:
                    q.clicked = True
        if q.clicked:
            click.play()
            if muted:
                click.set_volume(0) 
            button_animation(pa,q,alpha)
            return False
        if pa.clicked:
            click.play()
            reset(pa,q)
            if muted:
                click.set_volume(0) 
            a = button_animation(pa,q,alpha)
            if not(a):
                return False
            return start(muted)
        if alpha < 200:
            alpha += 1
        if cooldownsh > 0:
            cooldownsh -= 1
def loose(muted):
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
    s_loose.play()
    if muted:
        s_loose.set_volume(0)
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
    return button(muted)
def win(muted):
    s_win.play()
    if muted:
       s_win.set_volume(0) 
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
    return button(muted)
def draw ():
    screen.fill((0,0,0))
    screen.blit(bg,(0,0))
    p.shield.x = p.x
    p.shield.y = p.y
    if p.showhitbox:
        p.draw_hitbox()
        e.draw_hitbox()
    if p.shield.time > 0:
        pygame.draw.line(screen,p.shieldbarcolor,(0,h-30),(((p.shield.mxtime*(w//p.shield.mxtime))-(p.shield.mxtime-p.shield.time)*(w//p.shield.mxtime))//4,h-30),20)
    pygame.draw.line(screen,(255,0,0),(((p.shield.mxtime*(w//p.shield.mxtime))-(p.shield.mxtime-20)*(w//p.shield.mxtime))//4,h-40),(((p.shield.mxtime*(w//p.shield.mxtime))-(p.shield.mxtime-20)*(w//p.shield.mxtime))//4,h-20),3)
    if e.health > 0:
        pygame.draw.line(screen,e.healthbarcolor,(0,10),(w-(e.maxhealth-e.health)*(w/e.maxhealth),10),20)
    if p.health > 0:
        pygame.draw.line(screen,p.healthbarcolor,(0,h-10),(w-(p.maxhealth-p.health)*(w/p.maxhealth),h-10),20)
    for bullet in bullets.all:
        screen.blit(bullet.image,(bullet.x,bullet.y))
    screen.blit(e.image,(e.x,e.y))
    screen.blit(p.image ,(p.x,p.y))
    if e.shield.enable:
        screen.blit(e.shield.image,(e.shield.x,e.shield.y))
    if p.shield.enable:
        screen.blit(p.shield.image,(p.shield.x,p.shield.y))
    pygame.display.update()
def inside(hitbox,bullet):
     hitbox = list(hitbox[0])
     bullet = [bullet.x,bullet.y,bullet.image.get_width(),bullet.image.get_height()]
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
muted = False
run = start(muted)
while run:
    x = 0
    y = 0
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
        pygame.mixer.music.unpause()
    if keys[K_SPACE] and cooldownsh == 0:
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
    if keys[K_z] and ((p.shield.enable == True and p.shield.time > 0)or(p.shield.time > 20)):
        p.shield.enable = True
        p.shield.time -= 1
    else:
        p.shield.enable = False
    if keys[K_x] and cooldownb == 0:
        p.facing = [-1,0]
        for i in range(p.bps):
            f = (2/(p.bps+1))
            p.facing = [f*(i+1) - 1,-(1-(abs(f*(i+1)-1)))]
            p_bullet(p)
        cooldownb = bullets.all[-1].cooldown
        bullets.all[-1].sound.play()
        if (muted):
            bullets.all[-1].sound.set_volume(0)
    if abs(x)+abs(y) == p.vel*2:
        x *= p.persentage
        y *= p.persentage
    p.x += x
    p.x_midle += x
    p.y += y
    p.y_midle += y
    for bullet in bullets.all:
        bullet.vel = bullet.ss.b_vel
        bullet.damage = bullet.ss.b_damage
        bullet.cooldown = bullet.ss.b_cooldown
        bullet.x += bullet.facing[0] * bullet.vel
        bullet.y += bullet.facing[1] * bullet.vel
        bullet.rect.topleft = (x,y)
        index = bullets.all.index(bullet)
        if   bullet.y + bullet.image.get_height() <= 0 or bullet.y >=screen.get_height():
            del(bullet)
            bullets.all.pop(index)
        elif bullet.x  <= 0 or bullet.x + bullet.image.get_width() >=(screen.get_width()) :
            if bullet.ss.b_bounce:
                bullet.facing[0] *= -1
                if bullet.x + bullet.image.get_width() >=(screen.get_width()):
                    bullet.x = w-bullet.image.get_width()
                elif bullet.x <= 0:
                    bullet.x = 0
            elif bullet.x+ bullet.image.get_width()  <= 0 or bullet.x  >=(screen.get_width()):
                del(bullet)
                bullets.all.pop(index)
        else:
            for hitbox in allhitbox:
                if hitbox[1] != bullet.ss and inside(hitbox,bullet):
                    if not (hitbox[1].shield.enable):
                        hitbox[1].health -= bullet.damage
                    bullet.damages.play()
                    if  muted:
                        bullet.damages.set_volume(0)
                    del(bullet)
                    bullets.all.pop(index)
                    break
    if e.folow:
        if (abs(e.x_midle - p.x_midle) < e.vel*p.persentage)  and (((not(keys[K_RIGHT or K_LEFT] or (keys[K_LEFT] and keys[K_RIGHT]))))):
            e.x_midle = p.x_midle
            e.x = e.x_midle - e.image.get_width()/2
        elif e.x_midle > p.x_midle and e.x_midle - p.x_midle > e.vel*p.persentage:
            e.x_midle -= e.vel
            e.x -= e.vel
        elif e.x_midle < p.x_midle and p.x_midle - e.x_midle > e.vel*p.persentage:
            e.x_midle += e.vel
            e.x += e.vel     
    p.hitbox = ((p.x+5,p.y+5,p.hitbox_h_w[0],p.hitbox_h_w[1]))
    e.hitbox = (e.x,e.y,e.image.get_width(),e.image.get_height())
    e.shield.x = e.x
    e.shield.y = e.y - 90
    e.shield.hitbox = e.hitbox
    if cooldownbb == 0:
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
        if y == 0:
            y = 1
        e.facing = [x/(x+y) *xn,y/(x+y)*yn]
        f_x = e.facing[0]
        if ((e.facing[0]+1-f_x)/round(e.bps/2+0.01)) -1 + f_x < -1 :
            e.facing = [e.facing[0]+(((e.facing[0]+1-f_x)/round(e.bps/2+0.01))*(e.bps - round(e.bps/2 + 0.1))),1-e.facing[0]+(((e.facing[0]+1-f_x)/round(e.bps/2+0.01))*(e.bps - round(e.bps/2 + 0.1)))]
        elif ((e.facing[0]+1-f_x)/round(e.bps/2+0.01))*e.bps -1 + f_x > 1 :
            e.facing = [e.facing[0]-(((e.facing[0]+1-f_x)/round(e.bps/2+0.01))*(e.bps - round(e.bps/2 + 0.1))),1-e.facing[0]-(((e.facing[0]+1-f_x)/round(e.bps/2+0.01))*(e.bps - round(e.bps/2 + 0.1)))]
        f_x = e.facing[0]
        for i in range(e.bps):
            f = (2/(e.bps+1))
            e.facing = [f*(i+1)-1 + f_x,(1-(abs(f*(i+1)-1 + f_x)))]
            b_bullet(e)
        bullets.all[-1].sound.play()
        if (muted):
            bullets.all[-1].sound.set_volume(0)
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
    if e.shield.time == e.shield.mntime:
        e.folow = False
        e.shield.enable = False
        e.shield.time = e.shield.mxtime
    allhitbox = [[p.hitbox,p],[e.hitbox,e]]
    if e.health <= 0:
        run = win(muted)
    if p.health <= 0:
        run = loose(muted)
    if muted:
        pygame.mixer.music.set_volume(0)
    else:
        pygame.mixer.music.set_volume(0.5)
    if keys[K_ESCAPE] and cooldownsh == 0:
        paused = True
        pygame.mixer.music.pause()
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    paused = False
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        paused = False
                        cooldownsh = 6
    if not(p.shield.enable) and p.shield.time < p.shield.mxtime:
        p.shield.time += 0.2
    pygame.time.wait(0)
pygame.quit()