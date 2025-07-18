import pygame
import sys
import random
from typing import List, Tuple
import time

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
AZUL = (100, 100, 255)

ANCHO, ALTO = 1280, 720

pygame.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Sopa de Letras")
fuente = pygame.font.SysFont(None, 65)
fuente_peque = pygame.font.SysFont(None, 55)

# Cambia la fuente para la sopa de letras a Times New Roman
fuente_sopa = pygame.font.SysFont('Times New Roman', 36)
fuente_sopa_facil = pygame.font.SysFont('Times New Roman', 60)
fuente_sopa_media = pygame.font.SysFont('Times New Roman', 40)
fuente_sopa_dificil = pygame.font.SysFont('Times New Roman', 25)

activo = True

class SopaDeLetras:
    def __init__(self, filas, columnas):
        self.filas = 0
        self.columnas = 0
        self.palabras_facil = ["SOL","MAR","RÍO","PEZ","REY","AGUA","FIN","TREN","LUNA",
                               "PAN","FLOR","CASA","UÑA","OJO","PAZ","OSO","DÍA","MES","AÑO","SAL","MESA","VOZ","LUZ","CAMA"]
        self.palabras_medio = ["CABALLO","CONEJO","BALLENA","JIRAFA","ZORRO","VENTANA","ELEFANTE","PINTURA","MÚSICA",
                               "PUMA","LEÓN","GALLINA","MORADO","DELFÍN","NUBES","VIAJAR","CANTAR","PANDA","ZEBRA","LIBRO","CARRO","MONEDA","AGUA","ÁRBOL","SUEÑO","LENTO", "DULCE","FAMILIA","CABELLO","JARDÍN"]
        self.palabras_dificil = ["CORAZÓN","ESTRELLA","CHOCOLATE","TELÉFONO","ZANAHORIA","GUITARRA","ATARDECER","ESTUDIANTE","RECTÁNGULO",
                               "CIRCULO","AUTOBÚS","FERROCARIL","ESPEJO","ZAPATO","PLANETA","LINTERNA","FLORERO","ANUNCIO","TORTA","CAMINAR","ESPADA","FELICIDAD","HISTORIA","ENERGÍA","BATERÍA","IGLESIA"]
        # Direcciones: (fila, columna)
        self.direcciones = [
            (0, 1),   # → Horizontal derecha
            (1, 0),   # ↓ Vertical abajo
            (1, 1),   # ↘ Diagonal principal
            (-1, 0),  # ↑ Vertical arriba
            (0, -1),  # ← Horizontal izquierda
            (-1, -1), # ↖ Diagonal invertidas
            (-1, 1),  # ↗ Diagonal superior derecha
            (1, -1)   # ↙ Diagonal inferior izquierda
        ]
        self.palabras_en_sopa = []
        self.direcciones_usadas = []
        
    def posicion_valida(self, fila, col, letra):
        
        if fila < 0 or fila >= self.filas or col < 0 or col >= self.columnas:
            return False
        return self.sopa[fila][col] == ' ' or self.sopa[fila][col] == letra

    def colocar_palabra(self, palabra, direcciones):
        
        palabra = palabra.upper()
        max_intentos = 100

        for _ in range(max_intentos):
            dir_fila, dir_col = random.choice(direcciones)
            
            # función implementada para solucionar el problema de la busqueda de las palabras escondidas
        
            if dir_fila == 1:
                max_fila = self.filas - len(palabra)
            elif dir_fila == -1:
                max_fila = len(palabra) - 1
            else:
                max_fila = self.filas - 1

            if dir_col == 1:
                max_col = self.columnas - len(palabra)
            elif dir_col == -1:
                max_col = len(palabra) - 1
            else:
                max_col = self.columnas - 1

            if max_fila < 0 or max_col < 0:
                continue 

            fila = random.randint(0, max_fila) if max_fila > 0 else 0
            col = random.randint(0, max_col) if max_col > 0 else 0

        
            valido = True
            for i in range(len(palabra)):
                nueva_fila = fila + dir_fila * i
                nueva_col = col + dir_col * i
                if not self.posicion_valida(nueva_fila, nueva_col, palabra[i]):
                    valido = False
                    break

            if valido:
            
                for i in range(len(palabra)):
                    nueva_fila = fila + dir_fila * i
                    nueva_col = col + dir_col * i
                    self.sopa[nueva_fila][nueva_col] = palabra[i]
                return True  

        return False  
    
    def Dificultad(self, dificultad):
        if dificultad == "facil":
            # Solo horizontal (→) y diagonal (↘)
            direcciones = [self.direcciones[0], self.direcciones[2]]
            self.direcciones_usadas = direcciones
            self.filas, self.columnas = 5, 5
            self.sopa = [[' ' for _ in range(self.columnas)] for _ in range(self.filas)]
            palabras = random.sample(self.palabras_facil, 4)
            self.palabras_en_sopa = palabras
            self.generar_sopa(palabras, direcciones)
        elif dificultad == "media":
            # Horizontal (→, ←), vertical (↓, ↑), diagonal (↘, ↖)
            direcciones = [self.direcciones[0], self.direcciones[1], self.direcciones[2], self.direcciones[3], self.direcciones[4], self.direcciones[5]]
            self.direcciones_usadas = direcciones
            self.filas, self.columnas = 10, 10
            self.sopa = [[' ' for _ in range(self.columnas)] for _ in range(self.filas)]
            palabras = random.sample(self.palabras_medio, 6)
            self.palabras_en_sopa = palabras
            self.generar_sopa(palabras, direcciones)
        elif dificultad == "dificil":
            # Todas las direcciones
            direcciones = self.direcciones
            self.direcciones_usadas = direcciones
            self.filas, self.columnas = 15, 15
            self.sopa = [[' ' for _ in range(self.columnas)] for _ in range(self.filas)]
            palabras = random.sample(self.palabras_dificil, 9)
            self.palabras_en_sopa = palabras
            self.generar_sopa(palabras, direcciones)
            

    def rellenar_espacios_vacios(self):
        
        for f in range(self.filas):
            for c in range(self.columnas):
                if self.sopa[f][c] == ' ':
                    self.sopa[f][c] = random.choice('AÁÍÓÚÉBCDEFGHIJKLMNOPQRSTUVWXYZ')

    def generar_sopa(self, palabras: List[str], direcciones):
        print(palabras)
        
        for palabra in palabras:
            self.colocar_palabra(palabra, direcciones)
        self.rellenar_espacios_vacios()

