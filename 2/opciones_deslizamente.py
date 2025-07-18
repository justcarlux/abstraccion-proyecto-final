import pygame
import sys
from constantes_deslizamente import *
from game_deslizamente import *

#Submenú de opciones de juego
pygame.init()
class Modos:
    def __init__(self): #Pasar fondo como parámetro en el futuro
        #Pantalla
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))

        #Fondo de la pantalla
        self.fondo = pygame.image.load("Fondo_Opciones.jpg")
        

        #Tipo de letra de los botones y los títulos
        self.fuente_opciones = pygame.font.SysFont("consolas", 20)
        self.fuente_titulo = pygame.font.SysFont("consolas", 50)
        self.fuente_boton= pygame.font.SysFont("consolas", 25)

        #Declaración de los botones
        self.b_simple = pygame.Rect(ANCHO/2 - 100, ALTO / 2 + 50, 200, 50)
        self.b_contrarreloj = pygame.Rect(ANCHO/2 - 100, ALTO / 2 + 150, 200, 50)
        self.b_atras = pygame.Rect(0, 0, 200, 50) #Esquina superior izquierda


        self.b_facil = pygame.Rect(ANCHO/2 - 100, ALTO / 2 - 70 , 200, 50)
        self.b_intermedio = pygame.Rect(ANCHO/2 - 100, ALTO / 2 -70 + 70, 200, 50)
        self.b_dificil = pygame.Rect(ANCHO/2 - 100, ALTO / 2 - 70 + 140, 200, 50)

        #Color de los botones
        self.color_boton = VERDE 

        #Imagenes preestablecidas

        self.imagenes = imagenes
        self.miniaturas = []
        self.posiciones_min = []
        self.espaciado = ANCHO // 16
        self.margen_x = 40
        self.margen_y = ANCHO // 4
        #Cargando imágenes
        for i in range(0, 8):
            self.miniaturas.append(imagenes[i])
            self.miniaturas[i] = pygame.transform.smoothscale(self.miniaturas[i], (140, 140))
        
        self.tam_miniatura = 140 #Tamaño de las miniaturas, tanto horizontal, como vertical
        
        for i in range(2):
            for j in range(4):
                x = self.margen_x + j * (270 + self.espaciado)
                y = self.margen_y + i * (100 + self.espaciado)
                self.posiciones_min.append((x,y))
        


    def dibujar_menu(self):
        #Carga del fondo
        self.pantalla.blit(self.fondo, (0, 0))
        text_til = self.fuente_titulo.render("Modos de juego", True, AZUL_CLARO)
        self.pantalla.blit(text_til, (ANCHO // 2- text_til.get_width() // 2,80))

        color = Cambiar_color_boton(self.b_simple, VERDE, VERDE_CAMBIO)
        pygame.draw.rect(self.pantalla, color, self.b_simple)
        text_facil = self.fuente_boton.render("Simple", True, BLANCO)
        self.pantalla.blit(text_facil, (self.b_simple.x + self.b_simple.width // 2 - text_facil.get_width() // 2, 
                                        self.b_simple.y + self.b_simple.height // 2 - text_facil.get_height() // 2))

        color = Cambiar_color_boton(self.b_contrarreloj, VERDE, VERDE_CAMBIO)
        pygame.draw.rect(self.pantalla, color, self.b_contrarreloj)
        text_contrarreloj = self.fuente_boton.render("Contrarreloj", True, BLANCO)
        self.pantalla.blit(text_contrarreloj, (self.b_contrarreloj.x + self.b_contrarreloj.width // 2 - text_contrarreloj.get_width() // 2, self.b_contrarreloj.y + self.b_contrarreloj.height // 2 - text_contrarreloj.get_height() // 2))

        color = Cambiar_color_boton(self.b_atras, ROJO, ROJO_CAMBIO)
        pygame.draw.rect(self.pantalla, color, self.b_atras)
        text_atras = self.fuente_boton.render("Atras", True, BLANCO)
        self.pantalla.blit(text_atras, (self.b_atras.x + self.b_atras.width // 2 - text_atras.get_width() // 2, 
                                        self.b_atras.y + self.b_atras.height // 2 - text_atras.get_height() // 2))
        
        #Actualización de la pantalla
        pygame.display.flip()

    def dibujar_menu_imagenes(self):
        
        
        #Dibujar fondo
        Fondo = pygame.image.load("Fondo_juego.jpg")
        Fondo = pygame.transform.scale(Fondo, (ANCHO, ALTO))

        #Dibujar titulo de la ventana
        self.pantalla.blit(Fondo, (0,0))

        
        text_eleccion = self.fuente_opciones.render("Elige un rompecabezas", True, BLANCO)
        rect_eleccion = text_eleccion.get_rect(center = (ANCHO // 2, 100))
        self.pantalla.blit(text_eleccion, rect_eleccion)

        #Dibujar botón "atrás"
        color = Cambiar_color_boton(self.b_atras, ROJO, ROJO_CAMBIO)
        pygame.draw.rect(self.pantalla, color, self.b_atras)
        text_atras = self.fuente_boton.render("Atras", True, BLANCO)
        self.pantalla.blit(text_atras, (self.b_atras.x + self.b_atras.width // 2 - text_atras.get_width() // 2,
                                         self.b_atras.y + self.b_atras.height // 2 - text_atras.get_height() // 2))

        for idx in range(0, 8): 
            x, y = self.posiciones_min[idx]
            cuadro = pygame.Rect(x, y, 150, 150)
            pygame.draw.rect(self.pantalla, GRIS_CLARO, cuadro)
            self.pantalla.blit(self.miniaturas[idx], (x, y))

        pygame.display.flip()


    def dificultades(self):
        
        
        #Dibujar fondo
        Fondo = pygame.image.load("Fondo_juego.jpg")
        Fondo = pygame.transform.scale(Fondo, (ANCHO, ALTO))

        #Dibujar titulo de la ventana
        self.pantalla.blit(Fondo, (0,0))

        
        text_eleccion = self.fuente_opciones.render("Elige la dificultad", True, BLANCO)
        rect_eleccion = text_eleccion.get_rect(center = (ANCHO // 2, 100))
        self.pantalla.blit(text_eleccion, rect_eleccion)

        #Dibujar botón "atrás"
        text_atras = self.fuente_boton.render("Atras", True, BLANCO)
                        


        
        self.text_facil = self.fuente_boton.render("Fácil", True, BLANCO)
        

       
        text_intermedio = self.fuente_boton.render("Intermedio", True, BLANCO)
        

        
        text_dificil = self.fuente_boton.render("Dificil", True, BLANCO)
       

        eligiendo = True

        while eligiendo:
            self.pantalla.blit(Fondo, (0,0)) 

            self.pantalla.blit(text_eleccion, rect_eleccion)      

            color = Cambiar_color_boton(self.b_atras, ROJO, ROJO_CAMBIO)
            pygame.draw.rect(self.pantalla, color, self.b_atras)
            self.pantalla.blit(text_atras, (self.b_atras.x + self.b_atras.width // 2 - text_atras.get_width() // 2,
                                         self.b_atras.y + self.b_atras.height // 2 - text_atras.get_height() // 2))                

            color = Cambiar_color_boton(self.b_facil, VERDE, VERDE_CAMBIO)
            pygame.draw.rect(self.pantalla, color, self.b_facil)
            self.pantalla.blit(self.text_facil, 
                               (self.b_facil.x + self.b_facil.width // 2 - self.text_facil.get_width() // 2,
                                self.b_facil.y + self.b_facil.height // 2 - self.text_facil.get_height() // 2))

            color = Cambiar_color_boton(self.b_intermedio, VERDE, VERDE_CAMBIO)
            pygame.draw.rect(self.pantalla, color, self.b_intermedio)
            self.pantalla.blit(text_intermedio, 
                               (self.b_intermedio.x + self.b_intermedio.width //2 - text_intermedio.get_width() // 2, 
                                self.b_intermedio.y + self.b_intermedio.height // 2 - text_intermedio.get_height() //2))

            color = Cambiar_color_boton(self.b_dificil, VERDE, VERDE_CAMBIO)
            pygame.draw.rect(self.pantalla, color, self.b_dificil)
            self.pantalla.blit(text_dificil, 
                               (self.b_dificil.x + self.b_dificil.width // 2 - text_dificil.get_width() // 2,
                                self.b_dificil.y + self.b_dificil.height // 2 - text_dificil.get_height() // 2))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    sys.exit()

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.b_atras.collidepoint(evento.pos):
                        click_boton()                      
                        return "None"
                    
                    if self.b_facil.collidepoint(evento.pos):
                        click_boton()
                        return "Facil"
                    
                    if self.b_intermedio.collidepoint(evento.pos):
                        click_boton()
                        return "Intermedio"
                    
                    if self.b_dificil.collidepoint(evento.pos):
                        click_boton()
                        return "Dificil"
                    
                
            
            pygame.display.flip()


    def Cambio_musica(self, musica):
        pygame.mixer.stop()
        pygame.mixer.music.load(musica)
        pygame.mixer.music.play(-1)



    def Menu(self, sonido):
        
        ejecutando = True
        
        seleccionando = True
        while ejecutando:

            self.dibujar_menu()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    sys.exit()
                    
                if evento.type == pygame.MOUSEBUTTONDOWN:

                    if self.b_simple.collidepoint(evento.pos): #Si el juagdor elije juego simple
                        click_boton()
                        self.color_boton = AZUL
                        #Se abre el menú para seleccionar los rompecabezas
                        modo = self.dificultades()

                        if modo == "None":
                            seleccionando = False                        
                        else:    
                            seleccionando = True
                            if modo == "Facil":
                                filas = 2
                                columnas = 3

                            elif modo == "Intermedio":
                                filas = 3
                                columnas = 3

                            elif modo == "Dificil":
                                filas = 4
                                columnas = 4
                    
                        
                        
                        while seleccionando:

                            self.dibujar_menu_imagenes()
                            for evento2 in pygame.event.get():
                                
                                if evento2.type == pygame.QUIT:
                                    exit()
                                if evento2.type == pygame.MOUSEBUTTONDOWN:
                                    x_click, y_click = evento2.pos
                                        
                                    for idx, (x, y) in enumerate(self.posiciones_min):
                                        clicado = pygame.Rect(x, y, 150, 150)
                                        if clicado.collidepoint(x_click, y_click):
                                                
                                            juego = Juego(filas, columnas, self.imagenes[idx])
                                            if sonido:
                                                self.Cambio_musica("Soundtrack-juego.mp3")
                                                Opcion = juego.jugar()
                                                if Opcion == "salir":
                                                    seleccionando = False
                                                self.Cambio_musica("Soundtrack-inicio.mp3")
                                            else:
                                                Opcion = juego.jugar()
                                                if Opcion == "salir":
                                                    
                                                    seleccionando = False                                                    
                                            

                                        if self.b_atras.collidepoint(evento2.pos):
                                            
                                            seleccionando = False
                                            
                                            
                                        
                                        
                        
                
                    elif self.b_contrarreloj.collidepoint(evento.pos): #Si el jugador elije contrarreloj
                        click_boton()

                        modo = self.dificultades()

                        if modo == "None":
                            seleccionando = False
                            
                        else:
                            seleccionando = True
                            if modo == "Facil":
                                filas = 2
                                columnas = 3
                                tiempo = 180

                            elif modo == "Intermedio":
                                filas = 3
                                columnas = 3
                                tiempo = 360

                            elif modo == "Dificil":
                                filas = 4
                                columnas = 4
                                tiempo = 600

                        #Se abre el menú para seleccionar los rompecabezas
                        
                        while seleccionando: 
                            self.dibujar_menu_imagenes()
                            for evento2 in pygame.event.get():
                                
                                if evento2.type == pygame.QUIT:
                                    exit()                                
                                if evento2.type == pygame.MOUSEBUTTONDOWN:
                                    x_click, y_click = evento2.pos
                                        
                                    for idx, (x, y) in enumerate(self.posiciones_min):
                                        clicado = pygame.Rect(x, y, 150, 150)
                                        if clicado.collidepoint(x_click, y_click): 
                                            juego = Contrarreloj(filas, columnas,
                                                                self.imagenes[idx], tiempo)
                                            if sonido:
                                                self.Cambio_musica("Soundtrack-juego.mp3")
                                                
                                                Opcion = juego.jugar()
                                                if Opcion == "salir":
                                                    
                                                    seleccionando = False
                                                self.Cambio_musica("Soundtrack-inicio.mp3")
                                            else:
                                                Opcion = juego.jugar()
                                                if Opcion == "salir":
                                                    
                                                    seleccionando = False                                                

                                            #ejecutando = False

                                        if self.b_atras.collidepoint(evento2.pos):
                                            seleccionando = False

                            #ejecutando = False                        
                
                    elif self.b_atras.collidepoint(evento.pos):
                        
                        ejecutando = False
        

                        
                

pygame.quit() #Este método evita que se regrese al menú principal si cierra la ventana
        