import pygame
from math import sqrt, atan, cos, sin, pi
import os
WIDTH = 1200
HEIGHT = 800
FPS = 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TEST")


class MovingObject(pygame.sprite.Sprite):
    rotate = False
    a0 = 0
    ang = 0
    g = -10
    d = 1
    image = pygame.Surface((50, 50))
    orig_img = image
    color = (0, 0, 0)
    def __init__(self, vx, vy, x0, y0, S, R, id, air_resistance):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.vx = vx
        self.vy = vy
        self.x = x0
        self.y = y0
        self.S = S
        self.R = R
        self.air_resistance = air_resistance

        self.rect = self.image.get_rect()
        self.image.set_colorkey(self.color)
        self.rect.center = (self.x, self.y) 

    def update(self):
        R = self.R
        dt = 0.1
        vx, vy = self.vx, self.vy
        self.angle_for_bullet = atan(self.vy / self.vx) if self.vx != 0 else 0
        asoprx = - 1.23 * vx * abs(vx) / 2 * 0.4 * pi * R * R * int(not self.air_resistance)
        asopry = - 1.23 * vy * abs(vy) / 2 * 0.4 * pi * R * R * int(not self.air_resistance)
        g = self.g
        ax = asoprx + self.a0 * sin(self.ang)
        ay = asopry + self.a0 * cos(self.ang) + g
        self.y += self.d * (self.vy * dt + ay * dt ** 2 / 2)
        self.x += self.vx * dt + ax * dt ** 2 / 2
        self.vx += ax * dt
        self.vy += ay * dt
        self.rect.center = (self.x, self.y)
        if self.rotate:
            rot = self.angle_for_bullet * 180 / pi
            self.image = pygame.transform.rotate(self.orig_img, rot - 90)
            self.rect = self.image.get_rect(center=self.rect.center)
class Rocket(MovingObject):
    color = (255, 255, 255)
    type = "enemy"
    x1, y1 = 800, 700
    v = 30 * 30 / FPS
    g = 0
    a0 = 10 * 30 / FPS
    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')
    image = pygame.image.load(os.path.join(img_folder, 'rocket.png')).convert()
    def __init__(self, vx, vy, x0, y0, S, R, id, air_resistance):
        super().__init__(vx, vy, x0, y0, S, R, id, air_resistance)
        pygame.sprite.Sprite.__init__(self)
        self.ang = atan((self.x1 - x0) / (self.y1 - y0))
        self.image = pygame.transform.rotate(self.image, self.ang * 180 / pi - 90)
        self.vx = self.v * sin(self.ang)
        self.vy = self.v * cos(self.ang)

class Bullet(MovingObject):
    type = "bullet"
    g = -10
    a0 = 0
    d = -1
    rotate = True
    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')
    image = pygame.image.load(os.path.join(img_folder, 'bullet.png')).convert()
    orig_img = image
    color = (0, 0, 0)
    def __init__(self, vx, vy, x0, y0, S, R, id, air_resistance):
        super().__init__(vx, vy, x0, y0, S, R, id, air_resistance)

