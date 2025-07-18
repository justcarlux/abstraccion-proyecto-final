import pygame
import math
from constantes import ANCHO, Tipografia, Colores

class Titulo:
    def __init__(self, texto="Hangman Quest"):
        self.texto_completo = texto
        self.fuente = pygame.font.SysFont(Tipografia.FUENTE, Tipografia.TAMAÑO_TITULO, bold=True)
        self.subt_fnt = pygame.font.SysFont(Tipografia.FUENTE, Tipografia.TAMAÑO_SUBTITULO, bold=True)
        self.contador_animacion = 0
        self.letras_mostradas = 0
        self.velocidad_revelado = 3  # letras por segundo

        self.colores = [
            (255, 0, 102),
            (255, 153, 51),
            (255, 255, 0),
            (0, 204, 102),
            (0, 204, 255),
            (51, 102, 255),
            (153, 51, 255),
            (255, 51, 153)
        ]

    def actualizar(self):
        self.contador_animacion += 1
        tiempo_total_seg = self.contador_animacion / 60
        self.letras_mostradas = min(len(self.texto_completo), int(tiempo_total_seg * self.velocidad_revelado))

    def dibujar(self, pantalla):
        self.actualizar()
        offset_y = int(5 * math.sin(self.contador_animacion * 0.05))
        texto_visible = self.texto_completo[:self.letras_mostradas]
        ancho_total = sum(self.fuente.render(l, True, (0, 0, 0)).get_width() for l in texto_visible)
        x_actual = ANCHO // 2 - ancho_total // 2
        y_centro = 350

        for i, letra in enumerate(texto_visible):
            color = self.colores[i % len(self.colores)]
            letra_render = self.fuente.render(letra, True, color)
            sombra = self.fuente.render(letra, True, (30, 30, 30))
            luz = self.fuente.render(letra, True, (255, 255, 255))

            pantalla.blit(luz, (x_actual + 2, y_centro - 2 + offset_y))
            pantalla.blit(sombra, (x_actual + 3, y_centro + 1 + offset_y))
            pantalla.blit(letra_render, (x_actual, y_centro + offset_y))

            x_actual += letra_render.get_width()

        if self.letras_mostradas == len(self.texto_completo):
            if (self.contador_animacion // 30) % 2 == 0:
                subtitulo = self.subt_fnt.render("Presione cualquier tecla para comenzar", True, Colores.BLANCO)
                pantalla.blit(subtitulo, (ANCHO // 2 - subtitulo.get_width() // 2, y_centro + 80))



