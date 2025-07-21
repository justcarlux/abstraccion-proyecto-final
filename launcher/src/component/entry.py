import pygame
import os
import sys
import subprocess
from util.asset_paths import font_path

ROOT_GAMES_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class GameEntry:
    def __init__(self, index: int, name: str, entry_file: str, coords: tuple[int, int], surface: pygame.Surface):
        self.name = name
        self.hovered = False
        self.main_file = entry_file
        self.full_game_path = os.path.join(ROOT_GAMES_PATH, str(index + 1), entry_file)
        self.rect = pygame.Rect(coords[0], coords[1], 340, 160)
        self.surface = surface
        self.color = (100, 180, 250)
        self.hover_color = (90, 160, 230)
        self.text_color = (55, 55, 55)
        self.font = pygame.font.Font(font_path("open-dyslexic.ttf"), 34)
        self.line_1 = self.font.render(f"Minijuego #{index + 1}:", True, self.text_color)
        self.line_1_rect = self.line_1.get_rect(center=self.rect.center).move(0, -23)
        self.line_2 = self.font.render(name, True, self.text_color)
        self.line_2_rect = self.line_2.get_rect(center=self.rect.center).move(0, 23)
        
    def draw(self):
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(self.surface, self.hover_color if self.hovered else self.color, self.rect, border_radius=12)
        self.surface.blit(self.line_1, self.line_1_rect)
        self.surface.blit(self.line_2, self.line_2_rect)
        
    def on_click(self):
        working_dir = os.path.dirname(self.full_game_path)
        subprocess.Popen(
            [sys.executable, self.full_game_path],
            cwd=working_dir,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
