import pygame
import sys
import random
import math
import os

# Inicialización pygame
pygame.init()

# Configuración de sonido (corregida)
try:
    pygame.mixer.init()
    pygame.mixer.music.load("Sonido_fondo.mp3.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    sonido_click = pygame.mixer.Sound("Sonido_click.wav.wav")
    sonidos_disponibles = True
except pygame.error as e:
    sonidos_disponibles = False
    print(f"No se encontraron archivos de sonido: {e}. El juego continuará sin sonido")

# Dimensiones y colores
ANCHO, ALTO = 1200, 720
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
ROJO = (255, 50, 50)
AMARILLO = (255, 255, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
NARANJA = (255, 165, 0)

# Clase principal del juego
class LucesApagadas:
    def __init__(self):
        self.ANCHO, self.ALTO = ANCHO, ALTO
        self.pantalla = pygame.display.set_mode((self.ANCHO, self.ALTO))
        pygame.display.set_caption("Luces Apagadas")

        # Variables del juego
        self.TAM_CUADRICULA = 5
        self.COLOR_CELDA = BLANCO
        self.FORMA_CELDA = "cuadrado"
        self.tiempo_limite = 60
        self.tiempo_restante = self.tiempo_limite
        self.inicio_tiempo = 0
        self.clics = 0
        self.tiempo_total = 0
        self.pausado = False
        self.sonido_activado = True if sonidos_disponibles else False

        # Inicializar componentes del juego
        self.actualizar_tamanos()
        self.cuadricula = self.crear_cuadricula(self.TAM_CUADRICULA)

        # Estados del juego
        self.estados = {
            "menu": MenuState(self),
            "jugando": JugandoState(self),
            "configurar": ConfigurarState(self),
            "reglas": ReglasState(self),
            "pausa": PausaState(self),
            "ganaste": GanasteState(self),
            "tiempo_agotado": TiempoAgotadoState(self)
        }
        self.estado_actual = "menu"

    def actualizar_tamanos(self):
        self.TAM_CELDA = min(self.ANCHO - 40, self.ALTO - 150) // self.TAM_CUADRICULA
        self.margen_x = (self.ANCHO - self.TAM_CUADRICULA * self.TAM_CELDA) // 2
        self.margen_y = (self.ALTO - 100 - self.TAM_CUADRICULA * self.TAM_CELDA) // 2
        self.ALTO_AREA_BOTONES = self.ALTO - 100

    def crear_cuadricula(self, tam):
        return [[random.choice([True, False]) for _ in range(tam)] for _ in range(tam)]

    def alternar_vecinas(self, x, y):
        coordenadas = [(x, y), (x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        for i, j in coordenadas:
            if 0 <= i < self.TAM_CUADRICULA and 0 <= j < self.TAM_CUADRICULA:
                self.cuadricula[i][j] = not self.cuadricula[i][j]

    def verificar_victoria(self):
        return all(not celda for fila in self.cuadricula for celda in fila)

    def cambiar_estado(self, nuevo_estado):
        self.estado_actual = nuevo_estado

    def ejecutar(self):
        while True:
            estado = self.estados[self.estado_actual]
            estado.manejar_eventos()
            estado.dibujar()
            pygame.display.flip()

# Clase base EstadoJuego
class EstadoJuego:
    def __init__(self, juego):
        self.juego = juego

    def manejar_eventos(self):
        pass

    def dibujar(self):
        pass

# Implementación de estados
class MenuState(EstadoJuego):
    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if self.juego.ANCHO // 2 - 150 <= mouse_x <= self.juego.ANCHO // 2 + 150 and 200 <= mouse_y <= 250:
                    self.juego.cambiar_estado("jugando")
                    self.juego.cuadricula = self.juego.crear_cuadricula(self.juego.TAM_CUADRICULA)
                    self.juego.inicio_tiempo = pygame.time.get_ticks()
                    self.juego.clics = 0
                    self.juego.tiempo_total = 0

                elif self.juego.ANCHO // 2 - 150 <= mouse_x <= self.juego.ANCHO // 2 + 150 and 270 <= mouse_y <= 320:
                    self.juego.cambiar_estado("reglas")

                elif self.juego.ANCHO // 2 - 150 <= mouse_x <= self.juego.ANCHO // 2 + 150 and 340 <= mouse_y <= 390:
                    self.juego.cambiar_estado("configurar")

                elif self.juego.ANCHO // 2 - 150 <= mouse_x <= self.juego.ANCHO // 2 + 150 and 410 <= mouse_y <= 460:
                    pygame.quit()
                    sys.exit()

                elif self.juego.ANCHO - 120 <= mouse_x <= self.juego.ANCHO - 20 and 20 <= mouse_y <= 50 and sonidos_disponibles:
                    self.juego.sonido_activado = not self.juego.sonido_activado
                    volumen = 0.5 if self.juego.sonido_activado else 0.0
                    pygame.mixer.music.set_volume(volumen)

    def dibujar(self):
        fondo = pygame.image.load("fondo_menu.png")
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
        self.juego.pantalla.blit(fondo, (0, 0))

        # Define título y fuente
        fuente = pygame.font.Font(None, 50)

        botones = [("Jugar", 200), ("Reglas y Información", 270), ("Configurar", 340), ("Salir", 410)]
        for texto, y in botones:
            btn = fuente.render(texto, True, NEGRO)
            pygame.draw.rect(self.juego.pantalla, BLANCO, (self.juego.ANCHO // 2 - 175, y, 355, 50))
            self.juego.pantalla.blit(btn, (self.juego.ANCHO // 2 - btn.get_width() // 2, y + 10))

        if sonidos_disponibles:
            fuente_sonido = pygame.font.Font(None, 30)
            texto_sonido = fuente_sonido.render("Sonido: ON" if self.juego.sonido_activado else "Sonido: OFF", True, NEGRO)
            pygame.draw.rect(self.juego.pantalla, BLANCO, (self.juego.ANCHO - 120, 20, 120, 30))
            self.juego.pantalla.blit(texto_sonido, (self.juego.ANCHO - 110, 20))


class ConfigurarState(EstadoJuego):
    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Control de tiempo límite (-10 segundos)
                if (self.juego.ANCHO // 2 - 120 <= mouse_x <= self.juego.ANCHO // 2 - 70 and 
                    130 <= mouse_y <= 180):
                    if self.juego.tiempo_limite > 10:
                        self.juego.tiempo_limite -= 10
                        if self.juego.sonido_activado and sonidos_disponibles:
                            sonido_click.play()

                # Control de tiempo límite (+10 segundos)
                elif (self.juego.ANCHO // 2 + 70 <= mouse_x <= self.juego.ANCHO // 2 + 120 and 
                    130 <= mouse_y <= 180):
                    if self.juego.tiempo_limite < 300:
                        self.juego.tiempo_limite += 10
                        if self.juego.sonido_activado and sonidos_disponibles:
                            sonido_click.play()

                # Control de tamaño del tablero (-1 tamaño)
                elif (self.juego.ANCHO // 2 - 120 <= mouse_x <= self.juego.ANCHO // 2 - 70 and 
                    270 <= mouse_y <= 320):
                    if self.juego.TAM_CUADRICULA > 3:
                        self.juego.TAM_CUADRICULA -= 1
                        self.juego.actualizar_tamanos()
                        if self.juego.sonido_activado and sonidos_disponibles:
                            sonido_click.play()

                # Control de tamaño del tablero (+1 tamaño)
                elif (self.juego.ANCHO // 2 + 70 <= mouse_x <= self.juego.ANCHO // 2 + 120 and 
                    270 <= mouse_y <= 320):
                    if self.juego.TAM_CUADRICULA < 5:
                        self.juego.TAM_CUADRICULA += 1
                        self.juego.actualizar_tamanos()
                        if self.juego.sonido_activado and sonidos_disponibles:
                            sonido_click.play()

                # Selección de forma cuadrada
                elif (self.juego.ANCHO // 2 - 120 <= mouse_x <= self.juego.ANCHO // 2 - 20 and 
                    380 <= mouse_y <= 420):
                    self.juego.FORMA_CELDA = "cuadrado"
                    if self.juego.sonido_activado and sonidos_disponibles:
                        sonido_click.play()

                # Selección de forma circular
                elif (self.juego.ANCHO // 2 + 20 <= mouse_x <= self.juego.ANCHO // 2 + 120 and 
                    380 <= mouse_y <= 420):
                    self.juego.FORMA_CELDA = "circulo"
                    if self.juego.sonido_activado and sonidos_disponibles:
                        sonido_click.play()

                # Control de color de celdas
                colores = [BLANCO, ROJO, AMARILLO, AZUL, VERDE, NARANJA]
                for i, color in enumerate(colores):
                    x = self.juego.ANCHO // 2 - 140 + (i % 3) * 100
                    y = 470 if i < 3 else 530
                    if (x <= mouse_x <= x + 80 and y <= mouse_y <= y + 40):
                        self.juego.COLOR_CELDA = color
                        if self.juego.sonido_activado and sonidos_disponibles:
                            sonido_click.play()

                # Botón para volver al menú
                if (self.juego.ANCHO // 2 - 75 <= mouse_x <= self.juego.ANCHO // 2 + 75 and 
                    600 <= mouse_y <= 650):
                    self.juego.cambiar_estado("menu")

    def dibujar(self):
        fondo = pygame.image.load("fondo_configuracion.png")
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
        self.juego.pantalla.blit(fondo, (0, 0))

        # Título de configuración
        fuente = pygame.font.Font(None, 36)
        fuente_pequena = pygame.font.Font(None, 24)
        texto_titulo = fuente.render("Configuración del Juego", True, BLANCO)
        self.juego.pantalla.blit(texto_titulo, (self.juego.ANCHO // 2 - texto_titulo.get_width() // 2, 30))

        # Configuración de tiempo límite
        texto_tiempo = fuente.render(f"Tiempo límite: {self.juego.tiempo_limite} s", True, BLANCO)
        self.juego.pantalla.blit(texto_tiempo, (self.juego.ANCHO // 2 - texto_tiempo.get_width() // 2, 80))

        # Botones -/+ para tiempo
        menos_t = fuente.render("-", True, NEGRO)
        mas_t = fuente.render("+", True, NEGRO)
        pygame.draw.rect(self.juego.pantalla, BLANCO, (self.juego.ANCHO // 2 - 120, 130, 50, 50))
        self.juego.pantalla.blit(menos_t, (self.juego.ANCHO // 2 - 110, 135))
        pygame.draw.rect(self.juego.pantalla, BLANCO, (self.juego.ANCHO // 2 + 70, 130, 50, 50))
        self.juego.pantalla.blit(mas_t, (self.juego.ANCHO // 2 + 85, 135))

        # Configuración de tamaño del tablero
        texto_tamano = fuente.render(f"Tamaño tablero: {self.juego.TAM_CUADRICULA}x{self.juego.TAM_CUADRICULA}", True, BLANCO)
        self.juego.pantalla.blit(texto_tamano, (self.juego.ANCHO // 2 - texto_tamano.get_width() // 2, 220))

        # Botones -/+ para tamaño
        menos_s = fuente.render("-", True, NEGRO)
        mas_s = fuente.render("+", True, NEGRO)
        pygame.draw.rect(self.juego.pantalla, BLANCO, (self.juego.ANCHO // 2 - 120, 270, 50, 50))
        self.juego.pantalla.blit(menos_s, (self.juego.ANCHO // 2 - 110, 275))
        pygame.draw.rect(self.juego.pantalla, BLANCO, (self.juego.ANCHO // 2 + 70, 270, 50, 50))
        self.juego.pantalla.blit(mas_s, (self.juego.ANCHO // 2 + 85, 275))

        # Indicación de opciones de tamaño
        texto_opciones = fuente_pequena.render("(3x3, 4x4 o 5x5)", True, BLANCO)
        self.juego.pantalla.blit(texto_opciones, (self.juego.ANCHO // 2 - texto_opciones.get_width() // 2, 310))

        # Configuración de forma de celdas
        texto_forma = fuente.render(f"Forma celdas: {self.juego.FORMA_CELDA}", True, BLANCO)
        self.juego.pantalla.blit(texto_forma, (self.juego.ANCHO // 2 - texto_forma.get_width() // 2, 340))

        # Botones para selección de forma
        pygame.draw.rect(self.juego.pantalla, BLANCO, (self.juego.ANCHO // 2 - 120, 380, 130, 40))
        self.juego.pantalla.blit(fuente.render("Cuadrado", True, NEGRO), (self.juego.ANCHO // 2 - 110, 385))

        pygame.draw.rect(self.juego.pantalla, BLANCO, (self.juego.ANCHO // 2 + 20, 380, 100, 40))
        self.juego.pantalla.blit(fuente.render("Círculo", True, NEGRO), (self.juego.ANCHO // 2 + 30, 385))

        # Configuración de color de celdas
        texto_color = fuente.render("Color celdas:", True, BLANCO)
        self.juego.pantalla.blit(texto_color, (self.juego.ANCHO // 2 - texto_color.get_width() // 2, 440))

        # Mostrar opciones de colores
        colores = [BLANCO, ROJO, AMARILLO, AZUL, VERDE, NARANJA]
        nombres_colores = ["Blanco", "Rojo", "Amarillo", "Azul", "Verde", "Naranja"]

        for i, (color, nombre) in enumerate(zip(colores, nombres_colores)):
            x = self.juego.ANCHO // 2 - 140 + (i % 3) * 100
            y = 470 if i < 3 else 530
            pygame.draw.rect(self.juego.pantalla, color, (x, y, 80, 40))
            pygame.draw.rect(self.juego.pantalla, NEGRO, (x, y, 80, 40), 2)  # Borde

            # Resaltar el color seleccionado
            if color == self.juego.COLOR_CELDA:
                pygame.draw.rect(self.juego.pantalla, BLANCO, (x, y, 80, 40), 4)     

         # Dibujar botón para volver al menú
        pygame.draw.rect(self.juego.pantalla, BLANCO, (self.juego.ANCHO // 2 - 75, 600, 150, 50))
        texto_volver = fuente.render("Volver", True, NEGRO)
        self.juego.pantalla.blit(texto_volver, (self.juego.ANCHO // 2 - texto_volver.get_width() // 2, 610))  

class JugandoState(EstadoJuego):
    def manejar_eventos(self):
        if not self.juego.pausado:
            transcurrido = (pygame.time.get_ticks() - self.juego.inicio_tiempo) / 1000
            self.juego.tiempo_restante = self.juego.tiempo_limite - transcurrido

            if self.juego.tiempo_restante <= 0:
                self.juego.tiempo_total = self.juego.tiempo_limite
                self.juego.cambiar_estado("tiempo_agotado")

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Botón Reiniciar
                if 50 <= mouse_x <= 250 and self.juego.ALTO_AREA_BOTONES <= mouse_y <= self.juego.ALTO_AREA_BOTONES + 40:
                    self.juego.cuadricula = self.juego.crear_cuadricula(self.juego.TAM_CUADRICULA)
                    self.juego.inicio_tiempo = pygame.time.get_ticks()
                    self.juego.clics = 0

                # Botón Menú
                elif 350 <= mouse_x <= 550 and self.juego.ALTO_AREA_BOTONES <= mouse_y <= self.juego.ALTO_AREA_BOTONES + 40:
                    self.juego.cambiar_estado("menu")

                # Botón Pausa
                elif 230 <= mouse_x <= 330 and self.juego.ALTO_AREA_BOTONES <= mouse_y <= self.juego.ALTO_AREA_BOTONES + 40:
                    self.juego.pausado = True
                    self.juego.cambiar_estado("pausa")

                # Interacción con el tablero
                else:
                    fila = (mouse_x - self.juego.margen_x) // self.juego.TAM_CELDA
                    columna = (mouse_y - self.juego.margen_y) // self.juego.TAM_CELDA
                    if 0 <= fila < self.juego.TAM_CUADRICULA and 0 <= columna < self.juego.TAM_CUADRICULA:
                        if self.juego.sonido_activado and sonidos_disponibles:
                            sonido_click.play()
                        self.juego.alternar_vecinas(fila, columna)
                        self.juego.clics += 1
                        if self.juego.verificar_victoria():
                            self.juego.cambiar_estado("ganaste")
                            self.juego.tiempo_total = self.juego.tiempo_limite - self.juego.tiempo_restante

    def dibujar(self):
        fondo = pygame.image.load("fondo_configuracion.png") 
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))                 
        self.juego.pantalla.blit(fondo, (0, 0))

        # Dibujar cuadrícula
        for x in range(self.juego.TAM_CUADRICULA):
            for y in range(self.juego.TAM_CUADRICULA):
                rect = pygame.Rect(
                    self.juego.margen_x + x * self.juego.TAM_CELDA, 
                    self.juego.margen_y + y * self.juego.TAM_CELDA, 
                    self.juego.TAM_CELDA, 
                    self.juego.TAM_CELDA
                )

                color = self.juego.COLOR_CELDA if self.juego.cuadricula[x][y] else NEGRO
                if self.juego.FORMA_CELDA == "cuadrado":
                    pygame.draw.rect(self.juego.pantalla, color, rect)
                elif self.juego.FORMA_CELDA == "circulo":
                    pygame.draw.circle(self.juego.pantalla, color, rect.center, self.juego.TAM_CELDA // 2)

                pygame.draw.rect(self.juego.pantalla, GRIS, rect, 1)  # Borde

        # Mostrar información del juego
        fuente = pygame.font.Font(None, 36)
        texto_tiempo = fuente.render(f"Tiempo: {max(0, int(self.juego.tiempo_restante))}", True, BLANCO)
        self.juego.pantalla.blit(texto_tiempo, (10, self.juego.ALTO - 40))

        # Dibujar botones inferiores
        fuente_boton = pygame.font.Font(None, 40)
        pygame.draw.rect(self.juego.pantalla, GRIS, (50, self.juego.ALTO_AREA_BOTONES, 200, 40))
        pygame.draw.rect(self.juego.pantalla, GRIS, (350, self.juego.ALTO_AREA_BOTONES, 200, 40))
        pygame.draw.rect(self.juego.pantalla, GRIS, (230, self.juego.ALTO_AREA_BOTONES, 140, 40))

        self.juego.pantalla.blit(fuente_boton.render("Reiniciar", True, NEGRO), (100, self.juego.ALTO_AREA_BOTONES + 5))
        self.juego.pantalla.blit(fuente_boton.render("Menú", True, NEGRO), (400, self.juego.ALTO_AREA_BOTONES + 5))
        self.juego.pantalla.blit(fuente_boton.render("Pausa", True, NEGRO), (260, self.juego.ALTO_AREA_BOTONES + 5))

class ReglasState(EstadoJuego):
    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                self.juego.cambiar_estado("menu")
    
    def dibujar(self):
        fondo = pygame.image.load("reglas.png") 
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))                 
        self.juego.pantalla.blit(fondo, (0, 0))
        

class PausaState(EstadoJuego):
    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                self.juego.pausado = False
                self.juego.inicio_tiempo = pygame.time.get_ticks() - int((self.juego.tiempo_limite - self.juego.tiempo_restante) * 1000)
                self.juego.cambiar_estado("jugando")

    def dibujar(self):
        fondo = pygame.image.load("fondo_configuracion.png") 
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))                 
        self.juego.pantalla.blit(fondo, (0, 0))
        fuente = pygame.font.Font(None, 60)
        texto = fuente.render("Juego en pausa", True,BLANCO)
        self.juego.pantalla.blit(texto, (self.juego.ANCHO // 2 - texto.get_width() // 2, self.juego.ALTO // 2 - 40))
        sub = pygame.font.Font(None, 30)
        self.juego.pantalla.blit(sub.render("Haz clic para continuar", True,BLANCO), 
                               (self.juego.ANCHO // 2 - 120, self.juego.ALTO // 2 + 30))

class GanasteState(EstadoJuego):
    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                self.juego.cambiar_estado("menu")

    def dibujar(self):
        fondo = pygame.image.load("fondo_ganaste.png") 
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))                 
        self.juego.pantalla.blit(fondo, (0, 0))
        fuente = pygame.font.Font(None, 60)
        sub = pygame.font.Font(None, 30)
        self.juego.pantalla.blit(sub.render(f"Clics: {self.juego.clics}", True, BLANCO), 
                     (self.juego.ANCHO // 2 - 50, self.juego.ALTO // 2 - 110))
        self.juego.pantalla.blit(sub.render(f"Tiempo usado: {int(self.juego.tiempo_total)}s", True, BLANCO), 
                     (self.juego.ANCHO // 2 - 100, self.juego.ALTO // 2 + 140))
        self.juego.pantalla.blit(sub.render("Haz clic para volver al menú", True,BLANCO), 
                     (self.juego.ANCHO // 2 - 130, self.juego.ALTO // 2 + 170))

class TiempoAgotadoState(EstadoJuego):
    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                self.juego.cambiar_estado("menu")

    def dibujar(self):
        fondo = pygame.image.load("fondo_configuracion.png") 
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))                 
        self.juego.pantalla.blit(fondo, (0, 0))
        fuente = pygame.font.Font(None, 60)
        self.juego.pantalla.blit(fuente.render("¡Tiempo agotado!", True, BLANCO), 
                     (self.juego.ANCHO // 2 - 180, self.juego.ALTO // 2 - 90))
        sub = pygame.font.Font(None, 30)
        self.juego.pantalla.blit(sub.render(f"Clics: {self.juego.clics}", True, BLANCO), 
                     (self.juego.ANCHO // 2 - 50, self.juego.ALTO // 2 - 20))
        self.juego.pantalla.blit(sub.render(f"Tiempo usado: {int(self.juego.tiempo_total)}s", True, BLANCO), 
                     (self.juego.ANCHO // 2 - 100, self.juego.ALTO // 2 + 20))
        self.juego.pantalla.blit(sub.render("Haz clic para volver al menú", True, BLANCO), 
                     (self.juego.ANCHO // 2 - 140, self.juego.ALTO // 2 + 60))



# Punto de entrada principal del programa
if __name__ == "__main__":
    juego = LucesApagadas()
    juego.ejecutar()