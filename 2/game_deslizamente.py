import pygame
from sys import exit
from constantes_deslizamente import *
from random import shuffle


pygame.init()
pygame.mixer.init()
class Juego:
    def __init__(self, filas,columnas, imagen):
        #Dimensiones 
        self.FILAS= filas
        self.COLUMNAS =columnas
        self.ancho_disponible = ANCHO // self.COLUMNAS
        self.alto_disponible = ALTO // self.FILAS
        self.TAM_CASILLA = int(min(self.ancho_disponible, self.alto_disponible) * 0.5 ) #Se dividen para formar un numero entero

        #Pantalla del juego
        self.PANTALLA = pygame.display.set_mode((ANCHO, ALTO))

        #Lista de posiciones de las piezas
        self.POSICIONES = list(range(self.FILAS * self.COLUMNAS))
        #Lista de las piezas
        self.piezas = []

        #Respaldo
        self.respaldo = []

        #sonido de movimiento de piezas
        self.mov = pygame.mixer.Sound("Movimiento.wav")

        #Dimensiones del tablero

        self.ancho_tablero = self.COLUMNAS * self.TAM_CASILLA
        self.alto_tablero = self.FILAS * self.TAM_CASILLA


        #Posiciones iniciales del tablero
        self.x_inicial = (ANCHO - self.ancho_tablero) // 2
        self.y_inicial = (ALTO - self.alto_tablero) // 2
        
        #Imagen de prueba
        #Agrege convert_alpha
        
        self.imagen = imagen


        #Boton salir
        self.fuente_boton= pygame.font.SysFont("consolas", 25)
        self.b_salir = pygame.Rect(0, 0, 200, 50) #Esquina superior izquierda 

        #Fondo
        #Cambie .convert
        self.FONDO = pygame.image.load("fondo_juego.jpg").convert_alpha()

        #Fuente de texto
        self.fuente = pygame.font.SysFont("consolas", 20)

        pygame.display.set_caption("Deslizamente")

    def Dividir_Casillas(self):
        #Calcular el tamaño de la imagen
        ancho_total = self.COLUMNAS * self.TAM_CASILLA
        alto_total = self.FILAS * self.TAM_CASILLA

        #Redimensión de la imagen del rompecabezas
        self.imagen = pygame.transform.scale(self.imagen, (ancho_total, alto_total))

        for fila in range(self.FILAS):
            for columna in range(self.COLUMNAS):
                Casilla = pygame.Rect(columna * self.TAM_CASILLA, fila * self.TAM_CASILLA, self.TAM_CASILLA, self.TAM_CASILLA)
                if fila == self.FILAS-1 and columna == self.COLUMNAS-1:
                    self.piezas.append(None)
                else:
                    pieza = self.imagen.subsurface(Casilla).copy()
                    self.piezas.append(pieza)
        self.POSICIONES = list(range(self.FILAS * self.COLUMNAS))
        self.respaldo = self.POSICIONES[:]
        shuffle(self.POSICIONES)

    def dibujar_fondo(self, imagen):
        #Modificando dimensiones de la imagen de fondo y dibujarla
        self.FONDO = pygame.transform.scale(self.FONDO, (ANCHO,ALTO ))
        self.PANTALLA.blit(self.FONDO, (0,0))

        #Dibujando boton 'salir'
        color = Cambiar_color_boton(self.b_salir, ROJO, ROJO_CAMBIO)
        pygame.draw.rect(self.PANTALLA, color, self.b_salir)

        text_atras = self.fuente_boton.render("Atras", True, BLANCO)
        self.PANTALLA.blit(text_atras, (self.b_salir.x + self.b_salir.width // 2 - text_atras.get_width() // 2, self.b_salir.y + self.b_salir.height // 2 - text_atras.get_height() // 2))
        imagen_guia = imagen
        Ancho_guia, Alto_guia = self.ancho_tablero // 2 , self.alto_tablero // 2 
        imagen_guia = pygame.transform.scale(imagen, (Ancho_guia, Alto_guia))
        self.PANTALLA.blit(imagen_guia, (ANCHO- Ancho_guia, 0))      

    def Dibujar_tablero(self):
        self.dibujar_fondo(self.imagen)    

        for i, num_pieza in enumerate(self.POSICIONES):

            #Fila y columna actuales del tablero
            fila_actual = i // self.COLUMNAS
            columna_actual = i % self.COLUMNAS

            pieza_actual = self.piezas[num_pieza]
            if pieza_actual: #Si no hay espacio vacío...
                self.PANTALLA.blit(pieza_actual, (self.x_inicial + (columna_actual * self.TAM_CASILLA), 
                                                  self.y_inicial + (fila_actual * self.TAM_CASILLA)))
            #Dibuja un borde negro en cada celda
            pygame.draw.rect(self.PANTALLA, NEGRO, 
                         (self.x_inicial + columna_actual * self.TAM_CASILLA,
                           self.y_inicial + fila_actual * self.TAM_CASILLA, 
                           self.TAM_CASILLA, self.TAM_CASILLA), 2)
                
        

    def movimiento_valido(self, indice_clicado): #Este método verifica si el movimiento es válido
        # El espacio vacío está representando el último índice (por ejemplo: FILAS * COLUMNAS - 1)
        indice_vacío = self.POSICIONES.index(self.FILAS * self.COLUMNAS - 1)  
        fila_clicado = indice_clicado // self.COLUMNAS
        columna_clicado = indice_clicado % self.COLUMNAS
        fila_vacio = indice_vacío // self.COLUMNAS
        columna_vacio = indice_vacío % self.COLUMNAS
        return abs(fila_clicado - fila_vacio) + abs(columna_clicado - columna_vacio) == 1

    def mover_casilla(self, indice_clicado): #Mover casilla si el movimiento es válido
        #Intercambia la pieza clickeada con el espacio vacío.
        indice_vacio = self.POSICIONES.index(self.FILAS * self.COLUMNAS - 1)
        self.POSICIONES[indice_clicado], self.POSICIONES[indice_vacio]  = self.POSICIONES[indice_vacio], self.POSICIONES[indice_clicado]



    def dibujar_pop_salir(self, pantalla):
         #Añadir reloj como parametro o aplicar polimorfismo
        fuente = pygame.font.SysFont("consolas", 16)
        fondo_capturado = pantalla.copy()
        
        ejecutando_popup = True
        while ejecutando_popup:
            pantalla.blit(fondo_capturado, (0,0))
            overlay = pygame.Surface((ANCHO,ALTO), pygame.SRCALPHA)
            overlay.fill((50,50,50, 180))
            pantalla.blit(overlay, (0,0))

            popup_rect = pygame.Rect(ANCHO//2 -200 , ALTO// 2 -100, 400, 200)
            pygame.draw.rect(pantalla, BLANCO, popup_rect)
            pygame.draw.rect(pantalla, NEGRO, popup_rect, 4)

            texto = self.fuente.render("¿Deseas salir?", True, NEGRO)
            pantalla.blit(texto, (ANCHO// 2 - texto.get_width()// 2, ALTO//2 -70))

            b_volver_jugar = pygame.Rect(ANCHO// 2 - 150, ALTO//2 +20, 120, 40)
            b_salir = pygame.Rect(ANCHO// 2 +30, ALTO//2 +20, 120, 40)

            pygame.draw.rect(pantalla, VERDE, b_volver_jugar)
            pygame.draw.rect(pantalla, ROJO, b_salir)

            text_volver_jugar =fuente.render("Continuar", True, BLANCO)
            text_salir = fuente.render("Ir al menu", True, BLANCO)

            #pantalla.blit(text_volver_jugar, (b_volver_jugar.x +15, b_volver_jugar.y +8))
            #pantalla.blit(text_salir, (b_salir.x +25, b_salir.y +8))
            pantalla.blit(text_volver_jugar,
                           (b_volver_jugar.x + (b_volver_jugar.width - text_volver_jugar.get_width())// 2, 
                            b_volver_jugar.y +(b_volver_jugar.height -  text_volver_jugar.get_height()) // 2))
            pantalla.blit(text_salir, 
                          (b_salir.x + (b_salir.width - text_salir.get_width())//2, 
                           b_salir.y + (b_salir.height- text_salir.get_height())// 2))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando_popup = False
                    return "salir"
                    
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if b_volver_jugar.collidepoint(evento.pos):
                        click_boton()
                        """ejecutando_popup = False
                        self.Dividir_Casillas()
                        self.timer_activo = False
                        self.terminado = False
                        self.jugar()"""
                        ejecutando_popup = False
                        return "reintentar"
                    elif b_salir.collidepoint(evento.pos):
                        click_boton()
                        return "salir"
                    """
                        ejecutando_popup = False
                        from main2 import Menu
                        menu = Menu()
                        menu.mostrar_menu()
                        """
                    
            pygame.display.flip()




    def jugar(self):
        ejecutando =  True
        self.Dividir_Casillas()
        
        while ejecutando:
        
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    exit()
                    ejecutando = False
                if evento.type == pygame.MOUSEBUTTONDOWN:

                    pos_x, pos_y = pygame.mouse.get_pos()
                    columna = (pos_x - self.x_inicial) // self.TAM_CASILLA
                    fila = (pos_y - self.y_inicial) // self.TAM_CASILLA
                    indice = fila * self.COLUMNAS + columna

                    if self.b_salir.collidepoint(evento.pos):
                        click_boton()
                        respuesta = self.dibujar_pop_salir(self.PANTALLA)
                        if respuesta == "salir":
                            click_boton()
                            
                            ejecutando = False

                    # 1) Ignorar clicks fuera del área de juego
                    if not (self.x_inicial <= pos_x < self.x_inicial + self.ancho_tablero
                        and self.y_inicial <= pos_y < self.y_inicial + self.alto_tablero):
                        continue

                    # 2) Calcular fila y columna dentro del tablero
                    columna = (pos_x - self.x_inicial) // self.TAM_CASILLA
                    fila    = (pos_y - self.y_inicial) // self.TAM_CASILLA
                    indice  = fila * self.COLUMNAS + columna

                    # 3) Mover solo si es un movimiento válido
                    if self.movimiento_valido(indice):
                        self.mov.play()
                        self.mover_casilla(indice)
                        self.Dibujar_tablero()
                        #Verificacion si las posiciones movidas son iguales a las originales
                    
                        if self.POSICIONES == self.respaldo:
                            resultado = self.dibujar_win(self.PANTALLA)
                            if resultado == "menu":
                                ejecutando = False
                                pygame.mixer.music.stop()
                                pygame.mixer.music.load("Soundtrack-inicio.mp3")
                                pygame.mixer.music.play(-1)
                                return resultado
                                
                                
                            

                                


            
            self.Dibujar_tablero()
            pygame.display.flip() 

    def dibujar_win(self, pantalla):
        fuente = pygame.font.SysFont("consolas", 16)
        fuente2 = pygame.font.SysFont("consolas" , 55)
        fondo_capturado = pantalla.copy()

        trofeo = pygame.image.load("trofeo.png").convert_alpha()
        trofeo = pygame.transform.scale(trofeo, (80,80))
        ejecutando_popup = True
        while ejecutando_popup:
            pantalla.blit(fondo_capturado, (0,0))
            overlay = pygame.Surface((ANCHO,ALTO), pygame.SRCALPHA)
            overlay.fill((50,50,50, 180))
            pantalla.blit(overlay, (0,0))

            popup_rect = pygame.Rect(ANCHO//2 -200 , ALTO// 2 -150, 400, 300)
            pygame.draw.rect(pantalla, BLANCO, popup_rect)
            #pygame.draw.rect(pantalla, NEGRO, popup_rect, 4)

            texto = fuente2.render("¡Ganaste!", True, VERDE)
            #ANTES
            #pantalla.blit(texto, (ANCHO// 2 - texto.get_width()// 2, ALTO//2 -70))
            pantalla.blit(texto, (popup_rect.centerx - texto.get_width()//2, popup_rect.y + 30))
            
            #ANTES
            #pantalla.blit(trofeo, (ANCHO//2 - trofeo.get_width()//2, ALTO//2-85))
            pantalla.blit(trofeo, (popup_rect.centerx-trofeo.get_width()//2, popup_rect.y +100))

            #b_salir = pygame.Rect(ANCHO// 2 +30, ALTO//2 +20, 120, 40)
            """
            ANTES
            b_salir = pygame.Rect(ANCHO// 2 +30, ALTO//2 +20, 120, 40)
            b_salir.centerx = ANCHO//2
            """
            b_salir = pygame.Rect(0,0,160,45)
            b_salir.centerx = popup_rect.centerx
            b_salir.y = popup_rect.y + 210

            color = Cambiar_color_boton(b_salir, AZUL, AZUL_CAMBIO)
            pygame.draw.rect(pantalla, color, b_salir)

            
            text_salir = fuente.render("Ir al menu", True, BLANCO)

            pantalla.blit(text_salir, 
                          (b_salir.x + (b_salir.width - text_salir.get_width())//2, 
                           b_salir.y + (b_salir.height- text_salir.get_height())// 2))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando_popup = False
                    return "salir"
                    
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    
                    if b_salir.collidepoint(evento.pos):
                        click_boton()
                        return "menu"
                    
            pygame.display.flip()
            
#Modo contrareloj                
class Contrarreloj(Juego):
    def __init__(self, filas, columnas, imagen, duracion):
        super().__init__(filas,columnas,imagen)
        
        self.color = BLANCO
        self.timer_activo = False
        self.tiempo_inicial = 0
        self.duracion_timer = duracion * 1000 #Convertir a segundos
        self.reloj = pygame.time.Clock()

        #Para el pausado
        self.pausa = None
        self.acum_pausa = 0

        #Finalizado del temporizador
        self.terminado = False




    def iniciar(self):
        self.tiempo_inicial = pygame.time.get_ticks()
        self.inicio_pausa = None

        self.timer_activo = True




        


    def actualizar(self):
        if self.terminado:
            return -1
        if not self.timer_activo:
            return self.duracion_timer // 1000
        
        tiempo_actual = pygame.time.get_ticks()
        
        if self.inicio_pausa is not None:
            elapsed = self.inicio_pausa - self.tiempo_inicial - self.acum_pausa
        else: 
            elapsed = tiempo_actual - self.tiempo_inicial - self.acum_pausa
    

        tiempo_restante = self.duracion_timer - elapsed
        #Antes : tiempo_restante = self.duracion_timer -(tiempo_actual - self.tiempo_inicial)

        if tiempo_restante <= 0:
            self.timer_activo = False
            self.terminado = True
            return -1
        
        return tiempo_restante // 1000
    

    def tick(self):
        self.reloj.tick(60)

    def dib(self, pantalla):
        tiempo = self.actualizar()
        if tiempo == -1:
            texto = self.fuente.render("Se acabó el tiempo", True, ROJO)
            
        else:       
            minutos = tiempo// 60
            segundos = tiempo% 60
            if segundos < 10: 
                segundos = f"0{str(segundos)}"
                texto = self.fuente.render(f"Tiempo: {minutos}: {segundos}", True, self.color)
                pantalla.blit(texto, (ANCHO// 2 - texto.get_width() // 2, ALTO*0.2))
                segundos = int(segundos)

            else: 
                texto = self.fuente.render(f"Tiempo: {minutos}: {segundos}", True, self.color)
                pantalla.blit(texto, (ANCHO// 2 - texto.get_width() // 2, ALTO*0.2))




        
        
        


    def jugar(self):
        ejecutando =  True
        self.Dividir_Casillas()
        text_continuar = self.fuente.render("Haga click en cualquier parte de la pantalla para comenzar",
                                                  True, BLANCO)
        
        while ejecutando:


        
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    #pygame.quit()
                    exit()
                    ejecutando = False
                if evento.type == pygame.MOUSEBUTTONDOWN:

                    if not self.timer_activo and not self.terminado:
                        self.iniciar()
                    
                    


                    pos_x, pos_y = pygame.mouse.get_pos()
                    columna = (pos_x - self.x_inicial) // self.TAM_CASILLA
                    fila = (pos_y - self.y_inicial) // self.TAM_CASILLA
                    indice = fila * self.COLUMNAS + columna

                    if self.b_salir.collidepoint(evento.pos):
                        click_boton()
                        
                        respuesta = self.dibujar_pop_salir(self.PANTALLA)
                        click_boton()
                        if respuesta == "salir":
                            ejecutando = False
                        
                        
                            

                    # 1) Ignorar clicks fuera del área de juego
                    if not (self.x_inicial <= pos_x < self.x_inicial + self.ancho_tablero
                        and self.y_inicial <= pos_y < self.y_inicial + self.alto_tablero):
                        continue

                    # 2) Calcular fila y columna dentro del tablero
                    columna = (pos_x - self.x_inicial) // self.TAM_CASILLA
                    fila    = (pos_y - self.y_inicial) // self.TAM_CASILLA
                    indice  = fila * self.COLUMNAS + columna

                    # 3) Mover solo si es un movimiento válido
                    if self.movimiento_valido(indice):
                        self.mov.play()
                        self.mover_casilla(indice)
                        
                        #Verificacion si las posiciones movidas son iguales a las originales
                    
                        if self.POSICIONES == self.respaldo:
                            resultado = self.dibujar_win(self.PANTALLA)
                            if resultado == "menu":
                                ejecutando = False
                                pygame.mixer.music.stop()
                                pygame.mixer.music.load("Soundtrack-inicio.mp3")
                                pygame.mixer.music.play(-1)



                
                    
            
            if self.terminado:
                resultado = self.dibujar_pop(self.PANTALLA)
                if resultado == "menu":
                    return "salir"
                elif resultado == "salir":
                    
                    #exit()
                    return "salir"
                else:
                    return "reintentar"
                    


                #ejecutando = False

            
            self.Dibujar_tablero()

            if not self.timer_activo and not self.terminado:
                self.PANTALLA.blit(text_continuar, 
                                   (ANCHO// 2 - text_continuar.get_width() // 2, ALTO // 7))

            self.dib(self.PANTALLA)
            pygame.display.flip()
            self.tick()

            


    def dibujar_pop(self, pantalla):
        fuente = pygame.font.SysFont("consolas", 16)
        fondo_capturado = pantalla.copy()
        ejecutando_popup = True
        while ejecutando_popup:
            pantalla.blit(fondo_capturado, (0,0))
            overlay = pygame.Surface((ANCHO,ALTO), pygame.SRCALPHA)
            overlay.fill((50,50,50, 180))
            pantalla.blit(overlay, (0,0))

            popup_rect = pygame.Rect(ANCHO//2 -200 , ALTO// 2 -100, 400, 200)
            pygame.draw.rect(pantalla, BLANCO, popup_rect)
            pygame.draw.rect(pantalla, NEGRO, popup_rect, 4)

            texto = self.fuente.render("¡Se acabo el tiempo!", True, NEGRO)
            pantalla.blit(texto, (ANCHO// 2 - texto.get_width()// 2, ALTO//2 -70))

            b_volver_jugar = pygame.Rect(ANCHO// 2 - 150, ALTO//2 +20, 120, 40)
            b_salir = pygame.Rect(ANCHO// 2 +30, ALTO//2 +20, 120, 40)

            color = Cambiar_color_boton(b_volver_jugar, VERDE, VERDE_CAMBIO)
            pygame.draw.rect(pantalla, color, b_volver_jugar)

            color = Cambiar_color_boton(b_salir, ROJO, ROJO_CAMBIO)
            pygame.draw.rect(pantalla, color, b_salir)

            text_volver_jugar =fuente.render("Reintentar", True, BLANCO)
            text_salir = fuente.render("Ir al menu", True, BLANCO)

            #pantalla.blit(text_volver_jugar, (b_volver_jugar.x +15, b_volver_jugar.y +8))
            #pantalla.blit(text_salir, (b_salir.x +25, b_salir.y +8))
            pantalla.blit(text_volver_jugar,
                           (b_volver_jugar.x + (b_volver_jugar.width - text_volver_jugar.get_width())// 2, 
                            b_volver_jugar.y +(b_volver_jugar.height -  text_volver_jugar.get_height()) // 2))
            pantalla.blit(text_salir, 
                          (b_salir.x + (b_salir.width - text_salir.get_width())//2, 
                           b_salir.y + (b_salir.height- text_salir.get_height())// 2))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando_popup = False
                    return "salir"
                    
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if b_volver_jugar.collidepoint(evento.pos):
                        click_boton()
                        """ejecutando_popup = False
                        self.Dividir_Casillas()
                        self.timer_activo = False
                        self.terminado = False
                        self.jugar()"""
                        ejecutando_popup = False
                        return "reintentar"
                    elif b_salir.collidepoint(evento.pos):
                        click_boton()
                        return "menu"
                    """
                        ejecutando_popup = False
                        from main2 import Menu
                        menu = Menu()
                        menu.mostrar_menu()
                        """
                    
            pygame.display.flip()

    def dibujar_pop_salir(self, pantalla):
         #Añadir reloj como parametro o aplicar polimorfismo
        fuente = pygame.font.SysFont("consolas", 16)
        fondo_capturado = pantalla.copy()

        if self.timer_activo and  not self.terminado:
            self.inicio_pausa = pygame.time.get_ticks()

        
        ejecutando_popup = True
        while ejecutando_popup:
            pantalla.blit(fondo_capturado, (0,0))
            overlay = pygame.Surface((ANCHO,ALTO), pygame.SRCALPHA)
            overlay.fill((50,50,50, 180))
            pantalla.blit(overlay, (0,0))

            popup_rect = pygame.Rect(ANCHO//2 -200 , ALTO// 2 -100, 400, 200)
            pygame.draw.rect(pantalla, BLANCO, popup_rect)
            pygame.draw.rect(pantalla, NEGRO, popup_rect, 4)

            texto = self.fuente.render("¿Deseas salir?", True, NEGRO)
            pantalla.blit(texto, (ANCHO// 2 - texto.get_width()// 2, ALTO//2 -70))

            b_volver_jugar = pygame.Rect(ANCHO// 2 - 150, ALTO//2 +20, 120, 40)
            b_salir = pygame.Rect(ANCHO// 2 +30, ALTO//2 +20, 120, 40)

            pygame.draw.rect(pantalla, VERDE, b_volver_jugar)
            pygame.draw.rect(pantalla, ROJO, b_salir)

            text_volver_jugar =fuente.render("Continuar", True, BLANCO)
            text_salir = fuente.render("Ir al menu", True, BLANCO)

            #pantalla.blit(text_volver_jugar, (b_volver_jugar.x +15, b_volver_jugar.y +8))
            #pantalla.blit(text_salir, (b_salir.x +25, b_salir.y +8))
            pantalla.blit(text_volver_jugar,
                           (b_volver_jugar.x + (b_volver_jugar.width - text_volver_jugar.get_width())// 2, 
                            b_volver_jugar.y +(b_volver_jugar.height -  text_volver_jugar.get_height()) // 2))
            pantalla.blit(text_salir, 
                          (b_salir.x + (b_salir.width - text_salir.get_width())//2, 
                           b_salir.y + (b_salir.height- text_salir.get_height())// 2))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando_popup = False
                    return "salir"
                    
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if b_volver_jugar.collidepoint(evento.pos):
                        click_boton()
                        if self.inicio_pausa is not None:
                            self.acum_pausa += pygame.time.get_ticks() - self.inicio_pausa
                            self.inicio_pausa = None

                        """ejecutando_popup = False
                        self.Dividir_Casillas()
                        self.timer_activo = False
                        self.terminado = False
                        self.jugar()"""
                        ejecutando_popup = False
                        return "reintentar"
                    elif b_salir.collidepoint(evento.pos):
                        click_boton()
                        return "salir"
                    """
                        ejecutando_popup = False
                        from main2 import Menu
                        menu = Menu()
                        menu.mostrar_menu()
                        """
                    
            pygame.display.flip()

#Cambio de color

def Cambiar_color_boton(boton, color_i, color_f):            
    mouse_pos = pygame.mouse.get_pos()
    
    if boton.collidepoint(mouse_pos):
        color = color_f
    else: color = color_i

    return color

def click_boton():
    efecto_click = pygame.mixer.Sound("click_boton.wav")
    efecto_click.play()

pygame.quit()