# Cargar y redimensionar imágenes
menu_img = pygame.image.load('imagenes/menu.png')
menu_img = pygame.transform.scale(menu_img, (ANCHO, ALTO))
niveles_img = pygame.image.load('imagenes/niveles.jpg')
niveles_img = pygame.transform.scale(niveles_img, (ANCHO, ALTO))

# Cargar imágenes de los botones de nivel en tamaño completo
facil_img = pygame.image.load('imagenes/facil.png')
facil_img = pygame.transform.scale(facil_img, (ANCHO, ALTO))
normal_img = pygame.image.load('imagenes/normal.png')
normal_img = pygame.transform.scale(normal_img, (ANCHO, ALTO))
dificil_img = pygame.image.load('imagenes/dificil.jpg')
dificil_img = pygame.transform.scale(dificil_img, (ANCHO, ALTO))

# Cargar las imágenes de las ventanas de nivel
nivel_facil_img = pygame.image.load('imagenes/nivel_facil.png')
nivel_facil_img = pygame.transform.scale(nivel_facil_img, (ANCHO, ALTO))
nivel_normal_img = pygame.image.load('imagenes/nivel_normal.png')
nivel_normal_img = pygame.transform.scale(nivel_normal_img, (ANCHO, ALTO))
nivel_dificil_img = pygame.image.load('imagenes/nivel_dificil.png')
nivel_dificil_img = pygame.transform.scale(nivel_dificil_img, (ANCHO, ALTO))

