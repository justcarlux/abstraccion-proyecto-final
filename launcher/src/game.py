import pygame
from component.entries import GameEntries
from component.launcher_title import LauncherTitle
from util.asset_paths import image_path

class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption(f"Colección de Minijuegos de Destreza")
        self.is_running = True
        self.clock = pygame.time.Clock()
        self.game_entries = GameEntries(self.display)
        self.launcher_title = LauncherTitle(self.display)
        self.background = pygame.image.load(image_path("background.png"))

    def run(self):
        while self.is_running:
            self.handle_events()
            self.display.fill((0, 0, 0))
            
            self.display.blit(self.background, (0, 0))
            self.launcher_title.draw()
            self.game_entries.draw()

            pygame.display.flip()
            self.clock.tick(60)

    def stop(self):
        self.is_running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.game_entries.on_click()