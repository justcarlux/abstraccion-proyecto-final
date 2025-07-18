import random
import pygame

class LogicaSimon:
    def __init__(self, botones, pantalla):
        self.botones = botones  # Lista de botones visuales (SimonButton)
        self.pantalla = pantalla
        self.secuencia = []  # Secuencia generada por el juego
        self.input_jugador = []  # Clics del jugador
        self.nivel = 1
        self.puntaje = 0
        self.estado = "esperando"  # puede ser: 'esperando', 'mostrando', 'jugando', 'perdido'

        # Control de tiempo para reproducir la secuencia
        self.mostrando_secuencia = False
        self.indice_secuencia = 0
        self.tiempo_ultimo_flash = 0
        self.tiempo_entre_flashes = 700  # milisegundos
        self.tiempo_duracion_flash = 400
        self.flash_activo = False

    def iniciar_nueva_ronda(self):
        nuevo_boton = random.choice(self.botones)
        self.secuencia.append(nuevo_boton)
        self.input_jugador = []
        self.indice_secuencia = 0
        self.estado = "mostrando"
        self.mostrando_secuencia = True
        self.tiempo_ultimo_flash = pygame.time.get_ticks()
        self.flash_activo = False
        for boton in self.botones:
            boton.is_highlighted = False

    def actualizar(self):
        if self.estado == "mostrando":
            self.reproducir_secuencia()
        elif self.estado == "jugando":
            pass  # en este estado, el main controla los clics

    def reproducir_secuencia(self):
        tiempo_actual = pygame.time.get_ticks()
        
        if self.indice_secuencia < len(self.secuencia):
            if not self.flash_activo and tiempo_actual - self.tiempo_ultimo_flash >= self.tiempo_entre_flashes:
                # Activar flash
                boton = self.secuencia[self.indice_secuencia]
                boton.is_highlighted = True
                boton.play_sound()
                self.tiempo_ultimo_flash = tiempo_actual
                self.flash_activo = True

            elif self.flash_activo and tiempo_actual - self.tiempo_ultimo_flash >= self.tiempo_duracion_flash:
                # Apagar flash
                self.secuencia[self.indice_secuencia].encendido = False
                self.indice_secuencia += 1
                self.tiempo_ultimo_flash = tiempo_actual
                self.flash_activo = False
                for boton in self.botones:
                    boton.is_highlighted = False
        else:
            # Fin de reproducción
            self.mostrando_secuencia = False
            self.estado = "jugando"
            self.indice_secuencia = 0
            for boton in self.botones:
                boton.is_highlighted = False

    def registrar_clic(self, boton_clicado):
        if self.estado != "jugando":
            return

        self.input_jugador.append(boton_clicado)

        # Verificar si el clic fue correcto
        indice = len(self.input_jugador) - 1
        if self.input_jugador[indice] != self.secuencia[indice]:
            self.estado = "perdido"
            return "perdio"

        if len(self.input_jugador) == len(self.secuencia):
            self.nivel += 1
            self.puntaje += 10
            self.estado = "esperando"
            return "nivel_completado"

        return "correcto"

    def reiniciar_juego(self):
        self.secuencia = []
        self.input_jugador = []
        self.nivel = 1
        self.puntaje = 0
        self.estado = "esperando"
        self.indice_secuencia = 0
        self.mostrando_secuencia = False
        self.flash_activo = False
        for boton in self.botones:
            boton.is_highlighted = False

    def mostrar_nivel(self, fuente):
        texto = fuente.render(f"Nivel: {self.nivel}", True, (50, 50, 70))
        self.pantalla.blit(texto, (20, 10))

    def mostrar_puntaje(self, fuente):
        texto = fuente.render(f"Puntaje: {self.puntaje}", True, (50, 50, 70))
        self.pantalla.blit(texto, (20, 41))