import pygame
from util.asset_paths import image_path
from manager.sounds import SoundManager
from manager.settings import SettingsManager

class VolumeToggler:
    def __init__(self, surface: pygame.Surface, sound_manager: SoundManager, settings: SettingsManager):
        self.surface = surface
        self.settings = settings
        self.sound_manager = sound_manager
        self.volume_image = pygame.image.load(image_path("volume.png"))
        self.muted_volume_image = pygame.image.load(image_path("volume_muted.png"))
        self.corner_margin = 10
        self.rect = pygame.Rect(
            self.corner_margin, self.surface.get_height() - self.volume_image.get_height() - self.corner_margin,
            self.volume_image.get_width(), self.volume_image.get_height()
        )
        self.hovered = False
    
    def draw(self):
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        self.surface.blit(self.volume_image if self.settings.music_enabled else self.muted_volume_image, (self.rect.x, self.rect.y))
        
    def on_click(self):
        self.settings.toggle_music()
        if (self.settings.music_enabled):
            self.sound_manager.play_music()
        else:
            self.sound_manager.stop_music()