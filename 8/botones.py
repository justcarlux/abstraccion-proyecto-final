import pygame
import sys
import os
from constantes import Colores, Tipografia, ANCHO, ALTO

class BotonesSuperiores:
    def __init__(self):
        self.fuente = pygame.font.SysFont(Tipografia.FUENTE, Tipografia.TAMAÑO_BOTONES, bold=True)
        self.botones = {
            "Instrucciones": pygame.Rect(100, 20, 140, 40),
            "Reglas": pygame.Rect(400, 20, 140, 40),
            "Objetivo": pygame.Rect(700, 20, 140, 40),
            "Salir": pygame.Rect(1100, 20, 140, 40)
        }
        self.textos = {
            "Instrucciones": "Usa el teclado para adivinar letras, tienes un número limitado de intentos.",
            "Reglas": "No se permiten números, cada error dibuja una parte del personaje ahorcado.",
            "Objetivo": "Adivinar la palabra correcta antes de que se complete el dibujo del ahorcado.",
        }
        self.boton_activo = None

        # Ruta correcta para el sonido relativo al archivo actual
        carpeta_sonidos = os.path.join(os.path.dirname(__file__), "sonidos")
        ruta_sonido = os.path.join(carpeta_sonidos, "sonidodeboton.mp3")
        self.sonido_boton = pygame.mixer.Sound(ruta_sonido)

    def dibujar(self, pantalla):
        for nombre, rect in self.botones.items():
            color = Colores.VERDE_CLARO if self.boton_activo == nombre else Colores.AZUL
            pygame.draw.rect(pantalla, color, rect, border_radius=8)
            texto = self.fuente.render(nombre, True, Colores.BLANCO)
            pantalla.blit(texto, (rect.centerx - texto.get_width() // 2, rect.centery - texto.get_height() // 2))
        if self.boton_activo in self.textos:
            self._dibujar_ventana_info(pantalla, self.boton_activo)

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for nombre, rect in self.botones.items():
                if rect.collidepoint(evento.pos):
                    self.sonido_boton.play()  # Sonido al presionar cualquier botón

                    if nombre == "Salir":
                        pygame.quit()
                        sys.exit()

                    if self.boton_activo == nombre:
                        self.boton_activo = None
                    elif nombre in self.textos:
                        self.boton_activo = nombre
                    return
            self.boton_activo = None

    def _dibujar_ventana_info(self, pantalla, tipo):
        ancho, alto = 530, 100
        x = ANCHO // 2 - ancho // 2
        y = ALTO // 2 - 125
        pygame.draw.rect(pantalla, Colores.GRIS_OSCURO, (x, y, ancho, alto), border_radius=10)
        pygame.draw.rect(pantalla, Colores.BLANCO, (x, y, ancho, alto), 2, border_radius=10)
        font_titulo = pygame.font.SysFont(Tipografia.FUENTE, Tipografia.TAMAÑO_TITULO_VENTANA, bold=True)
        font_cuerpo = pygame.font.SysFont(Tipografia.FUENTE, Tipografia.TAMAÑO_CUERPO_VENTANA)
        titulo = font_titulo.render(tipo, True, Colores.BLANCO)
        cuerpo = font_cuerpo.render(self.textos[tipo], True, (230, 230, 230))
        pantalla.blit(titulo, (x + 20, y + 15))
        pantalla.blit(cuerpo, (x + 20, y + 60))







