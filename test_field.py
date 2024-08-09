import pygame
import random
import os
from math import sin, cos
from static_oblects import *
from moving_oblects import *

FPS = 100
WHITE = (255, 255, 255)
vx = 1
vy = 1
x0, y0 = 1000, 0
S, m, R = 1, 1, 1
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Airdefence")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
#          vx, vy, x0, y0, S, R, id, air_resistance
r = Rocket(vx, vy, x0, y0, S, R, id, True)
t = Target()
#         vx, vy, x0,       y0,     S,    R, id, air_resistance
b = Bullet(100, 100, 100, HEIGHT - 100, 0.01, 0.01, 1, False)
all_sprites.add(r)
all_sprites.add(t)
all_sprites.add(b)
running = True

while running:
    clock.tick(FPS)
   
   
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
  
   


    all_sprites.update()

    
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()