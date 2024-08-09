import pygame
from math import atan, pi, sqrt
import os
WIDTH = 1200
HEIGHT = 800
FPS = 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TEST")
BLACK = (0, 0, 0)


class Target(pygame.sprite.Sprite):
    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')
    image = pygame.image.load(os.path.join(img_folder, 'bunker.png')).convert()
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.radius = 10
        
        #self.rect.inflate_ip(-100, -100)
        self.rect.center = (800, 700)
        self.image.set_colorkey(BLACK)
        
        
class Wall(pygame.sprite.Sprite):
    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')
    image = pygame.image.load(os.path.join(img_folder, 'wall.png')).convert()
    x, y = WIDTH // 3, HEIGHT - 100
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
    
class PVO(pygame.sprite.Sprite):
    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')
    image = pygame.image.load(os.path.join(img_folder, 'PVO.png')).convert()
    x, y = WIDTH // 3, HEIGHT - 100
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rot = 0
        self.rot_speed = 30 / FPS
        self.orig_img = self.image
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.center = (self.x, self.y)
    def rotate(self, d):
        self.rot = (self.rot + self.rot_speed * d) % 360
        self.image = pygame.transform.rotate(self.orig_img, self.rot)
        self.rect = self.image.get_rect(center=self.rect.center)

class Radar():
    x0, y0 = WIDTH // 3, HEIGHT - 100
    def __init__(self, md):
        self.md = md
    def scan(self, rockets):
        ans = []
        for elem in pygame.sprite.Group.sprites(rockets):
            
            x1, y1 = elem.x, elem.y
            x0, y0 = self.x0, self.y0
            ang =  atan((x1 - x0) / (y1 - y0))
            distance = sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
            if distance < self.md:
                ans.append((elem.id, ang * 180 / pi, distance))
        print("SCANING: ", end = "")
        print(*ans)
    def machine_scan(self, rockets):
        ans = []
        for elem in pygame.sprite.Group.sprites(rockets):
            x1, y1 = elem.x, elem.y
            x0, y0 = self.x0, self.y0
            ang =  atan((x1 - x0) / (y1 - y0))
            distance = sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
            if distance < self.md:
                ans.append(elem)
        return ans