def menu_principal():
    rect_play = pygame.Rect(200, 570, 880, 100)
    rect_cerrar = pygame.Rect(40, 40, 100, 100)
    while True:
        ventana.blit(menu_img, (0, 0))
        # pygame.draw.rect(ventana, (255,0,0), rect_play, 3) 
        # pygame.draw.rect(ventana, (0,255,0), rect_cerrar, 3)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_play.collidepoint(event.pos):
                    seleccionar_nivel()
                if rect_cerrar.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def seleccionar_nivel():
    # Definir áreas de los botones de nivel y volver para 1280x720
    rect_facil = pygame.Rect(150, 500, 350, 140)
    rect_normal = pygame.Rect(480, 500, 350, 140)
    rect_dificil = pygame.Rect(880, 500, 350, 140)
    rect_volver = pygame.Rect(40, 40, 100, 100)
    while True:
        pos_mouse = pygame.mouse.get_pos()
        # Mostrar imagen de fondo según el hover
        if rect_facil.collidepoint(pos_mouse):
            ventana.blit(facil_img, (0, 0))
        elif rect_normal.collidepoint(pos_mouse):
            ventana.blit(normal_img, (0, 0))
        elif rect_dificil.collidepoint(pos_mouse):
            ventana.blit(dificil_img, (0, 0))
        else:
            ventana.blit(niveles_img, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_facil.collidepoint(event.pos):
                    jugar_sopa("facil")
                if rect_normal.collidepoint(event.pos):
                    jugar_sopa("media")
                if rect_dificil.collidepoint(event.pos):
                    jugar_sopa("dificil")
                if rect_volver.collidepoint(event.pos):
                    return

def es_seleccion_valida(seleccion, direcciones_permitidas):
    if len(seleccion) < 2:
        return False, None
    f0, c0 = seleccion[0]
    f1, c1 = seleccion[-1]
    df = f1 - f0
    dc = c1 - c0
    # Normalizar dirección
    if df != 0:
        df = int(df / abs(df))
    if dc != 0:
        dc = int(dc / abs(dc))
    if (df, dc) not in direcciones_permitidas:
        return False, None
    # Verificar que la selección es continua en esa dirección
    for i in range(1, len(seleccion)):
        pf, pc = seleccion[i-1]
        cf, cc = seleccion[i]
        if (cf - pf, cc - pc) != (df, dc):
            return False, None
    return True, (df, dc)

def jugar_sopa(dificultad):
    sopa = SopaDeLetras(0, 0)
    sopa.Dificultad(dificultad)
    rect_volver = pygame.Rect(10, 10, 80, 80) 
    rect_nuevo = pygame.Rect(10, 100, 80, 80)  # Botón nuevo abajo del de volver
    
    # Configuración para círculos - coordenadas específicas por nivel
    # Posiciones específicas para cada nivel - ajustadas a los círculos de las imágenes
    if dificultad == "facil":
        # Nivel fácil: 5x5, posición centrada en la parte superior
        radio_circulo = 15  # Círculos más pequeños para nivel fácil
        espaciado_x = 118  
        espaciado_y = 115  
        margen_x = 218  
        margen_y = 160  
        # Dimensiones de la sopa para calibración
        ancho_sopa = 5 * espaciado_x 
        alto_sopa = 5 * espaciado_y  
        margen_palabras_x = ANCHO - 330
        margen_palabras_y = 130
    elif dificultad == "media":
        # Nivel medio: 10x10, posición centrada
        radio_circulo = 16  # Círculos medianos para nivel normal
        espaciado_x = 69 
        espaciado_y = 58 
        margen_x = 170 
        margen_y = 120 
        margen_palabras_x = ANCHO - 330
        margen_palabras_y = 130
    elif dificultad == "dificil":
        # Nivel difícil: 15x15, posición ajustada
        radio_circulo = 14  # Círculos más pequeños para nivel difícil
        espaciado_x = 55 
        espaciado_y = 39  
        margen_x = 125
        margen_y = 110  
        margen_palabras_x = ANCHO - 310
        margen_palabras_y = 130

    seleccion = []
    palabras_encontradas = []
    letras_encontradas = set()
    seleccion_invalida = []
    mostrar_error = False
    error_time = 0

    palabras = [p.upper() for p in sopa.palabras_en_sopa]
    direcciones_permitidas = sopa.direcciones_usadas

    # Seleccionar la imagen según la dificultad
    if dificultad == "facil":
        imagen_fondo = nivel_facil_img
    elif dificultad == "media":
        imagen_fondo = nivel_normal_img
    else:  # dificil
        imagen_fondo = nivel_dificil_img

    def obtener_palabra_seleccionada_bidireccional():
        if not seleccion:
            return "", ""
        try:
            palabra1 = "".join([sopa.sopa[f][c] for f, c in seleccion])
            palabra2 = palabra1[::-1]
            return palabra1, palabra2
        except Exception:
            return "", ""

    def generar_nueva_sopa():
        nonlocal sopa, palabras, palabras_encontradas, letras_encontradas, seleccion
        sopa.Dificultad(dificultad)
        palabras = [p.upper() for p in sopa.palabras_en_sopa]
        palabras_encontradas = []
        letras_encontradas = set()
        seleccion = []

    def obtener_posicion_circulo(fila, col):
        """Calcula la posición del centro de un círculo"""
        # Todos los niveles usan espaciado separado en X e Y
        x = margen_x + col * espaciado_x + radio_circulo
        y = margen_y + fila * espaciado_y + radio_circulo
        return x, y

    def esta_dentro_circulo(pos_mouse, centro_circulo):
        """Verifica si un punto está dentro de un círculo"""
        x, y = pos_mouse
        cx, cy = centro_circulo
        distancia = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
        return distancia <= radio_circulo

    def obtener_celda_desde_posicion(pos_mouse):
        """Convierte una posición del mouse a coordenadas de celda"""
        x, y = pos_mouse
        for f in range(sopa.filas):
            for c in range(sopa.columnas):
                centro = obtener_posicion_circulo(f, c)
                if esta_dentro_circulo(pos_mouse, centro):
                    return f, c
        return None

    while True:
        ventana.blit(imagen_fondo, (0, 0))  # Usar la imagen correspondiente
        
        # Dibujar las letras con colores según el estado
        for f in range(sopa.filas):
            for c in range(sopa.columnas):
                centro_x, centro_y = obtener_posicion_circulo(f, c)
                
                # Determinar el color de la letra según el estado
                if (f, c) in letras_encontradas:
                    color_letra = (0, 255, 0)  # Verde oscuro para palabras encontradas
                elif (f, c) in seleccion:
                    color_letra = (0, 0, 255)  # Azul para selección actual
                elif (f, c) in seleccion_invalida:
                    color_letra = (255, 0, 0)  # Rojo para selección incorrecta
                else:
                    color_letra = NEGRO  # Negro para letras normales
                
                # Dibujar letra con fuente específica según nivel y color
                letra = sopa.sopa[f][c]
                if dificultad == "facil":
                    letra_img = fuente_sopa_facil.render(letra, True, color_letra)
                elif dificultad == "media":
                    letra_img = fuente_sopa_media.render(letra, True, color_letra)
                else:  # dificil
                    letra_img = fuente_sopa_dificil.render(letra, True, color_letra)
                letra_rect = letra_img.get_rect(center=(centro_x, centro_y))
                ventana.blit(letra_img, letra_rect)
        
        # Dibujar lista de palabras
        y_palabra = margen_palabras_y + 100  # Posición debajo de "PALABRAS"
        # Ajustar espaciado según la dificultad
        if dificultad == "dificil":
            espaciado_palabras = 44  # Más separación para nivel difícil
        else:
            espaciado_palabras = 50
            
        for palabra in palabras:
            if palabra in palabras_encontradas:
                # Palabras encontradas en gris
                texto_img = fuente_peque.render(palabra, True, (128, 128, 128))
                ventana.blit(texto_img, (margen_palabras_x, y_palabra))
            else:
                # Palabras no encontradas en negro
                texto_img = fuente_peque.render(palabra, True, NEGRO)
                ventana.blit(texto_img, (margen_palabras_x, y_palabra))
            y_palabra += espaciado_palabras
        
        pygame.display.flip()

        # Verificar si se encontraron todas las palabras
        if len(palabras_encontradas) == len(palabras):
            # Mostrar mensaje de felicitación sobre la pantalla actual
            mensaje = "¡FELICIDADES! Has encontrado todas las palabras"
            mensaje2 = "Regresando al menú de niveles..."
            texto1 = fuente.render(mensaje, True, (255, 255, 255))
            texto2 = fuente_peque.render(mensaje2, True, (255, 255, 255))
            rect1 = texto1.get_rect(center=(ANCHO//2, ALTO//2 - 50))
            rect2 = texto2.get_rect(center=(ANCHO//2, ALTO//2 + 50))
            # Dibujar un fondo semitransparente para el mensaje
            s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))  # Negro semitransparente
            ventana.blit(s, (0, 0))
            ventana.blit(texto1, rect1)
            ventana.blit(texto2, rect2)
            pygame.display.flip()
            pygame.time.wait(3000)  # Esperar 3 segundos
            return  # Regresar al menú de niveles

        if mostrar_error and time.time() - error_time > 0.5:
            mostrar_error = False
            seleccion_invalida = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rect_volver.collidepoint(event.pos):
                    return
                if rect_nuevo.collidepoint(event.pos):
                    generar_nueva_sopa()
                
                # Obtener celda desde posición del mouse
                celda = obtener_celda_desde_posicion(event.pos)
                if celda:
                    fila, col = celda
                    if (fila, col) not in seleccion:
                        seleccion.append((fila, col))
                        # Validar automáticamente si la selección es una palabra válida
                        es_valida, _ = es_seleccion_valida(seleccion, direcciones_permitidas)
                        palabra1, palabra2 = obtener_palabra_seleccionada_bidireccional()
                        if es_valida and ((palabra1.upper() in palabras and palabra1.upper() not in palabras_encontradas) or (palabra2.upper() in palabras and palabra2.upper() not in palabras_encontradas)):
                            if palabra1.upper() in palabras and palabra1.upper() not in palabras_encontradas:
                                palabras_encontradas.append(palabra1.upper())
                            elif palabra2.upper() in palabras and palabra2.upper() not in palabras_encontradas:
                                palabras_encontradas.append(palabra2.upper())
                            for f, c in seleccion:
                                letras_encontradas.add((f, c))
                            seleccion = []
                    else:
                        # Si hace clic en una celda ya seleccionada, validar la selección (por si el usuario quiere forzar validación)
                        es_valida, _ = es_seleccion_valida(seleccion, direcciones_permitidas)
                        palabra1, palabra2 = obtener_palabra_seleccionada_bidireccional()
                        if es_valida and ((palabra1.upper() in palabras and palabra1.upper() not in palabras_encontradas) or (palabra2.upper() in palabras and palabra2.upper() not in palabras_encontradas)):
                            if palabra1.upper() in palabras and palabra1.upper() not in palabras_encontradas:
                                palabras_encontradas.append(palabra1.upper())
                            elif palabra2.upper() in palabras and palabra2.upper() not in palabras_encontradas:
                                palabras_encontradas.append(palabra2.upper())
                            for f, c in seleccion:
                                letras_encontradas.add((f, c))
                            seleccion = []
                        else:
                            seleccion_invalida = seleccion[:]
                            mostrar_error = True
                            error_time = time.time()
                            seleccion = []
                else:
                    # Si hace clic fuera de la cuadrícula, validar la selección
                    if seleccion:
                        es_valida, _ = es_seleccion_valida(seleccion, direcciones_permitidas)
                        palabra1, palabra2 = obtener_palabra_seleccionada_bidireccional()
                        if es_valida and ((palabra1.upper() in palabras and palabra1.upper() not in palabras_encontradas) or (palabra2.upper() in palabras and palabra2.upper() not in palabras_encontradas)):
                            if palabra1.upper() in palabras and palabra1.upper() not in palabras_encontradas:
                                palabras_encontradas.append(palabra1.upper())
                            elif palabra2.upper() in palabras and palabra2.upper() not in palabras_encontradas:
                                palabras_encontradas.append(palabra2.upper())
                            for f, c in seleccion:
                                letras_encontradas.add((f, c))
                            seleccion = []
                        else:
                            seleccion_invalida = seleccion[:]
                            mostrar_error = True
                            error_time = time.time()
                            seleccion = []

# --- Inicio del programa ---
menu_principal()