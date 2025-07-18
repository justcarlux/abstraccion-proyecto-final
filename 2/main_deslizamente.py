import pygame
from opciones_deslizamente import *
import sys
from constantes_deslizamente import *

pygame.mixer.init()

class Menu():
    def __init__(self):
        pygame.init()

        self.pantalla = pygame.display.set_mode((ANCHO,ALTO))
        pygame.display.set_caption("Deslizamente")

        self.fuente_titulo = pygame.font.SysFont("Consolas", 50)
        self.fuente_boton= pygame.font.SysFont("Consolas", 25)
        self.fuente_texto= pygame.font.SysFont("Consolas", 20)

        self.b_jugar = pygame.Rect(ANCHO/2 - 100, ALTO / 2 - 70 , 200, 50)
        self.b_instruc = pygame.Rect(ANCHO/2 - 100, ALTO / 2 -70 + 70, 200, 50)
        self.b_salir = pygame.Rect(ANCHO/2 - 100, ALTO / 2 - 70 + 140, 200, 50)


        #Música de fondo
        pygame.mixer.music.load("Soundtrack-inicio.mp3")
        pygame.mixer.music.play(-1)
        #Booleano que controla si el soundtrack se reproduce o no
        self.Musica = True




    def dibujar_menu(self, img_icono_sonido):
           fondo = pygame.image.load("Fondo_inicio.jpg")
           fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
           self.pantalla.blit(fondo, (0,0))
           text_til = self.fuente_titulo.render("Deslizamente", True, BLANCO)
           self.pantalla.blit(text_til, (ANCHO // 2- text_til.get_width() // 2,80))

           color = Cambiar_color_boton(self.b_jugar, VERDE, VERDE_CAMBIO)
           pygame.draw.rect(self.pantalla, color, self.b_jugar)
           self.text_jugar = self.fuente_boton.render("Jugar", True, BLANCO)
           self.pantalla.blit(self.text_jugar, (self.b_jugar.x + self.b_jugar.width // 2 - self.text_jugar.get_width() // 2,self.b_jugar.y + self.b_jugar.height // 2 - self.text_jugar.get_height() // 2))

           color = Cambiar_color_boton(self.b_instruc, AZUL, AZUL_CAMBIO)
           pygame.draw.rect(self.pantalla, color, self.b_instruc)
           text_instruc = self.fuente_boton.render("Instrucciones", True, BLANCO)
           self.pantalla.blit(text_instruc, (self.b_instruc.x + self.b_instruc.width //2 - text_instruc.get_width() // 2, self.b_instruc.y + self.b_instruc.height // 2 - text_instruc.get_height() //2))

           color = Cambiar_color_boton(self.b_salir, ROJO, ROJO_CAMBIO)
           pygame.draw.rect(self.pantalla, color, self.b_salir)
           text_salir = self.fuente_boton.render("Salir", True, BLANCO)
           self.pantalla.blit(text_salir, (self.b_salir.x + self.b_salir.width // 2 - text_salir.get_width() // 2, self.b_salir.y + self.b_salir.height // 2 - text_salir.get_height() // 2))
           



           icono_sonido = pygame.image.load(img_icono_sonido)
           icono_sonido = pygame.transform.scale(icono_sonido, (80, 80))
           self.pantalla.blit(icono_sonido, (ANCHO-80, 0))


           pygame.display.flip()

            
    def mostrar_menu(self):
        cuadro_sonido = pygame.rect.Rect(ANCHO-80, 0, 80, 80)
        ejecutando =  True
        img_icono_sonido = "icono_sonido.png"
        while ejecutando:
            self.dibujar_menu(img_icono_sonido)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.b_jugar.collidepoint(evento.pos):
                        click_boton()
                        modo = Modos()
                        modo.Menu(self.Musica)
                        self.dibujar_menu(img_icono_sonido)
                    if self.b_instruc.collidepoint(evento.pos):
                        click_boton()
                        self.ventana_instrucciones()

                    if self.b_salir.collidepoint(evento.pos):
                        click_boton()
                        ejecutando= False

                    if cuadro_sonido.collidepoint(evento.pos):
                        if self.Musica:
                            img_icono_sonido = "icono_mute.png"
                            pygame.mixer.music.stop()
                            self.Musica = False
                    
                        else:
                            img_icono_sonido = "icono_sonido.png"
                            pygame.mixer.music.load("Soundtrack-inicio.mp3")
                            pygame.mixer.music.play(-1)
                            self.Musica = True
                        


        pygame.quit()

    
    def ventana_instrucciones(self):
        fuente_inst =  pygame.font.SysFont("Consolas", 20)
        fuente_bot = pygame.font.SysFont("Consolas", 20)
        fondo = pygame.image.load("fondo_instrucciones.jpg")
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
        en_instrucciones = True
        
        while en_instrucciones:
        
            self.pantalla.blit(fondo, (0,0))

            text_titulo = self.fuente_titulo.render("Instrucciones", True, BLANCO)
            self.pantalla.blit(text_titulo, (ANCHO //2 -text_titulo.get_width() // 2, 50))
            
            y_texto = 150
            for instruccion in INSTRUCCIONES:
                lineas  = instruccion.split("\n")

                for linea in lineas:
                    texto = fuente_inst.render(linea, True, NEGRO)
                    self.pantalla.blit(texto, (ANCHO// 2 - texto.get_width() // 2, y_texto))
                    y_texto+=45
                y_texto+= 30
                """texto =  fuente_inst.render(instruccion, True, NEGRO)
                self.pantalla.blit(texto, (ANCHO// 2 - texto.get_width() //2, y_texto))
                y_texto += 45"""
            
            b_regresar = pygame.Rect(ANCHO/2 - 100, y_texto + 30 , 200, 50)
            color = Cambiar_color_boton(b_regresar, ROJO, ROJO_CAMBIO)
            pygame.draw.rect(self.pantalla, color, b_regresar)
            text_regresar = fuente_bot.render("Regresar", True, BLANCO)
            self.pantalla.blit(text_regresar, (b_regresar.x + b_regresar.width // 2 - text_regresar.get_width() // 2, b_regresar.y + b_regresar.height// 2 - text_regresar.get_height() // 2))
            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    sys.exit()
                    
                    pygame.quit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if b_regresar.collidepoint(evento.pos):
                        
                        en_instrucciones = False

            
                

pygame.mixer.quit()            