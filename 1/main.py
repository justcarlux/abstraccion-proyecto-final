import pygame
import sys
import math
import random
from logic import LogicaSimon

pygame.init()

# --- CONFIGURACIÓN DE SONIDOS Y MÚSICA ---
MENU_MUSIC = "sounds/menu_music.mp3"
GAME_MUSIC = "sounds/game_music.mp3"
MENU_HOVER_SOUND = "sounds/menu_hover.wav"
MENU_CLICK_SOUND = "sounds/menu_click.wav"

# --- COLORES ACCESIBLES ---
BG_COLOR = (135, 206, 250)  # Azul claro, puedes cambiarlo por un fondo más agradable
ACCESSIBILITY_COLOR = (255, 223, 186)  # Color suave para ventana de accesibilidad
TEXT_COLOR = (50, 50, 70) # Dark color for good contrast

class Button:
    def __init__(self, surface, text, highlight_color, pos, dimensions, sound=None):
        self.surface = surface
        self.text = text
        self.highlight_color = highlight_color
        self.rect = pygame.Rect(
            pos[0] if pos[0] != -1 else (self.surface.get_width() / 2 - dimensions[0] / 2),
            pos[1],
            dimensions[0],
            dimensions[1]
        )
        self.font = pygame.font.SysFont("Open Sans", 30)
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.text_coords = (
            self.rect.x + dimensions[0] / 2 - self.text_surface.get_width() / 2,
            self.rect.y + dimensions[1] / 2 - self.text_surface.get_height() / 2
        )
        self.sound = sound
        self.hovered = False

    def draw(self):
        hovering = self.rect.collidepoint(pygame.mouse.get_pos())
        color = self.highlight_color if hovering else [0, 0, 0]
        pygame.draw.rect(self.surface, color, self.rect, border_radius=15)
        self.surface.blit(self.text_surface, self.text_coords)
        if hovering and not self.hovered:
            self.hovered = True
            if self.sound:
                self.sound.play()
        elif not hovering:
            self.hovered = False

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

