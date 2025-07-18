import pygame
import os
from constantes import ANCHO, ALTO, Colores

class MenuNiveles:
    """
    Menú interactivo para seleccionar niveles, con botones y texto.
    El fondo debe ser pintado antes de llamar a dibujar().
    """

    def __init__(self):
        self.fuente = pygame.font.SysFont("Comic Sans MS", 23, bold=True)
        self.botones = [
            {"texto": "Nivel 1: Colores", "nivel": 1, "rect": pygame.Rect(0, 0, 400, 60)},
            {"texto": "Nivel 2: Frutas y Verduras", "nivel": 2, "rect": pygame.Rect(0, 0, 400, 60)},
            {"texto": "Nivel 3: Animales", "nivel": 3, "rect": pygame.Rect(0, 0, 400, 60)},
            {"texto": "Nivel 4: Deportes", "nivel": 4, "rect": pygame.Rect(0, 0, 400, 60)},
            {"texto": "Nivel 5: Programacion", "nivel": 5, "rect": pygame.Rect(0, 0, 400, 60)},
        ]
        self.posicionar_botones()

        # Cargar sonido botón (usar ruta segura)
        ruta_sonido = os.path.join(os.path.dirname(__file__), "sonidos", "sonidodeboton.mp3")
        self.sonido_boton = pygame.mixer.Sound(ruta_sonido)

    def posicionar_botones(self):
        espacio_total = len(self.botones) * 70  # Ajustado para que no queden muy pegados
        inicio_y = (ALTO - espacio_total) // 2
        for i, boton in enumerate(self.botones):
            boton["rect"].center = (ANCHO // 2, inicio_y + i * 70)

    def dibujar(self, pantalla):
        # No pintamos fondo sólido aquí, se debe pintar antes
        # Dibujamos título
        titulo = self.fuente.render("Selecciona un Nivel", True, Colores.BLANCO)
        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 60))

        # Dibujamos botones
        for boton in self.botones:
            pygame.draw.rect(pantalla, Colores.AZUL_OSCURO, boton["rect"], border_radius=10)
            texto = self.fuente.render(boton["texto"], True, Colores.BLANCO)
            texto_rect = texto.get_rect(center=boton["rect"].center)
            pantalla.blit(texto, texto_rect)

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for boton in self.botones:
                if boton["rect"].collidepoint(evento.pos):
                    self.sonido_boton.play()  # Reproducir sonido al presionar cualquier botón
                    return boton["nivel"]
        return None

