from settings import *

class Ball(pg.sprite.Sprite):
    def __init__(self, group, paddle_sprites):
        # setup
        super().__init__(group)
        self.paddle_sprites = paddle_sprites
        self.sound()
        self.image = pg.Surface(SIZE["ball"], pg.SRCALPHA)
        pg.draw.circle(self.image, COLORS["ball"], (SIZE["ball"][0]/2, SIZE["ball"][1]/2), SIZE["ball"][0]/2)
        self.rect = self.image.get_frect(center = POS["ball"])
        self.speed = SPEED["ball"]
        self.dir = pg.Vector2(choice((1, -1)), uniform(0.6,0.8) * choice((-1,1)))
        self.old_rect = self.rect.copy()
        
        # goal
        self.goal = False
        self.speed_mod = 1
        self.last_goal_time = 0
        
        # motion blur object
        blur_nb = 12
        
        self.blur_surf = [pg.Surface(SIZE["ball"], pg.SRCALPHA) for i in range(blur_nb)]
        for i in range(len(self.blur_surf)):
            alpha = max(0, COLORS["ball"][3] - i * 25)
            modified_color = (COLORS["ball"][0], COLORS["ball"][1], COLORS["ball"][2], alpha)
            pg.draw.circle(self.blur_surf[i], modified_color, (SIZE["ball"][0]/2, SIZE["ball"][1]/2), (SIZE["ball"][0]/2)-i)
        self.old_pos = [self.rect] * len(self.blur_surf)
        
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.motion_blur()
        self.rect.centerx += self.speed * self.dir.x * dt * self.speed_mod * SPEED["speed mult"]
        self.paddle_collisions("horizontal")
        self.rect.centery += self.speed * self.dir.y * dt * self.speed_mod * SPEED["speed mult"]
        self.paddle_collisions("vertical")
        self.wall_collisions()
        self.reset()
        
    def motion_blur(self):
        self.old_pos.pop()
        self.old_pos.insert(0, self.old_rect)
        
    def sound(self):
        # imports
        self.paddle_sound = pg.mixer.Sound(join("audio", "pong.mp3"))
        self.paddle_sound.set_volume(0.5)
        self.wall_sound = pg.mixer.Sound(join("audio", "ping.mp3"))
        self.wall_sound.set_volume(0.5)
        self.goal_sound = pg.mixer.Sound(join("audio", "goal.mp3"))
        self.goal_sound.set_volume(0.6)
        
    def reset(self):
        if self.rect.right >= WINDOW_WIDTH or self.rect.left <= 0:
            self.last_goal_time = pg.time.get_ticks()
            self.goal_sound.play()
            SPEED["speed mult"] = 1
        if pg.time.get_ticks() - self.last_goal_time < 1000:
            self.speed_mod = 0
        else:
            self.speed_mod = 1
    
    def paddle_collisions(self, direction):
        for sprite in self.paddle_sprites:
            if sprite.rect.colliderect(self.rect):
                SPEED["speed mult"] += 0.2
                self.paddle_sound.play()
                if direction == "horizontal":
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.dir.x *= -1 
                    elif self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.dir.x *= -1
                if direction == "vertical":
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.dir.y *= -1 
                    elif self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.dir.y *= -1
                        
    def wall_collisions(self):
        # wall
        if self.rect.top <= 0:
            self.rect.top = 0
            self.dir.y *= -1
            self.wall_sound.play()
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.dir.y *= -1
            self.wall_sound.play()
        
    