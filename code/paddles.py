from settings import *

class Paddle(pg.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pg.Surface(SIZE["paddle"], pg.SRCALPHA)
        pg.draw.rect(self.image, COLORS["paddle"], pg.FRect((0, 0), SIZE["paddle"]), 0, 5)
        self.dir = pg.Vector2()
        self.old_rect = 0
        
        # shadow 
        self.shadow = self.image.copy()
        pg.draw.rect(self.shadow, COLORS["paddle shadow"], pg.FRect((0, 0), SIZE["paddle"]), 0, 5)
            
    def collisions(self):
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom =WINDOW_HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
            
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.movement()
        self.rect.centery += self.speed * self.dir.y * dt
        self.collisions()
        
class Player(Paddle):
    def __init__(self, group):
        super().__init__(group)
        self.speed = SPEED["player"]
        self.rect = self.image.get_frect(center = POS["player"])
        
    def movement(self):
        K_PRESS = pg.key.get_pressed()
        self.dir.y = K_PRESS[pg.K_s] - K_PRESS[pg.K_z]
        
class Opponent(Paddle):
    def __init__(self, group, ball):
        super().__init__(group)
        self.ball = ball
        self.rect = self.image.get_frect(center = POS["opponent"])
        self.speed = SPEED["opponent"]
        
    def movement(self):
        self.dir.y = 1 if self.ball.rect.centery+2 > self.rect.centery else -1