class InputBox:
    def __init__(self, x, y, w, h, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = TEXT_COLOR  # Usar el color de texto principal para el borde
        self.color_active = (140, 120, 190)  # Un color más brillante para el estado activo
        self.color = self.color_inactive
        self.text = ''
        self.font = font
        self.txt_surface = font.render(self.text, True, TEXT_COLOR) # Usar el color de texto principal
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return self.text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 12 and event.unicode.isalnum():
                    self.text += event.unicode
            self.txt_surface = self.font.render(self.text, True, TEXT_COLOR) # Usar el color de texto principal
        return None

    def draw(self, screen):
        text_rect = self.txt_surface.get_rect(center=self.rect.center)
        screen.blit(self.txt_surface, text_rect)
        pygame.draw.rect(screen, self.color, self.rect, 2)

class SimonButton:
    def __init__(self, surface, color, highlight_color, center, radius, start_angle, stop_angle, sound=None):
        self.surface = surface
        self.color = color
        self.highlight_color = highlight_color
        self.center = center
        self.radius = radius
        self.start_angle = start_angle
        self.stop_angle = stop_angle
        self.rect = pygame.Rect(center[0] - radius, center[1] - radius, radius * 2, radius * 2)
        self.sound = sound
        self.is_highlighted = False
    
    def draw(self, surface, is_highlighted=False):
        # Más claro si está presionado
        draw_color = self.highlight_color if is_highlighted or self.is_highlighted else self.color
        pygame.draw.arc(surface, draw_color, self.rect, self.start_angle, self.stop_angle, self.radius)

    def play_sound(self):
        if self.sound:
            self.sound.play()

    def is_clicked(self, pos):
        px, py = pos
        cx, cy = self.center
        distance_sq = (px - cx)**2 + (py - cy)**2
        if not (distance_sq <= self.radius**2):
            return False
        angle = math.atan2(cy - py, px - cx)
        if angle < 0:
            angle += 2 * math.pi
        return self.start_angle <= angle < self.stop_angle

class SimonSaysGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Simon Says")
        self.running = True
        self.state = "menu"  # menu, input, game, howto, accessibility
        self.show_accessibility = False
        

        # Fondo amigable
        try:
            self.background_image = pygame.image.load("background.webp").convert()
            self.background_image = pygame.transform.scale(self.background_image, (800, 600))
        except pygame.error:
            self.background_image = pygame.Surface((800, 600))
            self.background_image.fill(BG_COLOR)

        # Cargar la imagen del título para el menú
        try:
            self.title_image = pygame.image.load("title.png").convert_alpha()
            # Opcional: escalar si es necesario
            # self.title_image = pygame.transform.scale(self.title_image, (width, height))
            self.title_rect = self.title_image.get_rect(center=(self.screen.get_width() / 2, 120))
        except pygame.error:
            self.title_image = None

        self.title_font = pygame.font.SysFont("Open Sans", 60)
        self.font = pygame.font.SysFont("Open Sans", 30)
        self.howtofont = pygame.font.SysFont("Open Sans", 20)
        self.clock = pygame.time.Clock()
        self.button_initial_y = 250
        self.button_width = 250
        self.button_height = 50
        self.button_separation = 30

        # Sonidos de menú
        try:
            self.menu_hover_sound = pygame.mixer.Sound(MENU_HOVER_SOUND)
            self.menu_click_sound = pygame.mixer.Sound(MENU_CLICK_SOUND)
            self.menu_click_sound.set_volume(0.25)
        except:
            self.menu_hover_sound = self.menu_click_sound = None
        sonido  = pygame.mixer.Sound(MENU_HOVER_SOUND)
        sonido.set_volume(0.2)

        self.play_button = Button(self.screen, "Jugar", (76, 175, 80), (-1, self.button_initial_y), (self.button_width, self.button_height), sonido)
        self.howto_button = Button(self.screen, "Cómo se juega", (33, 150, 243), (-1, self.button_initial_y + self.button_height + self.button_separation), (self.button_width, self.button_height), sonido)
        self.close_button = Button(self.screen, "Salir", (244, 67, 54), (-1, self.button_initial_y + self.button_height * 2 + self.button_separation * 2), (self.button_width, self.button_height), sonido)
        self.input_box = InputBox(300, 300, 200, 40, self.font)
        self.username = ""
        self.error_message = ""
        self.score = 0

        # --- Simon Game Setup ---
        try:
            green_sound = pygame.mixer.Sound("sounds/f_sharp.wav")
            green_sound.set_volume(0.9)
            red_sound = pygame.mixer.Sound("sounds/c_sharp.wav")
            red_sound.set_volume(0.9)
            yellow_sound = pygame.mixer.Sound("sounds/a_sharp.wav")
            yellow_sound.set_volume(0.9)
            blue_sound = pygame.mixer.Sound("sounds/d_sharp.wav")
            blue_sound.set_volume(0.9)
        except pygame.error:
            green_sound = red_sound = yellow_sound = blue_sound = None

        simon_center = (self.screen.get_width() // 2, self.screen.get_height() // 2 + 50)
        simon_radius = 200
        inner_radius_ratio = 0.45
        self.simon_center_hub_radius = int(simon_radius * inner_radius_ratio)

        self.simon_logo_font = pygame.font.SysFont("Arial Black", 50)
        self.simon_logo_surface = self.simon_logo_font.render("SIMON", True, (255, 255, 255))
        self.simon_logo_rect = self.simon_logo_surface.get_rect(center=simon_center)

        self.simon_buttons = [
            SimonButton(self.screen, (0, 155, 0), (120, 255, 120), simon_center, simon_radius, math.pi / 2, math.pi, green_sound),
            SimonButton(self.screen, (155, 0, 0), (255, 120, 120), simon_center, simon_radius, 0, math.pi / 2, red_sound),
            SimonButton(self.screen, (155, 155, 0), (255, 255, 120), simon_center, simon_radius, math.pi, 3 * math.pi / 2, yellow_sound),
            SimonButton(self.screen, (0, 0, 155), (120, 120, 255), simon_center, simon_radius, 3 * math.pi / 2, 2 * math.pi, blue_sound),
        ]
        self.logica = LogicaSimon(self.simon_buttons, self.screen)
        self.fuente = pygame.font.SysFont("Arial Black", 20)  # Fuente para mostrar nivel/puntaje
        self.boton_flash = None
        self.tiempo_flash = 0
        
        # Botón de volver
        self.back_button = Button(self.screen, "Volver", (100, 100, 100), (self.screen.get_width() - 140, 20), (120, 40), sonido)

        # Imagen y texto para "Cómo se juega"
        try:
            self.howto_img = pygame.image.load("howto.png").convert_alpha()
        except:
            self.howto_img = None

        self.howto_text = [
            "El juego Simon Says muestra una secuencia de colores.",
            "Debes repetir la secuencia tocando los botones de colores.",
            "Cada ronda la secuencia se hace más larga.",
            "¡Intenta recordar y repetir la secuencia correctamente!"
        ]

        # Música
        pygame.mixer.music.load(MENU_MUSIC)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.25)  # Valores entre 0.0 (mute) y 1.0 (máximo)


    def switch_music(self, music_file):
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1)

    def run(self):
        while self.running:
            self.screen.blit(self.background_image, (0, 0))
            # Mostrar botón de accesibilidad solo en el menú principal
            if self.state == "menu":
                self.draw_accessibility_button()
            if self.show_accessibility:
                self.draw_accessibility_window()
            elif self.state == "menu":
                self.draw_menu()
            elif self.state == "input":
                self.draw_input()
            elif self.state == "game":
                self.draw_game()
            elif self.state == "howto":
                self.draw_howto()
            pygame.display.flip()
            self.clock.tick(60)

    def draw_accessibility_button(self):
        # Hide the button on "howto" screen
        if self.state == "howto":
            return
        pygame.draw.circle(self.screen, (255, 200, 0), (30, 30), 20)
        font = pygame.font.SysFont("Arial", 18, bold=True)
        txt = font.render("i", True, (0, 0, 0))
        txt_rect = txt.get_rect(center=(30, 30))
        self.screen.blit(txt, txt_rect)

    def draw_accessibility_window(self):
        # Create a semi-transparent surface for the pop-up
        surf = pygame.Surface((650, 250), pygame.SRCALPHA)
        # Draw the box with rounded corners and padding
        pygame.draw.rect(surf, (*ACCESSIBILITY_COLOR, 240), surf.get_rect(), border_radius=15)
        pygame.draw.rect(surf, (0, 0, 0), surf.get_rect(), 3, border_radius=15)

        font = pygame.font.SysFont("Arial", 22, bold=True)
        lines = [
            "Este juego está diseñado para personas con autismo,",
            "TDAH u otras condiciones que se benefician de juegos",
            "kinestésicos y de memoria. Los colores y sonidos",
            "fueron seleccionados para ser agradables y no invasivos.",
            "",
            "¡Esperamos que disfrutes la experiencia!"
        ]

        # Set initial y position for the text
        y_offset = 30
        for i, line in enumerate(lines):
            txt_surface = font.render(line, True, (0, 0, 0))
            # Center each line of text horizontally inside the surface
            txt_rect = txt_surface.get_rect(centerx=surf.get_width() / 2, y=y_offset)
            surf.blit(txt_surface, txt_rect)
            y_offset += 30 # Move to the next line

        # Center the pop-up on the screen
        screen_rect = self.screen.get_rect()
        surf_rect = surf.get_rect(center=screen_rect.center)
        self.screen.blit(surf, surf_rect)

        # Cerrar ventana accesibilidad
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.show_accessibility = False

    def draw_menu(self):
        # Usar la imagen del título si está disponible
        if self.title_image:
            self.screen.blit(self.title_image, self.title_rect)
        else:
            # Fallback a texto si la imagen no carga
            title_surface = self.title_font.render("Simon Says", True, TEXT_COLOR)
            self.screen.blit(title_surface, (self.screen.get_width() // 2 - title_surface.get_width() // 2, 100))

        self.play_button.draw()
        self.howto_button.draw()
        self.close_button.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.play_button.is_clicked(event):
                if self.menu_click_sound:
                    self.menu_click_sound.play()
                self.switch_music(GAME_MUSIC)
                self.state = "input"
            elif self.howto_button.is_clicked(event):
                if self.menu_click_sound:
                    self.menu_click_sound.play()
                self.state = "howto"
            elif self.close_button.is_clicked(event):
                if self.menu_click_sound:
                    self.menu_click_sound.play()
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Accesibilidad
                if pygame.Rect(10, 10, 40, 40).collidepoint(event.pos):
                    self.show_accessibility = True

    def draw_input(self):
        prompt = self.font.render("Ingresa tu nombre:", True, TEXT_COLOR)
        self.screen.blit(prompt, (self.screen.get_width() // 2 - prompt.get_width() // 2, 250))
        self.input_box.draw(self.screen)
        if self.error_message:
            error_surface = self.font.render(self.error_message, True, (255, 0, 0))
            self.screen.blit(error_surface, (self.screen.get_width() // 2 - error_surface.get_width() // 2, 350))
        self.back_button.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            result = self.input_box.handle_event(event)
            if result is not None:
                if not result or not result.isalnum():
                    self.error_message = "Nombre inválido. Solo letras y números."
                else:
                    self.username = result
                    self.error_message = ""
                    self.state = "game"
            if self.back_button.is_clicked(event):
                self.switch_music(MENU_MUSIC)
                self.state = "menu"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(10, 10, 40, 40).collidepoint(event.pos):
                    self.show_accessibility = True

    def draw_game(self):
        self.screen.blit(self.background_image, (0, 0))
        title_surface = self.title_font.render("Simon Says", True, TEXT_COLOR)
        self.screen.blit(title_surface, (self.screen.get_width() // 2 - title_surface.get_width() // 2, 20))
        self.back_button.draw()
        
        if self.username:
            user_surface = self.font.render(f"Jugador: {self.username}", True, TEXT_COLOR)
            self.screen.blit(user_surface, (20, 75))

        if self.logica.estado == "esperando":
            self.logica.iniciar_nueva_ronda()
            
        self.logica.actualizar()

        # --- Simon Toy ---
        for btn in self.simon_buttons:
            btn.draw(self.screen, btn.is_highlighted)
        pygame.draw.circle(self.screen, (0, 0, 0), self.simon_buttons[0].center, self.simon_center_hub_radius)
        self.screen.blit(self.simon_logo_surface, self.simon_logo_rect)
        self.back_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.logica.estado == "jugando":
                    for boton in self.simon_buttons:
                        if boton.is_clicked(event.pos):
                            boton.is_highlighted = True
                            boton.play_sound()
                        
                            for b in self.simon_buttons:
                                b.draw(self.screen, b.is_highlighted)
                                pygame.draw.circle(self.screen, (0, 0, 0), self.simon_buttons[0].center, self.simon_center_hub_radius)
                                titulo = self.simon_logo_font.render("SIMON", True, (255, 255, 255))
                                self.screen.blit(titulo, (400 - titulo.get_width() // 2, 350 - titulo.get_height() // 2))
                                self.logica.mostrar_nivel(self.fuente)
                                self.logica.mostrar_puntaje(self.fuente)

                            pygame.display.flip()
                            pygame.time.delay(150)

                            boton.is_highlighted = False

                            resultado = self.logica.registrar_clic(boton)
                            if resultado == "perdio":
                                print("¡Perdiste!")
                                self.logica.reiniciar_juego()
                            elif resultado == "nivel_completado":
                                print("¡Nivel superado!")
                                pygame.time.delay(50)
                if self.back_button.is_clicked(event):
                    self.switch_music(MENU_MUSIC)
                    self.state = "menu"

        self.logica.mostrar_nivel(self.fuente)
        self.logica.mostrar_puntaje(self.fuente)
        

    def draw_howto(self):
        settings_title = self.font.render("Cómo se juega", True, TEXT_COLOR)
        self.screen.blit(settings_title, (self.screen.get_width() // 2 - settings_title.get_width() // 2, 60))
        if self.howto_img:
            self.screen.blit(self.howto_img, (0, 0))
        for i, line in enumerate(self.howto_text):
            txt = self.howtofont.render(line, True, TEXT_COLOR)
            self.screen.blit(txt, (self.screen.get_width() // 2 - txt.get_width() // 2, 198 + i * 30))
        self.back_button.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.back_button.is_clicked(event):
                self.state = "menu"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(10, 10, 40, 40).collidepoint(event.pos):
                    self.show_accessibility = True

if __name__ == "__main__":
    game = SimonSaysGame()
    game.run()
