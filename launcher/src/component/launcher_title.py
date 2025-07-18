import pygame
from util.asset_paths import image_path, font_path

class LauncherTitle:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.background = pygame.image.load(image_path("title_background.png"))
        self.background_coords = (self.center_x(self.background), self.center_y(self.background))
        self.fonts = pygame.font.Font(font_path("open-dyslexic.ttf"), 40)
        self.line_1 = self.fonts.render("Colección de", True, (50, 50, 55))
        self.line_1_coords = (self.center_x(self.line_1), 270)
        self.line_2 = self.fonts.render("Minijuegos de", True, (50, 50, 55))
        self.line_2_coords = (self.center_x(self.line_2), 320)
        self.line_3 = self.fonts.render("Destreza", True, (50, 50, 55))
        self.line_3_coords = (self.center_x(self.line_3), 370)
    
    def draw(self):
        self.surface.blit(self.background, self.background_coords)
        self.surface.blit(self.line_1, self.line_1_coords)
        self.surface.blit(self.line_2, self.line_2_coords)
        self.surface.blit(self.line_3, self.line_3_coords)
        
    def center_x(self, target_surface: pygame.Surface):
        return (self.surface.get_width() - target_surface.get_width()) / 2
    
    def center_y(self, target_surface: pygame.Surface):
        return (self.surface.get_height() - target_surface.get_height()) / 2