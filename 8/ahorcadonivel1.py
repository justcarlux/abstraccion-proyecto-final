import pygame
import random
import os
from constantes import ANCHO, ALTO, Colores, Tipografia
from palabras import PALABRAS_NIVEL1  # type: ignore

class AhorcadoNivel1:
    def __init__(self, fondo, aleatorio=True):
        self.fondo = fondo
        self.max_rondas = 7
        self.errores = 0
        self.max_errores = 5  # Ahora máximo 9 errores para 10 imágenes
        self.monedas = 0
        self.pistas_restantes = 3
        self.consec_aciertos = 0
        self.juego_activo = True
        self.terminado = False
        self.nivel_completado = False
        self.mostrar_opciones = False
        self.mostrar_pista = False
        self.mensaje_fin = ""
        self.indice_pista = 0

        # Cargar sonido con ruta segura
        ruta_sonido = os.path.join(os.path.dirname(__file__), "sonidos", "sonidodeboton.mp3")
        self.sonido_boton = pygame.mixer.Sound(ruta_sonido)

        self.ronda_actual = 0
        self.letras_adivinadas = set()
        self.letras_falladas = set()

        self.fuente_grande = pygame.font.SysFont(Tipografia.FUENTE, Tipografia.TAMAÑO_TITULO)
        self.fuente_mediana = pygame.font.SysFont(Tipografia.FUENTE, Tipografia.TAMAÑO_TEXTO)
        self.fuente_pequena = pygame.font.SysFont(Tipografia.FUENTE, 20)

        # Palabras en orden o al azar
        self.palabras = random.sample(PALABRAS_NIVEL1, self.max_rondas) if aleatorio else PALABRAS_NIVEL1[:self.max_rondas]

        self.teclado = self.crear_teclado()
        self.cargar_palabra()

        self.tiempo_inicio = pygame.time.get_ticks()

        self.rect_boton_monedas = pygame.Rect(ANCHO - 200, 20, 130, 40)
        self.rect_opcion_letra = pygame.Rect(ANCHO - 330, 70, 300, 50)  # Más ancho
        self.rect_opcion_pista = pygame.Rect(ANCHO - 330, 130, 300, 50)  # Más ancho

        # Cargar imágenes superpuestas
        carpeta_imagenes = os.path.join(os.path.dirname(__file__), "imagenes")
        self.imagenes_ahorcado = []
        for i in range(6):  # capas 0 a 9
            ruta = os.path.join(carpeta_imagenes, f"imagen{i}.jpg")
            imagen = pygame.image.load(ruta).convert_alpha()
            imagen = pygame.transform.scale(imagen, (200, 200))
            self.imagenes_ahorcado.append(imagen)

    def crear_teclado(self):
        teclado = {}
        filas = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        x_inicial = ANCHO // 2 - 250
        y_inicial = ALTO - 250
        espacio_x = 55
        espacio_y = 60
        for fila_idx, fila in enumerate(filas):
            x = x_inicial + (27 * fila_idx)
            y = y_inicial + fila_idx * espacio_y
            for letra in fila:
                teclado[letra] = pygame.Rect(x, y, 50, 50)
                x += espacio_x
        return teclado

    def cargar_palabra(self):
        if self.ronda_actual >= self.max_rondas:
            self.terminar_juego(True)
            return
        entrada = self.palabras[self.ronda_actual]
        self.palabra = entrada["palabra"].upper()
        self.pistas = [entrada["pista"]]  # Puedes modificar para lista si quieres más pistas
        self.pista_actual_index = 0

        self.letras_adivinadas.clear()
        self.letras_falladas.clear()
        self.errores = 0
        self.consec_aciertos = 0
        self.juego_activo = True
        self.terminado = False
        self.mostrar_opciones = False
        self.mostrar_pista = False
        self.tiempo_inicio = pygame.time.get_ticks()

    def manejar_evento(self, evento):
        if self.terminado:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    self.__init__(self.fondo)  # Reiniciar todo el nivel
                elif evento.key == pygame.K_m:
                    return "menu_niveles"  # Devuelve para ir a menú de niveles
            return None

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return "menu_principal"
            letra = evento.unicode.upper()
            if letra in self.teclado:
                if letra not in self.letras_adivinadas and letra not in self.letras_falladas:
                    self.sonido_boton.play()  # Sonido botón tecla
                    self.procesar_letra(letra)

        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pos = evento.pos
            if self.rect_boton_monedas.collidepoint(pos):
                self.sonido_boton.play()  # Sonido botón monedas
                self.mostrar_opciones = not self.mostrar_opciones
                return None

            if self.mostrar_opciones:
                fuera = not (
                    self.rect_opcion_letra.collidepoint(pos) or
                    self.rect_opcion_pista.collidepoint(pos) or
                    self.rect_boton_monedas.collidepoint(pos)
                )
                if fuera:
                    self.mostrar_opciones = False
                    return None

                if self.rect_opcion_letra.collidepoint(pos):
                    if self.monedas >= 1:
                        self.sonido_boton.play()  # Sonido usar pista letra
                        self.revelar_letra()
                        self.monedas -= 1
                        self.mostrar_opciones = False
                    return None

                if self.rect_opcion_pista.collidepoint(pos):
                    if self.monedas >= 2 and self.pistas_restantes > 0:
                        self.sonido_boton.play()  # Sonido usar pista pista
                        self.pistas_restantes -= 1
                        self.monedas -= 2
                        self.mostrar_pista = True
                        self.mostrar_opciones = False
                    return None

            for letra, rect in self.teclado.items():
                if rect.collidepoint(pos):
                    if letra not in self.letras_adivinadas and letra not in self.letras_falladas:
                        self.sonido_boton.play()  # Sonido tecla clic
                        self.procesar_letra(letra)

    def procesar_letra(self, letra):
        if letra in self.palabra:
            self.letras_adivinadas.add(letra)
            self.consec_aciertos += 1
            if self.consec_aciertos == 2:
                self.monedas += 1
                self.consec_aciertos = 0
        else:
            self.letras_falladas.add(letra)
            self.errores += 1
            self.consec_aciertos = 0
        self.verificar_estado()

    def verificar_estado(self):
        if all(l in self.letras_adivinadas for l in set(self.palabra)):
            self.ronda_actual += 1
            if self.ronda_actual >= self.max_rondas:
                self.terminar_juego(True)
            else:
                self.cargar_palabra()
                self.mostrar_pista = False
        elif self.errores >= self.max_errores:
            self.terminar_juego(False)

    def revelar_letra(self):
        no_adivinadas = [l for l in set(self.palabra) if l not in self.letras_adivinadas]
        if no_adivinadas:
            letra = random.choice(no_adivinadas)
            self.letras_adivinadas.add(letra)
            self.verificar_estado()

    def terminar_juego(self, gano):
        self.terminado = True
        self.juego_activo = False
        if gano:
            self.nivel_completado = True
        else:
            self.mensaje_fin = "Perdiste. Presiona R para reiniciar o M para menú."

    def actualizar(self, pantalla):
        if self.terminado:
            return
        tiempo_transcurrido = (pygame.time.get_ticks() - self.tiempo_inicio) // 1000
        if tiempo_transcurrido >= 60:
            self.terminar_juego(False)

    def dibujar_texto(self, pantalla, texto, x, y, color=Colores.AZUL_OSCURO, fuente=None):
        fuente = fuente or self.fuente_mediana
        render = fuente.render(texto, True, color)
        pantalla.blit(render, (x, y))

    def dibujar(self, pantalla):
        self.fondo.dibujar(pantalla)

        # Dibujar imágenes superpuestas según errores
        if not self.nivel_completado:
            for i in range(min(self.errores + 1, len(self.imagenes_ahorcado))):
                pantalla.blit(self.imagenes_ahorcado[i], (ANCHO - 745, 0))

        if self.nivel_completado:
            fuente = pygame.font.SysFont(Tipografia.FUENTE, 40)
            mensaje = "¡Felicidades! Completaste el nivel."
            sub = "Presiona R para reiniciar o M para volver al menú"
            texto1 = fuente.render(mensaje, True, Colores.BLANCO)
            texto2 = fuente.render(sub, True, Colores.GRIS_OSCURO)
            pantalla.blit(texto1, (ANCHO // 2 - texto1.get_width() // 2, ALTO // 2 - 40))
            pantalla.blit(texto2, (ANCHO // 2 - texto2.get_width() // 2, ALTO // 2 + 20))
            return

        # Información izquierda
        self.dibujar_texto(pantalla, f"Ronda: {self.ronda_actual + 1} / {self.max_rondas}", 20, 20)
        self.dibujar_texto(pantalla, f"Errores: {self.errores} / {self.max_errores}", 20, 60)
        self.dibujar_texto(pantalla, f"Monedas: {self.monedas}", 20, 100)
        self.dibujar_texto(pantalla, f"Pistas restantes: {self.pistas_restantes}", 20, 140)
        tiempo_restante = max(0, 60 - (pygame.time.get_ticks() - self.tiempo_inicio) // 1000)
        self.dibujar_texto(pantalla, f"Tiempo: {tiempo_restante}s", 20, 180, Colores.AZUL)

        # Palabra adivinada centrada
        palabra_mostrada = " ".join([l if l in self.letras_adivinadas else "_" for l in self.palabra])
        render_palabra = self.fuente_grande.render(palabra_mostrada, True, Colores.AZUL_OSCURO)
        x_palabra = (ANCHO - render_palabra.get_width()) // 2
        y_palabra = ALTO // 2 - 50
        pantalla.blit(render_palabra, (x_palabra, y_palabra))

        # Pista centrada debajo de la palabra
        if self.mostrar_pista and self.indice_pista > 0:
            texto_pista = f"Pista: {self.pistas[self.indice_pista - 1]}"
            render_pista = self.fuente_mediana.render(texto_pista, True, Colores.NEGRO)
            x_pista = (ANCHO - render_pista.get_width()) // 2
            y_pista = ALTO // 2 - 10 + self.fuente_grande.get_height()  # Justo debajo de la palabra
            pantalla.blit(render_pista, (x_pista, y_pista))

        # Teclado visual
        for letra, rect in self.teclado.items():
            color = (180, 180, 180)
            if letra in self.letras_adivinadas:
                color = Colores.VERDE_CLARO
            elif letra in self.letras_falladas:
                color = (255, 100, 100)
            pygame.draw.rect(pantalla, color, rect, border_radius=8)
            render = self.fuente_pequena.render(letra, True, Colores.NEGRO)
            pantalla.blit(render, (rect.x + 12, rect.y + 8))

        # Botón monedas
        pygame.draw.rect(pantalla, Colores.AZUL, self.rect_boton_monedas, border_radius=10)
        self.dibujar_texto(pantalla, "💰 Opciones", self.rect_boton_monedas.x + 10, self.rect_boton_monedas.y + 7, Colores.BLANCO, self.fuente_pequena)

        # Opciones monedas desplegadas
        if self.mostrar_opciones:
            pygame.draw.rect(pantalla, Colores.AZUL_OSCURO, self.rect_opcion_letra, border_radius=10)
            self.dibujar_texto(pantalla, "Descubrir letra (1 moneda)", self.rect_opcion_letra.x + 10, self.rect_opcion_letra.y + 7, Colores.BLANCO, self.fuente_pequena)

            pygame.draw.rect(pantalla, Colores.AZUL_OSCURO, self.rect_opcion_pista, border_radius=10)
            self.dibujar_texto(pantalla, f"Dar pista (2 monedas) [{self.pistas_restantes}]", self.rect_opcion_pista.x + 10, self.rect_opcion_pista.y + 7, Colores.BLANCO, self.fuente_pequena)

        # Mensaje final de perder
        if self.terminado and not self.nivel_completado:
            ancho_mensaje = self.fuente_mediana.size(self.mensaje_fin)[0]
            self.dibujar_texto(
                pantalla,
                self.mensaje_fin,
                ANCHO // 2 - ancho_mensaje // 2,
                ALTO // 2 + 50,
                Colores.AZUL,
                self.fuente_mediana
            )