import pygame
from component.entry import GameEntry

class GameEntryRegistry():
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.entries: list[GameEntry] = []
        self.hovered = False
        
        self.__register("Simon Says", "main.py", (330, 10))
        self.__register("Deslizamente", "intro_deslizamente.py", (680, 10))
        self.__register("Luces apagadas", "Lights out-grupo 3.py", (895, 200))
        self.__register("Colores mágicos", "ColoresMagicos.py", (895, 380))
        self.__register("Memoria", "src/main.py", (680, 550))
        self.__register("Súpergatito", "Supergatito.py", (330, 550))
        self.__register("Sopa de letras", "Sopa_de_letras_OAD-3.py", (40, 380))
        self.__register("Ahorcado", "main3.py", (40, 200))

    def __register(self, name: str, entry_file: str, coords: tuple[int, int]):
        self.entries.append(GameEntry(len(self.entries), name, entry_file, coords, self.surface))
        
    def draw(self):
        self.hovered = False
        for entry in self.entries:
            entry.draw()
            if entry.hovered:
                self.hovered = True
            
    def on_screen_click(self):
        for entry in self.entries:
            if entry.hovered:
                entry.on_click()