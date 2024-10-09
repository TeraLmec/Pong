from ball import Ball
from paddles import Opponent, Player
from settings import *
from groups import Allsprites, Ballsprites

class Game:
    def __init__(self):
        # setup
        pg.init()
        self.sound()
        self.display_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pg.time.Clock()
        pg.display.set_caption(TITLE)
        self.running = True
        
        # groups
        self.all_sprites = Allsprites()
        self.ball_sprites = Ballsprites()
        self.paddle_sprites = pg.sprite.Group()
        
        # sprites
        self.ball = Ball(self.ball_sprites, self.paddle_sprites)
        
        # setup
        self.setup()
        
        # score
        try:
            with open(join("data", "score.txt")) as score_file:
                self.score = json.load(score_file)
        except:
            self.score = {"player": 0, "opponent": 0}
        self.font = pg.font.Font(None, 160)
        
    def display_score(self):
        # player
        player_surf = self.font.render(str(self.score["player"]), True, COLORS["bg detail"])
        player_rect = player_surf.get_frect(center = (WINDOW_WIDTH/2+100, WINDOW_HEIGHT/2))
        self.display_surface.blit(player_surf, player_rect)
        
        # opponent
        opponent_surf = self.font.render(str(self.score["opponent"]), True, COLORS["bg detail"])
        opponent_rect = opponent_surf.get_frect(center = (WINDOW_WIDTH/2-100, WINDOW_HEIGHT/2))
        self.display_surface.blit(opponent_surf, opponent_rect)
        
        # mid_line
        pg.draw.line(self.display_surface, COLORS["bg detail"],(WINDOW_WIDTH/2, 0), (WINDOW_WIDTH/2, WINDOW_HEIGHT), 7)
        
    def sound(self):
        self.music = pg.mixer.Sound(join("audio", "bg_music.mp3"))
        self.music.set_volume(0.1)
        
    def ball_goal(self):
        if self.ball.rect.right >= WINDOW_WIDTH:
            self.score["opponent"] += 1
            self.ball.rect.center = BALL_SPAWN
            self.ball.dir = pg.Vector2(1, uniform(0.4,0.8) * choice((-1,1)))
        elif self.ball.rect.left <= 0:
            self.score["player"] += 1
            self.ball.rect.center = BALL_SPAWN
            self.ball.dir = pg.Vector2(-1, uniform(0.4,0.8) * choice((-1,1)))
        
    def setup(self):
        self.player = Player((self.all_sprites, self.paddle_sprites))
        self.opponent = Opponent((self.all_sprites, self.paddle_sprites), self.ball)
        self.music.play(-1)
        
    def run(self):
        while self.running:
            
            dt = self.clock.tick(100) * 0.001
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    with open(join("data", "score.txt"), "w") as score_file:
                        json.dump(self.score, score_file)
                    
            self.ball_goal()
            self.ball_sprites.update(dt)
            self.all_sprites.update(dt)
            self.display_surface.fill(COLORS["bg"])
            self.display_score()
            self.ball_sprites.draw()
            self.all_sprites.draw()
                
            pg.display.update()
            
        pg.quit()
        
if  __name__ == "__main__":
    Game().run()