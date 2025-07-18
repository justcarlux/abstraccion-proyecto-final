import pygame
import sys
import os
from constantes import ANCHO, ALTO, Colores
from fondo import Fondo
from titulo import Titulo
from botones import BotonesSuperiores
from menu_niveles import MenuNiveles
from ahorcadonivel1 import AhorcadoNivel1
from ahorcadonivel2 import AhorcadoNivel2
from ahorcadonivel3 import AhorcadoNivel3
from ahorcadonivel4 import AhorcadoNivel4
from ahorcadonivel5 import AhorcadoNivel5

# Inicialización
pygame.init()
pygame.mixer.init()

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Hangman Quest")
reloj = pygame.time.Clock()

# Música de fondo
carpeta_sonidos = os.path.join(os.path.dirname(__file__), "sonidos")
ruta_musica = os.path.join(carpeta_sonidos, "sonido.mp3")
if os.path.exists(ruta_musica):
    pygame.mixer.music.load(ruta_musica)
    pygame.mixer.music.set_volume(1.5)
    pygame.mixer.music.play(-1)
else:
    print("⚠️ No se encontró la música de fondo en:", ruta_musica)

# Instancias principales
fondo = Fondo()
titulo = Titulo()
botones_superiores = BotonesSuperiores()
menu_niveles = MenuNiveles()

estado = "menu_principal"  # Estados: menu_principal, menu_niveles, juego
ahorcado = None  # Instancia de juego que crearemos al elegir nivel

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if estado == "menu_principal":
            botones_superiores.manejar_evento(evento)
            if evento.type == pygame.KEYDOWN:
                estado = "menu_niveles"

        elif estado == "menu_niveles":
            nivel_elegido = menu_niveles.manejar_evento(evento)
            if nivel_elegido is not None:
                if nivel_elegido == 1:
                    ahorcado = AhorcadoNivel1(fondo)
                elif nivel_elegido == 2:
                    ahorcado = AhorcadoNivel2(fondo)
                elif nivel_elegido == 3:
                    ahorcado = AhorcadoNivel3(fondo)
                elif nivel_elegido == 4:
                    ahorcado = AhorcadoNivel4(fondo)
                elif nivel_elegido == 5:
                    ahorcado = AhorcadoNivel5(fondo)
                estado = "juego"

        elif estado == "juego":
            resultado = ahorcado.manejar_evento(evento)
            if resultado == "menu_niveles":
                estado = "menu_niveles"
                ahorcado = None

    # Dibujo y actualización
    pantalla.fill(Colores.NEGRO)

    if estado == "menu_principal":
        fondo.dibujar(pantalla)
        titulo.dibujar(pantalla)
        botones_superiores.dibujar(pantalla)

    elif estado == "menu_niveles":
        fondo.dibujar(pantalla)
        menu_niveles.dibujar(pantalla)

    elif estado == "juego":
        ahorcado.actualizar(pantalla)
        ahorcado.dibujar(pantalla)

    pygame.display.flip()
    reloj.tick(60)





