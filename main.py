import pygame
import random
import os
from math import sin, cos
from static_oblects import *
from moving_oblects import *

#Чтобы перевести ПВО в автоматический режим нужно нажать "E"
gamespeed = 1
max_distance = 800
dulo = 80
spawn_cd = 40 / gamespeed
cold_cd = 7 / gamespeed
cold = 10
S_R = 0.01 #Площадь сечения ракеты
R_R = 0.01 #радиус сечения раекеты
running = True
lr, rr = False, False
bullet_speed = 100
Pi = 3.14
spawn = -100
id = 0
radar_cd = 0
WIDTH = 1200
HEIGHT = 800
FPS = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Airdefence")

clock = pygame.time.Clock()

bullets = pygame.sprite.Group()
rockets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

target = Target()
player = PVO()
wall = Wall()

radar = Radar(max_distance)

all_sprites.add(target)
all_sprites.add(wall)
all_sprites.add(player)

def check(rocket):
    x0, y0 = player.rect.center[0] + cos(player.rot * Pi / 180) * dulo, player.rect.center[1] - sin(player.rot * Pi / 180) * dulo
    v0x, v0y = bullet_speed * cos(player.rot * Pi / 180), bullet_speed * sin(player.rot * Pi / 180)
    x1, y1 = rocket.rect.center[0], rocket.rect.center[1]
    v1x, v1y = rocket.vx, rocket.vy
    R = 0.01
    dt = 0.1
    g = -10
    a0 = 10 * 30 / FPS
    tm = 0
    while tm < 7:
        if ((x0 - x1) ** 2 + (y0 - y1) ** 2) ** 0.5 < 20:
            return True
        asoprx = - 1.23 * v0x * abs(v0x) / 2 * 0.4 * pi * R * R
        asopry = - 1.23 * v0y * abs(v0y) / 2 * 0.4 * pi * R * R
        ax = asoprx
        ay = asopry + g
        y0 += -(v0y * dt + ay * dt ** 2 / 2)
        x0 += v0x * dt + ax * dt ** 2 / 2
        v0x += ax * dt
        v0y += ay * dt

        ax1 = a0 * sin(rocket.ang)
        ay1 = a0 * cos(rocket.ang)
        y1 += v1y * dt + ay1 * dt ** 2 / 2
        x1 += v1x * dt + ax1 * dt ** 2 / 2
        v1x += ax1 * dt
        v1y += ay1 * dt

        tm += dt
    return False

auts = False
while running:
    clock.tick(FPS)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    if not auts and keys[pygame.K_e]:
        auts = True
    elif auts and keys.count(True) > 0:
        auts = False
    if auts:
        if abs(player.rot - 45) > 2:
            if player.rot > 45:
                player.rotate(-1)
            else:
                player.rotate(1)
        for elem in pygame.sprite.Group.sprites(rockets):
            if check(elem) and cold > cold_cd / 30 * FPS:
                b = Bullet(bullet_speed * cos(player.rot * Pi / 180), bullet_speed * sin(player.rot * Pi / 180), player.rect.center[0] + cos(player.rot * Pi / 180) * dulo, player.rect.center[1] - sin(player.rot * Pi / 180) * dulo, 0.01, 0.01, id, False)
                bullets.add(b)
                all_sprites.add(b)
                cold = 0

            
        #else:
            #print(radar.machine_scan(rockets))
        
    

    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and cold > cold_cd / 30 * FPS:
            cold = 0
                    #               vx,                               vy,                                        x0,                                                            y0,                                                    S,   R, id, air_resistance
            b = Bullet(bullet_speed * cos(player.rot * Pi / 180), bullet_speed * sin(player.rot * Pi / 180), player.rect.center[0] + cos(player.rot * Pi / 180) * dulo, player.rect.center[1] - sin(player.rot * Pi / 180) * dulo, 0.01, 0.01, id, False)
            #print(b.vx, b.vy)
            bullets.add(b)
            all_sprites.add(b)
        
    

        if keys[pygame.K_a]:
            lr = True
        else:
            lr = False
        if keys[pygame.K_d]:
            rr = True
        else:
            rr = False
        if rr:
            player.rotate(-1)
        elif lr:
            player.rotate(1)


    if radar_cd > 40 / 30 * FPS:
        radar_cd = 0
        radar.scan(rockets)
    radar_cd += 1
    if spawn > spawn_cd / 30 * FPS:
        #               vx, vy, x0, y0, S, R, id, air_resistance
        rocket = Rocket(0, 0, random.randrange(1, WIDTH), 0, S_R, R_R, id, True)
        id += 1
        all_sprites.add(rocket)
        rockets.add(rocket)
 
        spawn = 0
    spawn += 1
    hits = pygame.sprite.spritecollide(target, rockets, False, pygame.sprite.collide_rect_ratio(0.7))

    for bul in bullets:
        if pygame.sprite.spritecollide(bul, rockets, True):
            bul.kill()
    if hits:
        for i in hits:
            i.kill()
        if hits[0].type == "enemy":
            f1 = pygame.font.Font(None, 36)
            text1 = f1.render('Бункер был уничтожен вражескими ракетами', True,
                        (180, 0, 0))
            screen.blit(text1, (10, 50))
            pygame.display.update()
            f = True
            while f:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        f = False
                        break
            running = False


    all_sprites.update()
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()
    cold += 1
pygame.quit()