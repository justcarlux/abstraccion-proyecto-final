import pygame
import os
import sys
import subprocess
from util.asset_paths import font_path

ROOT_GAMES_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class GameEntry:
    def __init__(self, index: int, name: str, entry_file: str, coords: tuple[int, int]):
        self.name = name
        self.hovered = False
        self.main_file = entry_file
        self.full_game_path = os.path.join(ROOT_GAMES_PATH, str(index + 1), entry_file)
        self.rect = pygame.Rect(coords[0], coords[1], 340, 160)
        self.color = (100, 180, 250)
        self.hover_color = (90, 160, 230)
        self.text_color = (55, 55, 55)
        self.font = pygame.font.Font(font_path("open-dyslexic.ttf"), 34)
        self.line_1 = self.font.render(f"Minijuego #{index + 1}:", True, self.text_color)
        self.line_1_rect = self.line_1.get_rect(center=self.rect.center).move(0, -23)
        self.line_2 = self.font.render(name, True, self.text_color)
        self.line_2_rect = self.line_2.get_rect(center=self.rect.center).move(0, 23)
        
    def draw(self, surface: pygame.Surface):
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(surface, self.hover_color if self.hovered else self.color, self.rect, border_radius=12)
        surface.blit(self.line_1, self.line_1_rect)
        surface.blit(self.line_2, self.line_2_rect)
        
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

class GameEntries():
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.entries: list[GameEntry] = []
        self.hovered = False
        
        self.__register("Simon Says", "main.py", (330, 10))
        self.__register("Deslizamente", "intro_deslizamente.py", (680, 10))
        self.__register("Luces apagadas", "Lights out-grupo 3.py", (895, 200))
        self.__register("Colores mágicos", "ColoresMagicos.py", (895, 380))
        self.__register("Memoria", "src/main.py", (680, 550))
        self.__register("Matigatito", "Matigatito.py", (330, 550))
        self.__register("Sopa de letras", "Sopa_de_letras_OAD-3.py", (40, 380))
        self.__register("Ahorcado", "main3.py", (40, 200))

    def __register(self, name: str, entry_file: str, coords: tuple[int, int]):
        self.entries.append(GameEntry(len(self.entries), name, entry_file, coords))
        
    def draw(self):
        self.hovered = False
        for entry in self.entries:
            entry.draw(self.surface)
            if entry.hovered:
                self.hovered = True
            
    def on_screen_click(self):
        for entry in self.entries:
            if entry.hovered:
                entry.on_click()