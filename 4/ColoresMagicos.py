import pygame
import random
import sqlite3
import os
import sys
import colorsys

class ColoresMagicosPygame:
    FUENTE_TITULO = 'Baloo2-VariableFont_wght.ttf'
    TAM_TITULO = 62
    TAM_SUBTITULO = 30
    TAM_BOTON = 36
    TAM_LISTA = 24
    TAM_INSTRUCCION = 22

    def __init__(self):
        pygame.init()
        self.ANCHO = 1280
        self.ALTO = 720
        self.pantalla = pygame.display.set_mode((self.ANCHO, self.ALTO))
        pygame.display.set_caption("Colores Mágicos - Juego de Memoria")
        self.COLORES = {'fondo': (26, 35, 126),'fondo_claro': (40, 53, 147),'texto': (255, 255, 255),'texto_claro': (144, 202, 249),'rojo': (231, 76, 60),'amarillo': (241, 196, 15),'verde': (39, 174, 96),'azul': (52, 152, 219),'gris': (52, 73, 94),'verde_claro': (39, 174, 96),'rojo_claro': (231, 76, 60),'dorado': (241, 196, 15),'plateado': (149, 165, 166),'bronce': (230, 126, 34)}
        self.colores_juego = ["azul", "verde", "rosa", "amarillo"]
        self.colores_hex = {"azul": (173, 216, 230),"verde": (144, 238, 144),"rosa": (255, 182, 193),"amarillo": (255, 255, 224)}
        self.secuencia = []
        self.respuesta_actual = []
        self.nivel = 1
        self.frecuencias = 0
        self.mejores_puntuaciones = []
        self.indice_secuencia = 0
        self.nombre_jugador = ""
        self.estado = "bienvenida"
        self.estado_juego = "esperando"
        self.db_path = "colores_magicos.db"
        self.inicializar_base_datos()
        self.cargar_puntuaciones()
        self.fuente_titulo = pygame.font.Font(self.FUENTE_TITULO, self.TAM_TITULO)
        self.fuente_titulo.set_bold(True)
        self.fuente_subtitulo = pygame.font.Font(self.FUENTE_TITULO, self.TAM_SUBTITULO)
        self.fuente_subtitulo.set_bold(True)
        self.fuente_boton = pygame.font.Font(self.FUENTE_TITULO, self.TAM_BOTON)
        self.fuente_boton.set_bold(True)
        self.fuente_lista = pygame.font.Font(self.FUENTE_TITULO, self.TAM_LISTA)
        self.fuente_instruccion = pygame.font.Font(self.FUENTE_TITULO, self.TAM_INSTRUCCION)
        self.cache_texto = {}
        self.botones = {}
        self.crear_botones()
        self.tiempo_ultimo_evento = pygame.time.get_ticks()
        self.rect_colores = {}
        self.crear_rect_colores()
        self.texto_entrada = ""
        self.ultimo_color_clicado = None
        self.tiempo_ultimo_clic = 0
        self.duracion_feedback = 300
        self.color_iluminado = None
        self.tiempo_iluminacion = 0
        self.duracion_iluminacion = 800
        self.imagen_fondo = None
        self.cargar_imagen_fondo()
        self.imagen_boton = None
        self.cargar_imagen_botones()
        self.ultimo_estado = None
        self.necesita_redibujar = True
        self.boton_hover = None
        self.boton_click = None
        self.tiempo_click = 0
        self.duracion_click = 300

    def inicializar_base_datos(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS puntuaciones (id INTEGER PRIMARY KEY AUTOINCREMENT,nombre TEXT NOT NULL,frecuencias INTEGER NOT NULL,fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error al inicializar base de datos: {e}")

    def cargar_puntuaciones(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT nombre, frecuencias FROM puntuaciones ORDER BY frecuencias DESC LIMIT 50')
            self.mejores_puntuaciones = cursor.fetchall()
            conn.close()
        except Exception as e:
            print(f"Error al cargar puntuaciones: {e}")
            self.mejores_puntuaciones = []

    def guardar_puntuacion(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO puntuaciones (nombre, frecuencias) VALUES (?, ?)',(self.nombre_jugador, self.frecuencias))
            conn.commit()
            conn.close()
            self.cargar_puntuaciones()
        except Exception as e:
            print(f"Error al guardar puntuación: {e}")

    def limpiar_puntuaciones(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM puntuaciones')
            conn.commit()
            conn.close()
            self.mejores_puntuaciones = []
        except Exception as e:
            print(f"Error al limpiar puntuaciones: {e}")

    def crear_botones(self):
        boton_w, boton_h = 280, 100
        espacio_y = 20
        offset_x = (self.ANCHO - boton_w) // 2
        offset_y = 180
        boton_pequeno_w, boton_pequeno_h = 180, 50
        espacio_botones = 40
        boton_volver_w, boton_volver_h = 120, 45
        self.botones = {'jugar': pygame.Rect(offset_x, offset_y, boton_w, boton_h),'puntuaciones': pygame.Rect(offset_x, offset_y + boton_h + espacio_y, boton_w, boton_h),'info': pygame.Rect(offset_x, offset_y + 2*(boton_h + espacio_y), boton_w, boton_h),'salir': pygame.Rect(offset_x, offset_y + 3*(boton_h + espacio_y), boton_w, boton_h),'continuar': pygame.Rect(offset_x, self.ALTO - 180, boton_w, boton_h),'iniciar_juego': pygame.Rect(offset_x, 400, boton_w, boton_h),'volver_menu': pygame.Rect(30, 30, boton_volver_w, boton_volver_h),'limpiar_puntuaciones': pygame.Rect(0, 0, 220, 70),'volver_a_jugar': pygame.Rect(0, 0, boton_pequeno_w, boton_pequeno_h),'menu_principal': pygame.Rect(0, 0, boton_pequeno_w, boton_pequeno_h),'confirmar_si': pygame.Rect(offset_x - boton_pequeno_w//2 - espacio_botones//2, self.ALTO - 140, boton_pequeno_w, boton_pequeno_h),'confirmar_no': pygame.Rect(offset_x + boton_pequeno_w//2 + espacio_botones//2, self.ALTO - 140, boton_pequeno_w, boton_pequeno_h),'ok': pygame.Rect(self.ANCHO - 120, self.ALTO - 80, 100, 50)}

    def crear_rect_colores(self):
        boton_w, boton_h = 240, 120
        espacio_x, espacio_y = 80, 60
        total_w = boton_w * 2 + espacio_x
        total_h = boton_h * 2 + espacio_y
        offset_x = (self.ANCHO - total_w) // 2
        offset_y = 220
        posiciones = [(offset_x, offset_y),(offset_x + boton_w + espacio_x, offset_y),(offset_x, offset_y + boton_h + espacio_y),(offset_x + boton_w + espacio_x, offset_y + boton_h + espacio_y)]
        for i, color in enumerate(self.colores_juego):
            self.rect_colores[color] = pygame.Rect(posiciones[i][0], posiciones[i][1], boton_w, boton_h)

    def dibujar_boton_menu(self, rect, texto, clave=None):
        tiempo_actual = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()
        esta_hover = rect.collidepoint(mouse_pos)
        esta_click = (self.boton_click == clave and tiempo_actual - self.tiempo_click < self.duracion_click)
        if esta_hover:
            self.boton_hover = clave
        elif self.boton_hover == clave:
            self.boton_hover = None
        desplazamiento = (0, 0)
        if self.imagen_boton:
            imagen_escalada = pygame.transform.scale(self.imagen_boton, (rect.width, rect.height))
            if esta_click:
                self.pantalla.blit(imagen_escalada, rect.move(*desplazamiento))
            else:
                self.pantalla.blit(imagen_escalada, rect)
        else:
            color_boton = (180, 238, 224)
            if esta_click:
                pygame.draw.ellipse(self.pantalla, color_boton, rect.move(*desplazamiento))
                pygame.draw.ellipse(self.pantalla, (0, 0, 0), rect.move(*desplazamiento), 3)
                pygame.draw.ellipse(self.pantalla, (0, 0, 0), rect.move(*desplazamiento).inflate(-8, -8), 2)
            else:
                pygame.draw.ellipse(self.pantalla, color_boton, rect)
                pygame.draw.ellipse(self.pantalla, (0, 0, 0), rect, 3)
                pygame.draw.ellipse(self.pantalla, (0, 0, 0), rect.inflate(-8, -8), 2)
        if rect.width <= 120:
            tamano_fuente = 28
        elif texto in ["SÍ, BORRAR", "CANCELAR"]:
            tamano_fuente = 24
        elif texto in ["Volver a Jugar", "Menú Principal"]:
            tamano_fuente = 24
        else:
            tamano_fuente = self.TAM_BOTON
        cache_key = f"boton_{texto}_{tamano_fuente}"
        if cache_key not in self.cache_texto:
            fuente = pygame.font.Font(self.FUENTE_TITULO, tamano_fuente)
            fuente.set_bold(True)
            texto_surf = fuente.render(texto, True, (54, 73, 110))
            self.cache_texto[cache_key] = texto_surf
        else:
            texto_surf = self.cache_texto[cache_key]
        texto_rect = texto_surf.get_rect(center=rect.center)
        texto_rect = texto_rect.move(*desplazamiento) if esta_click else texto_rect
        self.pantalla.blit(texto_surf, texto_rect)

    def dibujar_titulo(self, texto, y):
        cache_key = f"titulo_{texto}_{y}"
        if cache_key not in self.cache_texto:
            surf = self.fuente_titulo.render(texto, True, (54, 73, 110))
            rect = surf.get_rect(center=(self.ANCHO//2, y))
            self.cache_texto[cache_key] = (surf, rect)
        else:
            surf, rect = self.cache_texto[cache_key]
        self.pantalla.blit(surf, rect)

    def dibujar_subtitulo(self, texto, y):
        cache_key = f"subtitulo_{texto}_{y}"
        if cache_key not in self.cache_texto:
            surf = self.fuente_subtitulo.render(texto, True, (54, 73, 110))
            rect = surf.get_rect(center=(self.ANCHO//2, y))
            self.cache_texto[cache_key] = (surf, rect)
        else:
            surf, rect = self.cache_texto[cache_key]
        self.pantalla.blit(surf, rect)

    def dibujar_texto_centrado(self, texto, y, color=(54, 73, 110), size=None):
        cache_key = f"texto_{texto}_{y}_{color}_{size}"
        if cache_key not in self.cache_texto:
            fuente = self.fuente_lista if size is None else pygame.font.Font(self.FUENTE_TITULO, size)
            surf = fuente.render(texto, True, color)
            rect = surf.get_rect(center=(self.ANCHO//2, y))
            self.cache_texto[cache_key] = (surf, rect)
        else:
            surf, rect = self.cache_texto[cache_key]
        self.pantalla.blit(surf, rect)

    def dibujar_fondo_estrellas(self):
        if self.imagen_fondo:
            self.pantalla.blit(self.imagen_fondo, (0, 0))
        else:
            self.pantalla.fill((0, 0, 0))

    def dibujar_bienvenida(self):
        self.dibujar_fondo_estrellas()
        cache_key = "bienvenida_titulo"
        if cache_key not in self.cache_texto:
            fuente_titulo = pygame.font.Font(self.FUENTE_TITULO, self.TAM_TITULO)
            fuente_titulo.set_bold(True)
            surf_titulo = fuente_titulo.render("COLORES MAGICOS", True, (54, 73, 110))
            rect_titulo = surf_titulo.get_rect(center=(self.ANCHO//2, 90))
            self.cache_texto[cache_key] = (surf_titulo, rect_titulo)
        else:
            surf_titulo, rect_titulo = self.cache_texto[cache_key]
        self.pantalla.blit(surf_titulo, rect_titulo)
        cache_key = "bienvenida_bloque1"
        if cache_key not in self.cache_texto:
            bloque1 = "Este juego educativo está diseñado específicamente para niños con TDAH."
            fuente_bloque = pygame.font.Font(self.FUENTE_TITULO, self.TAM_INSTRUCCION)
            surf1 = fuente_bloque.render(bloque1, True, (54, 73, 110))
            rect1 = surf1.get_rect(center=(self.ANCHO//2, 180))
            self.cache_texto[cache_key] = (surf1, rect1)
        else:
            surf1, rect1 = self.cache_texto[cache_key]
        self.pantalla.blit(surf1, rect1)
        cache_key = "bienvenida_bloque2a"
        if cache_key not in self.cache_texto:
            bloque2a = "Ayuda a mejorar la atención sostenida, la memoria de trabajo y habilidades"
            fuente_bloque = pygame.font.Font(self.FUENTE_TITULO, self.TAM_INSTRUCCION)
            surf2a = fuente_bloque.render(bloque2a, True, (54, 73, 110))
            rect2a = surf2a.get_rect(center=(self.ANCHO//2, 240))
            self.cache_texto[cache_key] = (surf2a, rect2a)
        else:
            surf2a, rect2a = self.cache_texto[cache_key]
        self.pantalla.blit(surf2a, rect2a)
        cache_key = "bienvenida_bloque2b"
        if cache_key not in self.cache_texto:
            bloque2b = "secuenciales a través de secuencia de colores"
            fuente_bloque = pygame.font.Font(self.FUENTE_TITULO, self.TAM_INSTRUCCION)
            surf2b = fuente_bloque.render(bloque2b, True, (54, 73, 110))
            rect2b = surf2b.get_rect(center=(self.ANCHO//2, 280))
            self.cache_texto[cache_key] = (surf2b, rect2b)
        else:
            surf2b, rect2b = self.cache_texto[cache_key]
        self.pantalla.blit(surf2b, rect2b)
        cache_key = "bienvenida_bloque3a"
        if cache_key not in self.cache_texto:
            bloque3a = "Los colores suaves y la estructura clara del juego facilitan la concentración y"
            fuente_bloque = pygame.font.Font(self.FUENTE_TITULO, self.TAM_INSTRUCCION)
            surf3a = fuente_bloque.render(bloque3a, True, (54, 73, 110))
            rect3a = surf3a.get_rect(center=(self.ANCHO//2, 340))
            self.cache_texto[cache_key] = (surf3a, rect3a)
        else:
            surf3a, rect3a = self.cache_texto[cache_key]
        self.pantalla.blit(surf3a, rect3a)
        cache_key = "bienvenida_bloque3b"
        if cache_key not in self.cache_texto:
            bloque3b = "reducen la sobrecarga sensorial."
            fuente_bloque = pygame.font.Font(self.FUENTE_TITULO, self.TAM_INSTRUCCION)
            surf3b = fuente_bloque.render(bloque3b, True, (54, 73, 110))
            rect3b = surf3b.get_rect(center=(self.ANCHO//2, 380))
            self.cache_texto[cache_key] = (surf3b, rect3b)
        else:
            surf3b, rect3b = self.cache_texto[cache_key]
        self.pantalla.blit(surf3b, rect3b)
        self.dibujar_boton_menu(self.botones['continuar'], "COMENZAR")

    def dibujar_menu_principal(self):
        self.dibujar_fondo_estrellas()
        self.dibujar_titulo("COLORES MAGICOS", 120)
        self.dibujar_boton_menu(self.botones['jugar'], "Jugar", clave='jugar')
        self.dibujar_boton_menu(self.botones['puntuaciones'], "Puntuaciones", clave='puntuaciones')
        self.dibujar_boton_menu(self.botones['info'], "Información", clave='info')
        self.dibujar_boton_menu(self.botones['salir'], "Salir", clave='salir')

    def dibujar_boton_color_juego(self, rect, color, texto, iluminado=False):
        radio_esquinas = 25
        color_borde = tuple(max(0, c - 40) for c in self.colores_hex[color])
        if iluminado:
            base = self.colores_hex[color]
            r, g, b = [c / 255.0 for c in base]
            h, s, v = colorsys.rgb_to_hsv(r, g, b)
            s = 0.6
            r2, g2, b2 = colorsys.hsv_to_rgb(h, s, v)
            color_iluminado = (int(r2 * 255), int(g2 * 255), int(b2 * 255))
            pygame.draw.rect(self.pantalla, color_iluminado, rect, border_radius=radio_esquinas)
            pygame.draw.rect(self.pantalla, color_borde, rect, 3, border_radius=radio_esquinas)
        else:
            pygame.draw.rect(self.pantalla, self.colores_hex[color], rect, border_radius=radio_esquinas)
            pygame.draw.rect(self.pantalla, color_borde, rect, 3, border_radius=radio_esquinas)
        rect_interior = rect.inflate(-8, -8)
        pygame.draw.rect(self.pantalla, color_borde, rect_interior, 2, border_radius=radio_esquinas)

    def dibujar_juego(self):
        self.dibujar_fondo_estrellas()
        self.dibujar_titulo("JUGANDO", 80)
        self.dibujar_boton_menu(self.botones['volver_menu'], "Volver")
        self.dibujar_texto_centrado(f"Nivel: {self.nivel}", 140, (54, 73, 110), 36)
        boton_w, boton_h = 240, 120
        espacio_x, espacio_y = 80, 60
        total_w = boton_w * 2 + espacio_x
        total_h = boton_h * 2 + espacio_y
        offset_x = (self.ANCHO - total_w) // 2
        offset_y = 220
        posiciones = [
            (offset_x, offset_y),
            (offset_x + boton_w + espacio_x, offset_y),
            (offset_x, offset_y + boton_h + espacio_y),
            (offset_x + boton_w + espacio_x, offset_y + boton_h + espacio_y)
        ]
        for i, color in enumerate(self.colores_juego):
            rect = self.rect_colores[color]
            rect.x, rect.y = posiciones[i]
            rect.width, rect.height = boton_w, boton_h
            iluminado = (self.color_iluminado == color) or (self.ultimo_color_clicado == color)
            self.dibujar_boton_color_juego(rect, color, "", iluminado)
        y_frecuencias = offset_y + total_h + 60
        if self.estado_juego != "esperando":
            self.dibujar_texto_centrado(f"Frecuencias obtenidas: {self.frecuencias}", y_frecuencias, (54, 73, 110), 28)
        y_mensajes = y_frecuencias + 40
        if self.estado_juego == "esperando":
            boton_iniciar_y = min(offset_y + total_h + 160, self.ALTO - 120)
            self.botones['iniciar_juego'].centerx = self.ANCHO // 2
            self.botones['iniciar_juego'].centery = boton_iniciar_y
            self.dibujar_boton_menu(self.botones['iniciar_juego'], "Iniciar Juego")
        elif self.estado_juego == "mostrando":
            self.dibujar_texto_centrado("Observa la secuencia...", y_mensajes)
        elif self.estado_juego == "jugando":
            self.dibujar_texto_centrado("¡Tu turno! Repite la secuencia:", y_mensajes)
            self.dibujar_texto_centrado(f"{len(self.respuesta_actual)} de {len(self.secuencia)} colores", y_mensajes + 40, (54, 73, 110), 28)
        elif self.estado_juego == "completado":
            self.dibujar_texto_centrado("¡Secuencia completada!", y_mensajes)
            self.dibujar_texto_centrado(f"Frecuencia {self.frecuencias + 1} completada", y_mensajes + 40, (54, 73, 110), 28)
        elif self.estado_juego == "pausado":
            self.dibujar_texto_centrado("¡Correcto! Preparando siguiente nivel...", y_mensajes)
            self.dibujar_texto_centrado(f"Frecuencia {self.frecuencias} completada", y_mensajes + 40, (54, 73, 110), 28)

    def dibujar_puntuaciones(self):
        self.dibujar_fondo_estrellas()
        self.dibujar_titulo("RECORD", 120)
        self.dibujar_boton_menu(self.botones['volver_menu'], "Volver")
        y_base = 220
        if self.mejores_puntuaciones:
            fuente = pygame.font.Font(self.FUENTE_TITULO, 36)
            fuente.set_bold(True)
            x_offset = -60  # Desplazamiento a la izquierda
            x_pos = self.ANCHO//2 - 220 + x_offset
            x_nombre = self.ANCHO//2 - 40 + x_offset
            x_freq = self.ANCHO//2 + 200 + x_offset
            surf_pos = fuente.render("Posición", True, (54, 73, 110))
            rect_pos = surf_pos.get_rect(left=x_pos, centery=y_base)
            self.pantalla.blit(surf_pos, rect_pos)
            surf_nombre = fuente.render("Jugador", True, (54, 73, 110))
            rect_nombre = surf_nombre.get_rect(left=x_nombre, centery=y_base)
            self.pantalla.blit(surf_nombre, rect_nombre)
            surf_freq = fuente.render("Frecuencias", True, (54, 73, 110))
            rect_freq = surf_freq.get_rect(left=x_freq, centery=y_base)
            self.pantalla.blit(surf_freq, rect_freq)
            fuente = pygame.font.Font(self.FUENTE_TITULO, 28)
            fuente.set_bold(True)
            for i, (nombre, frecuencias) in enumerate(self.mejores_puntuaciones[:5], 1):
                surf_pos = fuente.render(f"{i:2d}", True, (54, 73, 110))
                rect_pos = surf_pos.get_rect(left=x_pos, centery=y_base + 40 + i*30)
                self.pantalla.blit(surf_pos, rect_pos)
                surf_nombre = fuente.render(f"{nombre}", True, (54, 73, 110))
                rect_nombre = surf_nombre.get_rect(left=x_nombre, centery=y_base + 40 + i*30)
                self.pantalla.blit(surf_nombre, rect_nombre)
                surf_freq = fuente.render(f"{frecuencias}", True, (54, 73, 110))
                rect_freq = surf_freq.get_rect(left=x_freq, centery=y_base + 40 + i*30)
                self.pantalla.blit(surf_freq, rect_freq)
        else:
            self.dibujar_texto_centrado("Aún no hay puntuaciones registradas", y_base+40)
            self.dibujar_texto_centrado("¡Sé el primero en jugar!", y_base+80, (54, 73, 110), 32)
        self.botones['limpiar_puntuaciones'].centerx = self.ANCHO // 2
        self.botones['limpiar_puntuaciones'].bottom = self.ALTO - 80
        self.dibujar_boton_menu(self.botones['limpiar_puntuaciones'], "LIMPIAR")

    def dibujar_info(self):
        self.dibujar_fondo_estrellas()
        surf_titulo = self.fuente_titulo.render("Información del Juego", True, (54, 73, 110))
        rect_titulo = surf_titulo.get_rect(center=(self.ANCHO//2, 50))
        self.pantalla.blit(surf_titulo, rect_titulo)
        intro = [
            "Juego Educativo de Memoria y Concentración para Niños",
            "está diseñado específicamente para ayudar a niños con",
            "trastorno de Déficit de Atención e Hiperactividad."
        ]
        for i, linea in enumerate(intro):
            surf = self.fuente_instruccion.render(linea, True, (54, 73, 110))
            rect = surf.get_rect(center=(self.ANCHO//2, 100 + i*32))
            self.pantalla.blit(surf, rect)
        surf_ben = self.fuente_subtitulo.render("Beneficios:", True, (54, 73, 110))
        rect_ben = surf_ben.get_rect(left=220, top=190)
        self.pantalla.blit(surf_ben, rect_ben)
        beneficios = [
            "Mejora la atención sostenida",
            "Desarrolla la memoria de trabajo",
            "Fortalece las habilidades secuenciales",
            "Reduce la impulsividad",
            "Aumenta la concentración visual"
        ]
        for i, b in enumerate(beneficios):
            texto = f"• {b}"
            surf = self.fuente_lista.render(texto, True, (54, 73, 110))
            rect = surf.get_rect(left=250, top=230 + i*28)
            self.pantalla.blit(surf, rect)
        surf_cj = self.fuente_subtitulo.render("Cómo Jugar:", True, (54, 73, 110))
        rect_cj = surf_cj.get_rect(left=220, top=390)
        self.pantalla.blit(surf_cj, rect_cj)
        como_jugar = [
            "Observa la secuencia de colores que aparece",
            "Repite la secuencia en el mismo orden",
            "Cada nivel añade un color más a la secuencia",
            "El juego termina al primer error"
        ]
        for i, c in enumerate(como_jugar):
            texto = f"• {c}"
            surf = self.fuente_lista.render(texto, True, (54, 73, 110))
            rect = surf.get_rect(left=250, top=430 + i*28)
            self.pantalla.blit(surf, rect)
        final = [
            "¡Diseñado con colores suaves y estructura clara para",
            "facilitar la concentración!"
        ]
        for i, linea in enumerate(final):
            surf = self.fuente_instruccion.render(linea, True, (54, 73, 110))
            rect = surf.get_rect(center=(self.ANCHO//2, 600 + i*28))
            self.pantalla.blit(surf, rect)
        ok_rect = pygame.Rect(self.ANCHO - 150, self.ALTO - 80, 100, 50)
        self.botones['ok'] = ok_rect
        self.dibujar_boton_menu(ok_rect, "OK", clave='ok')

    def dibujar_fin_juego(self):
        self.dibujar_fondo_estrellas()
        self.dibujar_titulo("¡Juego terminado!", 120)
        y_base = 220
        self.dibujar_texto_centrado(f"Jugador: {self.nombre_jugador}", y_base, (54, 73, 110), 32)
        self.dibujar_texto_centrado(f"Frecuencias alcanzadas: {self.frecuencias}", y_base+50, (54, 73, 110), 32)
        self.dibujar_texto_centrado(f"Nivel alcanzado: {self.nivel}", y_base+100, (54, 73, 110), 32)
        self.dibujar_texto_centrado("¿Quieres volver a jugar o regresar al menú?", y_base+170, (54, 73, 110), 28)
        boton_pequeno_w, boton_pequeno_h = 200, 85
        espacio_botones = 30
        boton_y = y_base+250
        centro_pantalla = self.ANCHO // 2
        self.botones['volver_a_jugar'].width = boton_pequeno_w
        self.botones['volver_a_jugar'].height = boton_pequeno_h
        self.botones['volver_a_jugar'].centerx = centro_pantalla - boton_pequeno_w//2 - espacio_botones//2
        self.botones['volver_a_jugar'].centery = boton_y
        self.dibujar_boton_menu(self.botones['volver_a_jugar'], "Volver a Jugar")
        self.botones['menu_principal'].width = boton_pequeno_w
        self.botones['menu_principal'].height = boton_pequeno_h
        self.botones['menu_principal'].centerx = centro_pantalla + boton_pequeno_w//2 + espacio_botones//2
        self.botones['menu_principal'].centery = boton_y
        self.dibujar_boton_menu(self.botones['menu_principal'], "Menú Principal")

    def dibujar_entrada_nombre(self):
        self.dibujar_fondo_estrellas()
        self.dibujar_titulo("INGRESA TU NOMBRE", 120)
        entrada_rect = pygame.Rect(self.ANCHO//2 - 200, 220, 400, 60)
        pygame.draw.rect(self.pantalla, (255,255,255), entrada_rect, border_radius=18)
        pygame.draw.rect(self.pantalla, (54, 73, 110), entrada_rect, 3, border_radius=18)
        texto_nombre = self.texto_entrada if self.texto_entrada else "Escribe aquí..."
        color_texto = (54, 73, 110) if self.texto_entrada else (150,150,150)
        fuente = pygame.font.Font(self.FUENTE_TITULO, 32)
        surf = fuente.render(texto_nombre, True, color_texto)
        rect = surf.get_rect(center=entrada_rect.center)
        self.pantalla.blit(surf, rect)
        self.dibujar_texto_centrado("Presiona ENTER para continuar", entrada_rect.bottom + 40, (54, 73, 110), 28)
        self.dibujar_boton_menu(self.botones['volver_menu'], "Volver", clave='volver_menu')

    def dibujar_confirmar_borrado(self):
        self.dibujar_fondo_estrellas()
        self.dibujar_titulo("CONFIRMAR BORRADO", 120)
        self.dibujar_texto_centrado("¿Estás seguro de que quieres eliminar", 320, (54, 73, 110), 26)
        self.dibujar_texto_centrado("todas las puntuaciones?", 360, (54, 73, 110), 26)
        self.dibujar_texto_centrado("Esta acción no se puede deshacer.", 400, (150,150,150), 24)
        boton_pequeno_w, boton_pequeno_h = 200, 100
        espacio_botones = 40
        boton_y = 460
        centro_pantalla = self.ANCHO // 2
        self.botones['confirmar_si'].centerx = centro_pantalla - boton_pequeno_w//2 - espacio_botones//2
        self.botones['confirmar_si'].centery = boton_y
        self.dibujar_boton_menu(self.botones['confirmar_si'], "SÍ, BORRAR", clave='confirmar_si')
        self.botones['confirmar_no'].centerx = centro_pantalla + boton_pequeno_w//2 + espacio_botones//2
        self.botones['confirmar_no'].centery = boton_y
        self.dibujar_boton_menu(self.botones['confirmar_no'], "CANCELAR", clave='confirmar_no')

    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    resultado = self.manejar_clic(evento.pos)
                    if resultado == False:
                        return False
            elif evento.type == pygame.KEYDOWN:
                if self.estado == "entrada_nombre":
                    if evento.key == pygame.K_RETURN:
                        if self.texto_entrada.strip():
                            self.nombre_jugador = self.texto_entrada.strip()
                            self.texto_entrada = ""
                            self.estado = "juego"
                            self.estado_juego = "esperando"
                            self.necesita_redibujar = True
                    elif evento.key == pygame.K_BACKSPACE:
                        self.texto_entrada = self.texto_entrada[:-1]
                        self.necesita_redibujar = True
                    else:
                        if len(self.texto_entrada) < 20:
                            self.texto_entrada += evento.unicode
                            self.necesita_redibujar = True
        return True

    def manejar_clic(self, pos):
        tiempo_actual = pygame.time.get_ticks()
        if self.estado == "bienvenida":
            if self.botones['continuar'].collidepoint(pos):
                self.boton_click = "continuar"
                self.tiempo_click = tiempo_actual
                self.necesita_redibujar = True
                self.estado = "menu"
        elif self.estado == "menu":
            if self.botones['jugar'].collidepoint(pos):
                self.boton_click = "jugar"
                self.tiempo_click = tiempo_actual
                self.necesita_redibujar = True
                self.estado = "entrada_nombre"
                self.texto_entrada = ""
            elif self.botones['puntuaciones'].collidepoint(pos):
                self.boton_click = "puntuaciones"
                self.tiempo_click = tiempo_actual
                self.necesita_redibujar = True
                self.estado = "puntuaciones"
            elif self.botones['info'].collidepoint(pos):
                self.boton_click = "info"
                self.tiempo_click = tiempo_actual
                self.necesita_redibujar = True
                self.estado = "info"
            elif self.botones['salir'].collidepoint(pos):
                self.boton_click = "salir"
                self.tiempo_click = tiempo_actual
                self.necesita_redibujar = True
                return False
        elif self.estado == "entrada_nombre":
            if self.botones['volver_menu'].collidepoint(pos):
                self.boton_click = "volver_menu"
                self.tiempo_click = tiempo_actual
                self.necesita_redibujar = True
                self.estado = "menu"
                self.texto_entrada = ""
        elif self.estado == "juego":
            if self.botones['volver_menu'].collidepoint(pos):
                self.boton_click = "volver_menu"
                self.tiempo_click = tiempo_actual
                self.necesita_redibujar = True
                self.estado = "menu"
            elif self.botones['iniciar_juego'].collidepoint(pos) and self.estado_juego == "esperando":
                self.boton_click = "iniciar_juego"
                self.tiempo_click = tiempo_actual
                self.necesita_redibujar = True
                self.iniciar_juego()
            else:
                for color, rect in self.rect_colores.items():
                    if rect.collidepoint(pos):
                        self.color_clicado(color)
                        self.necesita_redibujar = True
                        break
        elif self.estado == "puntuaciones":
            if self.botones['volver_menu'].collidepoint(pos):
                self.boton_click = "volver_menu"
                self.tiempo_click = tiempo_actual
                self.necesita_redibujar = True
                self.estado = "menu"
            elif self.botones['limpiar_puntuaciones'].collidepoint(pos):
                self.boton_click = "limpiar_puntuaciones"
                self.tiempo_click = tiempo_actual
                self.necesita_redibujar = True
                self.estado = "confirmar_borrado"
        elif self.estado == "info":
            if self.botones['ok'].collidepoint(pos):
                self.boton_click = "ok"
                self.tiempo_click = tiempo_actual
                self.necesita_redibujar = True
                self.estado = "menu"
        elif self.estado == "fin_juego":
            if self.botones['volver_a_jugar'].collidepoint(pos):
                self.boton_click = "volver_a_jugar"
                self.tiempo_click = tiempo_actual
                self.necesita_redibujar = True
                self.reiniciar_juego()
            elif self.botones['menu_principal'].collidepoint(pos):
                self.boton_click = "menu_principal"
                self.tiempo_click = tiempo_actual
                self.necesita_redibujar = True
                self.estado = "menu"
        elif self.estado == "confirmar_borrado":
            if self.botones['confirmar_si'].collidepoint(pos):
                self.boton_click = "confirmar_si"
                self.tiempo_click = tiempo_actual
                self.necesita_redibujar = True
                self.limpiar_puntuaciones()
                self.estado = "puntuaciones"
            elif self.botones['confirmar_no'].collidepoint(pos):
                self.boton_click = "confirmar_no"
                self.tiempo_click = tiempo_actual
                self.necesita_redibujar = True
                self.estado = "puntuaciones"
        return True

    def iniciar_juego(self):
        self.secuencia = []
        self.respuesta_actual = []
        self.nivel = 1
        self.frecuencias = 0
        self.estado_juego = "mostrando"
        self.indice_secuencia = 0
        self.tiempo_ultimo_evento = pygame.time.get_ticks()
        self.nuevo_nivel()

    def nuevo_nivel(self):
        color_nuevo = random.choice(self.colores_juego)
        self.secuencia.append(color_nuevo)
        self.estado_juego = "mostrando"
        self.indice_secuencia = 0
        self.tiempo_ultimo_evento = pygame.time.get_ticks()

    def color_clicado(self, color):
        if self.estado_juego == "jugando":
            posicion_actual = len(self.respuesta_actual)
            if posicion_actual < len(self.secuencia):
                color_correcto = self.secuencia[posicion_actual]
                if color == color_correcto:
                    self.ultimo_color_clicado = color
                    self.tiempo_ultimo_clic = pygame.time.get_ticks()
                    self.respuesta_actual.append(color)
                    if len(self.respuesta_actual) == len(self.secuencia):
                        self.estado_juego = "completado"
                        self.tiempo_ultimo_evento = pygame.time.get_ticks()
                else:
                    self.fin_juego()

    def verificar_respuesta(self):
        self.frecuencias += 1
        self.nivel += 1
        self.estado_juego = "pausado"
        self.tiempo_ultimo_evento = pygame.time.get_ticks()
        self.ultimo_color_clicado = None

    def fin_juego(self):
        if self.nombre_jugador:
            self.guardar_puntuacion()
        self.estado = "fin_juego"

    def reiniciar_juego(self):
        self.estado = "juego"
        self.estado_juego = "esperando"
        self.secuencia = []
        self.respuesta_actual = []
        self.nivel = 1
        self.frecuencias = 0
        self.ultimo_color_clicado = None

    def cargar_imagen_fondo(self):
        try:
            posibles_nombres = ["fondo.jpg", "fondo.png", "background.jpg", "background.png", "fondo_magico.jpg", "fondo_magico.png"]
            for nombre in posibles_nombres:
                if os.path.exists(nombre):
                    self.imagen_fondo = pygame.image.load(nombre)
                    self.imagen_fondo = pygame.transform.scale(self.imagen_fondo, (self.ANCHO, self.ALTO))
                    return
        except Exception as e:
            print(f"Error al cargar imagen de fondo: {e}")
            self.imagen_fondo = None

    def cargar_imagen_botones(self):
        try:
            nombre_boton = "boton.png"
            if os.path.exists(nombre_boton):
                self.imagen_boton = pygame.image.load(nombre_boton).convert_alpha()
                return
        except Exception as e:
            print(f"Error al cargar imagen de botones: {e}")
            self.imagen_boton = None

    def actualizar_juego(self):
        tiempo_actual = pygame.time.get_ticks()
        necesita_actualizar = False
        pausa_repetido = 300
        pausa_apagado = 250
        if not hasattr(self, 'estado_apagado_repetido'):
            self.estado_apagado_repetido = False
            self.tiempo_apagado_repetido = 0
        if self.estado_juego == "mostrando":
            if self.indice_secuencia < len(self.secuencia):
                if self.estado_apagado_repetido:
                    if tiempo_actual - self.tiempo_apagado_repetido >= pausa_apagado:
                        self.estado_apagado_repetido = False
                        self.color_iluminado = self.secuencia[self.indice_secuencia]
                        self.tiempo_iluminacion = tiempo_actual
                        necesita_actualizar = True
                elif self.color_iluminado is None:
                    if self.indice_secuencia > 0 and self.secuencia[self.indice_secuencia] == self.secuencia[self.indice_secuencia-1]:
                        self.estado_apagado_repetido = True
                        self.tiempo_apagado_repetido = tiempo_actual
                        necesita_actualizar = True
                    else:
                        self.color_iluminado = self.secuencia[self.indice_secuencia]
                        self.tiempo_iluminacion = tiempo_actual
                        necesita_actualizar = True
                else:
                    pausa_extra = 0
                    if self.indice_secuencia > 0 and self.secuencia[self.indice_secuencia] == self.secuencia[self.indice_secuencia-1]:
                        pausa_extra = pausa_repetido
                    if tiempo_actual - self.tiempo_iluminacion >= self.duracion_iluminacion + pausa_extra:
                        self.color_iluminado = None
                        self.indice_secuencia += 1
                        self.tiempo_ultimo_evento = tiempo_actual
                        self.estado_apagado_repetido = False
                        necesita_actualizar = True
            else:
                self.color_iluminado = None
                self.estado_juego = "jugando"
                self.respuesta_actual = []
                self.estado_apagado_repetido = False
                necesita_actualizar = True
        elif self.estado_juego == "completado":
            if tiempo_actual - self.tiempo_ultimo_evento >= 1000:
                self.verificar_respuesta()
                necesita_actualizar = True
        elif self.estado_juego == "pausado":
            if tiempo_actual - self.tiempo_ultimo_evento >= 2000:
                self.nuevo_nivel()
                necesita_actualizar = True
        if self.ultimo_color_clicado and tiempo_actual - self.tiempo_ultimo_clic >= self.duracion_feedback:
            self.ultimo_color_clicado = None
            necesita_actualizar = True
        if self.boton_click and tiempo_actual - self.tiempo_click >= self.duracion_click:
            self.boton_click = None
            necesita_actualizar = True
        if necesita_actualizar:
            self.necesita_redibujar = True

    def dibujar(self):
        if self.estado == "bienvenida":
            self.dibujar_bienvenida()
        elif self.estado == "menu":
            self.dibujar_menu_principal()
        elif self.estado == "entrada_nombre":
            self.dibujar_entrada_nombre()
        elif self.estado == "juego":
            self.dibujar_juego()
        elif self.estado == "puntuaciones":
            self.dibujar_puntuaciones()
        elif self.estado == "confirmar_borrado":
            self.dibujar_confirmar_borrado()
        elif self.estado == "info":
            self.dibujar_info()
        elif self.estado == "fin_juego":
            self.dibujar_fin_juego()
        pygame.display.flip()

    def ejecutar(self):
        reloj = pygame.time.Clock()
        ejecutando = True
        while ejecutando:
            ejecutando = self.manejar_eventos()
            if self.estado == "juego":
                self.actualizar_juego()
            else:
                tiempo_actual = pygame.time.get_ticks()
                if self.boton_click and tiempo_actual - self.tiempo_click >= self.duracion_click:
                    self.boton_click = None
                    self.necesita_redibujar = True
            estado_actual = (self.estado, self.estado_juego, self.color_iluminado, self.ultimo_color_clicado, self.boton_hover, self.boton_click)
            if estado_actual != self.ultimo_estado:
                self.necesita_redibujar = True
                self.ultimo_estado = estado_actual
            if self.necesita_redibujar:
                self.dibujar()
                self.necesita_redibujar = False
            reloj.tick(60)
        pygame.quit()
        sys.exit()

def main():
    juego = ColoresMagicosPygame()
    juego.ejecutar()

if __name__ == "__main__":
    main() 