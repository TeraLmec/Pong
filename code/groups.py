from settings import *

class Allsprites(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        
    def draw(self):
        # drawing shadow surface
        for sprite in self:
            for i in range(5):
                self.display_surface.blit(sprite.shadow, sprite.rect.topleft + pg.Vector2(i,i))
        
        # drawing main surface
        for sprite in self:
            self.display_surface.blit(sprite.image, sprite.rect)
            
class Ballsprites(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        
    def draw(self):
        # drawing shadow surface
        for sprite in self:
            for i in range(len(sprite.blur_surf)):
                self.display_surface.blit(sprite.blur_surf[i], sprite.old_pos[i])
                
        # drawing main surface
        for sprite in self:
            self.display_surface.blit(sprite.image, sprite.rect)
