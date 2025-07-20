import pygame
from component.entries import GameEntries
from component.launcher_title import LauncherTitle
from component.volume import VolumeToggler
from util.asset_paths import image_path
from manager.sounds import SoundManager

class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption(f"Colección de Minijuegos de Destreza")
        self.is_running = True
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load(image_path("background.png"))
        self.game_entries = GameEntries(self.display)
        self.launcher_title = LauncherTitle(self.display)
        self.sound_manager = SoundManager()
        self.volume_toggler = VolumeToggler(self.display, self.sound_manager)

    def run(self):
        self.sound_manager.play_music()
        while self.is_running:
            self.handle_events()
            self.display.fill((0, 0, 0))
            
            self.display.blit(self.background, (0, 0))
            self.launcher_title.draw()
            self.game_entries.draw()
            self.volume_toggler.draw()

            if (self.game_entries.hovered or self.volume_toggler.hovered):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            pygame.display.flip()
            self.clock.tick(60)

    def stop(self):
        self.is_running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.game_entries.on_screen_click()
                if (self.volume_toggler.hovered):
                    self.volume_toggler.on_click()