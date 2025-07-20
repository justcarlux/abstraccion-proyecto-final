import pygame
from constantes_deslizamente import *
from game_deslizamente import Cambiar_color_boton
from main_deslizamente import Menu

pygame.init()
class DeslizamenteIntro():
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Deslizamente")
        self.fondoOrg = pygame.image.load("fondo_intro.jpg").convert_alpha()
        self.fondo =  pygame.transform.scale(self.fondoOrg, (ANCHO,ALTO))
        self.fuente_titulo = pygame.font.SysFont("Consolas", 30)
        self.fuente_titulo2 = pygame.font.SysFont("Consolas", 40)
        self.fuente_texto = pygame.font.SysFont("Consolas", 18)
        self.fuente_boton = pygame.font.SysFont("Consolas", 20)

        self.b_siguiente = pygame.Rect(ANCHO // 2 - 200, ALTO -90, 160, 45)
        self.b_salir = pygame.Rect(ANCHO // 2 - 20, ALTO-90, 160, 45)
        self.opciones = ["¿Que es deslizamente?", "Objetivo del juego", "¿Quienes pueden jugar?", "Capacidades que desarrolla"]
        self.ops = {
            "¿Que es deslizamente?": "Deslizamente es un juego de lógica y estrategia mental, donde debes mover piezas dentro de una cuadrícula \npara reconstruir una imagen. Solo puedes deslizar piezas adyacentes al espacio vacío.",
            "Objetivo del juego": "Organiza correctamente todas las piezas en su lugar, moviéndolas una a una. Planifica, anticipa y completa la imagen.",
            "¿Quienes pueden jugar?": "Este juego está diseñado para niños, jóvenes, adultos y personas con alguna condición cognitiva o motriz que \ndeseen ejercitar su mente. Es accesible y adaptable para todos los públicos que busquen mejorar su concentración\ny razonamiento lógico.",
            "Capacidades que desarrolla": "Este juego fortalece:\n\n- Razonamiento espacial\n- Planeación estratégica \n- Memoria de trabajo \n- Resolución de problemas \n- Atención sostenida"   
        }
    def dibujar_intro(self):
        self.pantalla.blit(self.fondo, (0,0))

        titulo = self.fuente_titulo2.render("Bienvenido a Deslizamente", True, NEGRO)
        self.pantalla.blit(titulo, (ANCHO // 2 -titulo.get_width() //2, 30))
        space = 30
        y_texto = 110

        for opcion in self.opciones:
            #(0, 102, 0)
            titulo = self.fuente_titulo.render(opcion, True, (0, 0, 153))
            self.pantalla.blit(titulo, (50, y_texto))
            y_texto+=40
            lineas = self.ops[opcion].split("\n")
            for linea in lineas:
                texto = self.fuente_texto.render(linea, True, NEGRO)
                self.pantalla.blit(texto,(70, y_texto))
                y_texto+=20
            y_texto +=20

        color = Cambiar_color_boton(self.b_siguiente, VERDE, VERDE_CAMBIO)
        pygame.draw.rect(self.pantalla, color, self.b_siguiente)
        texto_boton = self.fuente_boton.render("SIGUIENTE", True, BLANCO)
        self.pantalla.blit(texto_boton, (self.b_siguiente.centerx -  texto_boton.get_width() // 2, self.b_siguiente.centery - texto_boton.get_height() //2))
        
        color = Cambiar_color_boton(self.b_salir, ROJO, ROJO_CAMBIO)
        pygame.draw.rect(self.pantalla,color, self.b_salir)
        text_b_salir = self.fuente_boton.render("SALIR", True, BLANCO)
        self.pantalla.blit(text_b_salir,(self.b_salir.centerx - text_b_salir.get_width() //2, self.b_salir.centery - text_b_salir.get_height() //2) )
        
        
        
        pygame.display.flip()
    def mostrar(self):
        mostrando = True
        while mostrando:
            self.dibujar_intro()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    mostrando = False
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if self.b_siguiente.collidepoint(e.pos):
                        mostrando = False
                        men = Menu()
                        men.mostrar_menu()
                    elif self.b_salir.collidepoint(e.pos):
                        mostrando = False
des = DeslizamenteIntro()
des.mostrar()
