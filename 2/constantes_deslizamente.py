import pygame
pygame.init()

#Dimensiones de la ventana
ANCHO = 1280
ALTO = 720

#colores utilizados
NEGRO = (0,0,0)
GRIS = (54,48,48)
GRIS_CLARO = (221, 221, 221)
BLANCO = (255, 255, 255)
VERDE = (0, 180, 0)
VERDE_CAMBIO = (0, 173, 0)
ROJO = (200, 0, 0) 
AZUL = (0,0, 200)
AZUL_CAMBIO = (7, 7, 182)
AZUL_CLARO = (51, 221, 255)
ROJO_CAMBIO = (211, 0, 0)
AMARILLO = (255, 255, 51)

#Imagenes para los rompecabezas
imagenes = []
for i in range(8):
    imagen = pygame.image.load(f"imagen{i+1}.jpg")
    imagenes.append(imagen)
    

INSTRUCCIONES = [
            "→ Haz click en 'Jugar' en el menú principal.",
            "→ Luego selecciona el modo de juego, la dificultad y la imagen que te gustaría armar.",
            "→ Una vez iniciado el juego, haz click en la pieza del rompecabezas que deseas mover,\n siempre que tenga una pieza libre a su lado.",
            "→ La pieza seleccionada se moverá al espacio vacío, dejando libre su posición anterior.",
            "→ Mueve todas las piezas hasta armar la imagen original para ganar la partida."
        ]

pygame.quit()