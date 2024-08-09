dt = 0.1
        C = 0.4
        S = self.S
        g = -10
        p = 1.2
        if self.vx == 0:
            d = -1 if self.vy < 0 else 1
            a = 1/2 * d
        else:
            a = atan(self.vy / self.vx)
        V = sqrt(self.vx ** 2 + self.vy ** 2)
        m = self.m

        Fsopr = -C * S * abs(V) * V * p / 2
        print(self.vx, self.vy, Fsopr)
       

        if self.vx != 0:
             ax = Fsopr * cos(a) / m
        else:
            ax = 0
        if self.vy != 0:
            ay = Fsopr * sin(a) / m
        else:
            ay = 0

        self.x += self.vx * dt + ax * dt ** 2 / 2
        self.y -= self.vy * dt + (ay + g) * dt ** 2 / 2
        
        if self.vx > 0:
            self.vx = max(self.vx + ax * dt, 0)
        else:
            self.vx = min(self.vx + ax * dt, 0)
        if self.vy > 0:
            self.vy = max(self.vy + ay * dt, 0)
        else:
            self.vy = min(self.vy + ay * dt, 0)
        self.vy += g * dt

        #self.y += -(self.vy * dt + ay * dt ** 2 / 2)
        #self.vy += ay * dt
        #self.x += self.vx * dt

class Rocket(MovingObject):
    def __init__(self, v, x0, y0, x1, y1, S, m, img):
        super().__init__(vx, vy, x0, y0, S, m, img)
        self.type = "enemy"
        self.ang = atan((x1 - x0) / (y1 - y0))
        self.vx = v * sin(self.ang)
        self.vy = v * cos(self.ang)
        self.m = m
        self.img = img
        self.rect = self.image.get_rect()
        self.image.set_colorkey((255, 255, 255))
        self.rect.center = (self.x, self.y) 
    def update(self):
        g = -10
        dt = 0.1
        self.y -= self.vy * dt + g * dt ** 2 / 2
        self.x += self.vx * dt
        self.vy += g * dt