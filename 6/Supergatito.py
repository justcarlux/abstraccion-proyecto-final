import pygame
import random
import os

pygame.init()
pygame.mixer.init()

color_fondo_principal = (220, 235, 245)  
color_bandeja = (240, 240, 230) 
color_opcion_fondo = (200, 220, 210) 
color_borde = (120, 180, 200) 
negro = (0, 0, 0)
rojo = (255, 0, 0)
verde = (0, 255, 0)
naranja = (255, 165, 0)
verde_oscuro = (0, 100, 0)
azul_cielo = (135, 206, 235) 
amarillo = (255, 255, 0)

ancho, alto = 1280, 720 
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("SúperGatito")

sonido_musica = pygame.mixer.Sound("sonidos/cancion.wav")
sonido_musica.set_volume(0.3)
sonido_acierto = pygame.mixer.Sound("sonidos/acertar.wav")
sonido_acierto.set_volume(0.25)
sonido_error = pygame.mixer.Sound("sonidos/errar.wav")
sonido_error.set_volume(0.15)
sonido_musica.play(-1)  

ruta_img = os.path.join(os.path.dirname(__file__))

opciones_por_pagina = 4  
pagina_actual = 0    
opciones_mezcladas = []  # Lista de opciones de alimentos mezcladas para paginación
volumen=1
  # Volumen inicial, 1 es máximo, 0 es silencio
def cargar_img(nombre, tam=None):
    ruta_completa = os.path.join(ruta_img, nombre)
    if not os.path.exists(ruta_completa):
        print(f"Error: La imagen no se encontró en {ruta_completa}")
        return pygame.Surface((100, 100), pygame.SRCALPHA) # Superficie vacía y transparente
    img = pygame.image.load(ruta_completa).convert_alpha()
    if tam:
        img = pygame.transform.scale(img, tam)
    return img

try:
    gato_frames = [cargar_img(f"imagenes/gato{i}.png", (400, 400)).convert_alpha() for i in range(1, 5)]
    gato_img_estatica = cargar_img("imagenes/gato.png", (400, 400)).convert_alpha() # Para pantalla de bienvenida y nube de pensamiento

    papa = cargar_img("imagenes/papa.png", (140,140)).convert_alpha()
    fresa = cargar_img("imagenes/fresa.png", (140,140)).convert_alpha()
    pimenton = cargar_img("imagenes/pimenton.png", (140,140)).convert_alpha()
    dona = cargar_img("imagenes/dona.png",(140,140)).convert_alpha()
    uvas = cargar_img("imagenes/uvas.png", (140,140)).convert_alpha()
    pera = cargar_img("imagenes/pera.png", (140,140)).convert_alpha()
    manzana = cargar_img("imagenes/manzana.png", (140,140)).convert_alpha()
    limones = cargar_img("imagenes/limones.png", (140,140)).convert_alpha()
    torta = cargar_img("imagenes/torta.png", (140,140)).convert_alpha()
    berenjena = cargar_img("imagenes/berenjena.png", (140,140)).convert_alpha()
    bananas= cargar_img("imagenes/bananas.png", (140,140)).convert_alpha()
    calabaza= cargar_img("imagenes/calabaza.png", (140,140)).convert_alpha()
    
    pensamiento = cargar_img("imagenes/pensamiento.png", (430, 290)).convert_alpha()
    fondo_juego = cargar_img("imagenes/fondo.png", (ancho, alto)).convert_alpha()
    fondo_bienvenida = cargar_img("imagenes/fondo_bienvenida.png", (ancho, alto)).convert_alpha()
    letras_bienvenida = cargar_img("imagenes/letras_bienvenida.png", (500, 300)).convert_alpha()
    info = cargar_img("imagenes/info.png", (750, 500)).convert_alpha()
    vol_off = cargar_img("imagenes/vol_off.png", (80, 80)).convert_alpha()
    vol_on = cargar_img("imagenes/vol_on.png", (80, 80)).convert_alpha()
    avanzar= cargar_img("imagenes/flecha_derecha.png",(70,70)).convert_alpha()
    retroceder= cargar_img("imagenes/flecha_izquierda.png",(70,70)).convert_alpha()
    img_reglas= cargar_img("imagenes/reglas.png",(610,380)).convert_alpha()
                           
except Exception as e:
    print(f"Error al cargar una imagen: {e}")
    print("Asegúrate de que las imágenes están en la carpeta 'images' junto a tu script.")
    pygame.quit()
    exit()

opciones_alimentos = [
    {'nombre': 'Papa', 'img': papa, 'tipo': 'vegetal'},
    {'nombre': 'Fresa', 'img': fresa, 'tipo': 'fruta'},
    {'nombre': 'Pimentón', 'img': pimenton, 'tipo': 'vegetal'},
    {'nombre': 'Donut', 'img': dona, 'tipo': 'dulce'},
    {'nombre': 'Uvas', 'img': uvas, 'tipo': 'fruta'},
    {'nombre': 'Pera', 'img': pera, 'tipo': 'fruta'},
    {'nombre': 'Manzana', 'img': manzana, 'tipo': 'fruta'},
    {'nombre': 'Limones', 'img': limones, 'tipo': 'fruta'},
    {'nombre': 'Torta', 'img': torta, 'tipo': 'dulce'},
    {'nombre': 'Berenjena', 'img': berenjena, 'tipo': 'vegetal'},
    {'nombre': 'Bananas', 'img': bananas, 'tipo': 'fruta'},
    {'nombre': 'Calabaza', 'img': calabaza, 'tipo': 'vegetal'}
]
num1=0
num2=0
resultado_suma=0
def siguiente():

    global num1, num2, resultado_suma, opciones_mezcladas, pagina_actual

    num1= random.randint(1, 5)  
    num2 = random.randint(1, 5) 
    resultado_suma = num1 + num2

    todas_las_respuestas_posibles = {resultado_suma} 
    
    # Generando respuestas incorrectas
    while len(todas_las_respuestas_posibles) < opciones_por_pagina:
        distractor = random.randint(1, 10) 
        if distractor not in todas_las_respuestas_posibles:
            todas_las_respuestas_posibles.add(distractor)
    
    # Convertir a lista y mezclar
    lista_respuestas_mezcladas = list(todas_las_respuestas_posibles)
    random.shuffle(lista_respuestas_mezcladas)

    # Preparar las opciones numéricas con sus superficies de texto
    opciones_mezcladas = [] # Limpiar opciones_mezcladas
    for num_val in lista_respuestas_mezcladas:
        texto_num_surface = fuente_principal.render(str(num_val), True, negro)
        opciones_mezcladas.append({'valor': num_val, 'superficie_texto': texto_num_surface})

    pagina_actual = 0 # Siempre empezar en la primera página con las nuevas opciones

def mezclar_opciones_juego():
    global opciones_mezcladas
    opciones_mezcladas = random.sample(opciones_alimentos, len(opciones_alimentos))

mezclar_opciones_juego()

# Configuración de fuentes
fuente_principal = pygame.font.Font("AGAALER.TTF", 60)
fuente_comentarios = pygame.font.Font("AGAALER.TTF", 56)
fuente_boton = pygame.font.SysFont(None, 44) 
fuente_ins=  pygame.font.SysFont(None, 25)

# Posiciones de elementos en pantalla
pos_gato = (60, 190) # Posición del gato
rect_bandeja = pygame.Rect(850, 330, 350, 180) # Rectángulo de la bandeja
volumen_rect = pygame.Rect(ancho - 130, 35, 100, 100)
volumen=1

presionado_sig=False
presionado_ant=False

class GatoAnimado(pygame.sprite.Sprite):
    def __init__(self, frames, pos):
        super().__init__()
        self.frames = frames
        self.frame_idx = 0
        self.image = self.frames[self.frame_idx]
        self.rect = self.image.get_rect(topleft=pos)
        self.vel_animacion = 0.4 # segundos por fotograma
        self.tiempo_acumulado = 0

    def update(self, dt):
        self.tiempo_acumulado += dt
        if self.tiempo_acumulado >= self.vel_animacion:
            self.tiempo_acumulado = 0
            self.frame_idx = (self.frame_idx + 1) % len(self.frames)
            self.image = self.frames[self.frame_idx]

def obtener_opciones_y_rects_visibles():

    ancho_opcion = 120   
    alto_opcion = 120      
    separacion = 100      
    margen_inferior = 50  

    # Opciones visibles según paginación
    inicio = pagina_actual * opciones_por_pagina
    fin = inicio + opciones_por_pagina
    opciones_visibles = opciones_mezcladas[inicio:fin]
    cantidad = len(opciones_visibles)
    ancho_total = cantidad * ancho_opcion + (cantidad - 1) * separacion
    margen_izquierdo = (ancho - ancho_total) // 2
    y = alto - alto_opcion - margen_inferior
    rects_opciones = [pygame.Rect(margen_izquierdo + i * (ancho_opcion + separacion),y,ancho_opcion,alto_opcion) for i in range(cantidad)]

    return opciones_visibles, rects_opciones

def dibujar_escena_juego(gato_piensa_item, indice_arrastrado=None, pos_arrastre=None, presionado_sig=False, presionado_ant=False):
    ventana.blit(fondo_juego, (0, 0))
    ventana.blit(pensamiento, (500, 40)) # Nube de pensamiento

    # Imagen que el gato está pensando
    img_pensada = gato_piensa_item.get('img')
    if img_pensada:
        rect_img_pensada = img_pensada.get_rect(center=(700, 150))
        ventana.blit(img_pensada, rect_img_pensada)
    #instrucciones
    instrucciones = "NOTA: Desplázate a la izquierda y derecha en las opciones, para encontrar lo que el gato está pensando, y luego arrastrala hasta la bandeja."
    super_instrucciones = fuente_ins.render(instrucciones, True, negro)
    rect_inst = super_instrucciones.get_rect(center=(ancho//2, 20))
    ventana.blit(super_instrucciones, rect_inst)
    
    # Dibujando bandeja
    pygame.draw.rect(ventana, color_bandeja, rect_bandeja, border_radius=30)
    pygame.draw.rect(ventana, color_borde, rect_bandeja, 5, border_radius=30)
    # Opciones en la parte inferior
    opciones_visibles, rects_opciones_visibles = obtener_opciones_y_rects_visibles()
    for idx, opt in enumerate(opciones_visibles):
        if idx == indice_arrastrado:
            continue
        pygame.draw.rect(ventana, color_opcion_fondo, rects_opciones_visibles[idx], border_radius=25)
        # Muestra imagen o número según el contenido del diccionario
        if 'img' in opt:
            rect_img_opcion = opt['img'].get_rect(center=rects_opciones_visibles[idx].center)
            ventana.blit(opt['img'], rect_img_opcion)
        elif 'superficie_texto' in opt:
            rect_txt_opcion = opt['superficie_texto'].get_rect(center=rects_opciones_visibles[idx].center)
            ventana.blit(opt['superficie_texto'], rect_txt_opcion)

    # Si un elemento está siendo arrastrado, dibujarlo
    if indice_arrastrado is not None and pos_arrastre is not None:
        rect_arrastre_fondo = pygame.Rect(*pos_arrastre, 160, 160) 
        pygame.draw.rect(ventana, color_borde, rect_arrastre_fondo, border_radius=25)
        pygame.draw.rect(ventana, (255,255,255), rect_arrastre_fondo, 5, border_radius=25)
        opcion_arrastrada_real = opciones_mezcladas[pagina_actual * opciones_por_pagina + indice_arrastrado]
        if 'img' in opcion_arrastrada_real:
            rect_img_arrastrada = opcion_arrastrada_real['img'].get_rect(center=(pos_arrastre[0]+80, pos_arrastre[1]+80))
            ventana.blit(opcion_arrastrada_real['img'], rect_img_arrastrada)
        elif 'superficie_texto' in opcion_arrastrada_real:
            rect_txt_arrastrada = opcion_arrastrada_real['superficie_texto'].get_rect(center=(pos_arrastre[0]+80, pos_arrastre[1]+80))
            ventana.blit(opcion_arrastrada_real['superficie_texto'], rect_txt_arrastrada)
    

    boton_anterior_rect = pygame.Rect(40, 650, 145, 60)
    boton_siguiente_rect = pygame.Rect(ancho - 170, 650, 145, 60)
    
    # Botones de paginación pequeño/s y en la parte inferior
    color_anterior = verde if presionado_ant else color_fondo_principal
    pygame.draw.rect(ventana, color_anterior, boton_anterior_rect, border_radius=15)
    pygame.draw.rect(ventana, negro, boton_anterior_rect, 2, border_radius=15)

    color_siguiente = verde if presionado_sig else color_fondo_principal
    pygame.draw.rect(ventana, color_siguiente, boton_siguiente_rect, border_radius=15)
    pygame.draw.rect(ventana, negro, boton_siguiente_rect, 2, border_radius=15)
    # Botones de paginación grandes y centrados a la izquierda y derecha abajo

    texto_anterior = fuente_boton.render("Anterior", True, negro)
    texto_siguiente = fuente_boton.render("Siguiente", True, negro)
    rect_texto_anterior = texto_anterior.get_rect(center=boton_anterior_rect.center)
    rect_texto_siguiente = texto_siguiente.get_rect(center=boton_siguiente_rect.center)
    ventana.blit(texto_anterior, rect_texto_anterior)
    ventana.blit(texto_siguiente, rect_texto_siguiente)

def main_nivel_1():
    mezclar_opciones_juego()
    juego_corriendo = True
    reloj = pygame.time.Clock()
    arrastrando_item = False
    idx_arrastrado = None 
    offset_arrastre = (0,0)
    num_aciertos = 0
    num_errores = 0
    gato_piensa_item = random.choice(opciones_alimentos)
    mensaje_feedback = ""
    color_feedback = color_borde
    timer_feedback = 0
    duracion_feedback = 1500
    mostrar_flecha_izq = False
    mostrar_flecha_der = False
    tiempo_flecha = 0
    duracion_flecha = 1000  

    global pagina_actual

    gato_sprite = GatoAnimado(gato_frames, (100, 130))
    grupo_sprites_gato = pygame.sprite.Group(gato_sprite)

    while juego_corriendo:
        dt = reloj.tick(40) / 1000
        boton_anterior_rect = pygame.Rect(40, 650, 145, 60)
        boton_siguiente_rect = pygame.Rect(ancho - 170, 650, 145, 60)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if pygame.time.get_ticks() - timer_feedback > duracion_feedback:
                    if boton_anterior_rect.collidepoint(evento.pos):
                        if pagina_actual > 0:
                            pagina_actual -= 1
                        else:
                            mostrar_flecha_der = True
                            tiempo_flecha = pygame.time.get_ticks()
                    elif boton_siguiente_rect.collidepoint(evento.pos):
                        max_pagina = (len(opciones_mezcladas) - 1) // opciones_por_pagina
                        # Solo puede avanzar si NO está en la última página
                        if pagina_actual < max_pagina:
                            pagina_actual += 1
                        else:
                            mostrar_flecha_izq = True
                            tiempo_flecha = pygame.time.get_ticks()
                    else:
                        opciones_visibles, rects_opciones_visibles = obtener_opciones_y_rects_visibles()
                        for idx, rect in enumerate(rects_opciones_visibles):
                            if rect.collidepoint(evento.pos):
                                arrastrando_item = True
                                idx_arrastrado = idx
                                offset_arrastre = (evento.pos[0] - rect.x, evento.pos[1] - rect.y)
                                break
                    off_on_vol(evento)
            elif evento.type == pygame.MOUSEBUTTONUP:
                if arrastrando_item:
                    pos_soltar = (evento.pos[0] - offset_arrastre[0], evento.pos[1] - offset_arrastre[1])
                    rect_soltar = pygame.Rect(*pos_soltar, 100, 100)
                    if rect_bandeja.colliderect(rect_soltar):
                        opciones_visibles, _ = obtener_opciones_y_rects_visibles()
                        item_arrastrado = opciones_visibles[idx_arrastrado]
                        if item_arrastrado['nombre'] == gato_piensa_item['nombre']:
                            mensaje_feedback = "Excelente"
                            color_feedback = verde_oscuro
                            num_aciertos += 1
                            sonido_acierto.play()
                            timer_feedback = pygame.time.get_ticks() 
                        else:
                            mensaje_feedback = "Intenta de nuevo"
                            color_feedback = rojo
                            num_errores += 1
                            sonido_error.play()
                            timer_feedback = pygame.time.get_ticks() 
                        if num_aciertos + num_errores == 6:
                            finalizar_juego(num_aciertos, num_errores)
                            timer_feedback = pygame.time.get_ticks()
                            juego_corriendo = False
                        gato_piensa_item = random.choice(opciones_alimentos)
                        mezclar_opciones_juego()
                    arrastrando_item = False
                    idx_arrastrado = None

        pos_arrastre = None
        if arrastrando_item and idx_arrastrado is not None:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            pos_arrastre = (mouse_x - offset_arrastre[0], mouse_y - offset_arrastre[1])
        mouse_pos = pygame.mouse.get_pos()
        resalta_ant = boton_anterior_rect.collidepoint(mouse_pos)
        resalta_sig = boton_siguiente_rect.collidepoint(mouse_pos)
        ventana.blit(fondo_juego, (0, 0))
        dibujar_escena_juego(gato_piensa_item, idx_arrastrado, pos_arrastre, presionado_sig=resalta_sig, presionado_ant=resalta_ant)
        grupo_sprites_gato.update(dt)
        grupo_sprites_gato.draw(ventana)

        # Mostrar flecha si es necesario
        ahora = pygame.time.get_ticks()
        if mostrar_flecha_izq and ahora - tiempo_flecha < duracion_flecha:
            ventana.blit(retroceder, (boton_siguiente_rect.centerx - 20, boton_siguiente_rect.y - 70))
        if mostrar_flecha_der and ahora - tiempo_flecha < duracion_flecha:
            ventana.blit(avanzar, (boton_anterior_rect.centerx - 20, boton_anterior_rect.y - 70))
        # Desactiva la flecha si ya pasó el tiempo
        if mostrar_flecha_izq and ahora - tiempo_flecha >= duracion_flecha:
            mostrar_flecha_izq = False
        if mostrar_flecha_der and ahora - tiempo_flecha >= duracion_flecha:
            mostrar_flecha_der = False

        if mensaje_feedback:
            texto_feedback = fuente_comentarios.render(mensaje_feedback, True, color_feedback)
            rect_texto_feedback = texto_feedback.get_rect(topleft=(15, 50))
            ventana.blit(texto_feedback, rect_texto_feedback)
            if pygame.time.get_ticks() - timer_feedback > duracion_feedback:
                mensaje_feedback = ""
        off_on_vol()
        pygame.display.flip()

    pygame.quit()

def main_nivel_2():
    juego_activo = True
    aciertos = 0
    errores = 0
    mensaje = ""
    color_msg = verde_oscuro
    timer_feedback = 0
    duracion_feedback = 1500

    # Fuente para la suma dentro de la nube de pensamiento
    fuente_suma = pygame.font.SysFont("Open Sans", 120, True, False)
    
    # Al comenzar nos preparemos una suma 
    siguiente()

    while juego_activo:
        instrucciones = "NOTA: Selecciona la respuesta correcta en la 4 opciones disponibles para la suma que aparece en el pensamiento del gato."
        super = fuente_ins.render(instrucciones, True, negro)
        rect_inst = super.get_rect(center=(ancho//2, 20))
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                opciones_visibles, rects_opciones = obtener_opciones_y_rects_visibles()
                for idx, rect in enumerate(rects_opciones):
                    if rect.collidepoint(evento.pos):
                        opcion = opciones_visibles[idx]['valor']
                        if opcion == resultado_suma:
                            aciertos += 1
                            mensaje = "Excelente"
                            color_msg = verde_oscuro
                            sonido_acierto.play()
                        else:
                            errores += 1
                            mensaje = "Intenta de nuevo"
                            color_msg = rojo
                            sonido_error.play()
                        timer_feedback = pygame.time.get_ticks()
                        siguiente()  # Prepara nueva suma y opciones

                        if aciertos + errores == 6:
                            finalizar_juego(aciertos, errores)
                            juego_activo = False
                        break
                off_on_vol(evento)    
        # Interfaz de pantalla
        ventana.fill(color_fondo_principal)
        ventana.blit(fondo_juego, (0, 0))
        ventana.blit(gato_img_estatica, (85, 130))  # Gato estático en la parte izquierda

        # DIBUJA LA NUBE DE PENSAMIENTO
        ventana.blit(pensamiento, (500, 40))  # Nube en la parte superior

        # DIBUJA LA OPERACIÓN DENTRO DE LA NUBE DE PENSAMIENTO
        suma_texto = f"{num1} + {num2}"
        texto_suma_nube = fuente_suma.render(suma_texto, True, negro)
        rect_texto_suma_nube = texto_suma_nube.get_rect(center=(700, 150))  # Centrar en la nube de pensamiento
        ventana.blit(texto_suma_nube, rect_texto_suma_nube)

        # Dibuja las opciones numericas
        opciones_visibles, rects_opciones = obtener_opciones_y_rects_visibles()
        for idx, opt in enumerate(opciones_visibles):
            pygame.draw.rect(ventana, color_opcion_fondo, rects_opciones[idx], border_radius=25)
            ventana.blit(opt['superficie_texto'], opt['superficie_texto'].get_rect(center=rects_opciones[idx].center))

        if mensaje:
            texto_feed = fuente_comentarios.render(mensaje, True, color_msg)
            rect_feed = texto_feed.get_rect(topleft=(20, 60))
            ventana.blit(texto_feed, rect_feed)
            if pygame.time.get_ticks() - timer_feedback > duracion_feedback:
                mensaje = ""
        
        ventana.blit(super, rect_inst)
        off_on_vol()
        pygame.display.flip()
def pantalla_bienvenida():
    en_bienvenida = True
    accion_elegida = None
    reloj = pygame.time.Clock()

    # Textos de los botones
    texto_jugar = fuente_principal.render("JUGAR", True, negro)
    texto_salir = fuente_principal.render("- SALIR", True, negro)
    
    texto_regresar = fuente_principal.render("REGRESAR", True, negro)
    rect_texto_regresar = texto_regresar.get_rect(center=(ancho // 2, 600))
    boton_regresar_rect = rect_texto_regresar.inflate(40, 20)

    # Rectángulos para los textos de los botones
    rect_texto_jugar = texto_jugar.get_rect(center=(1000, 350))
    rect_texto_salir = texto_salir.get_rect(center=(1000, 480))

    # Rectángulos de los botones clickeables
    pad_x, pad_y = 30, 10
    rect_boton_jugar = rect_texto_jugar.inflate(pad_x * 2, pad_y * 2)
    rect_boton_salir = rect_texto_salir.inflate(pad_x * 2, pad_y * 2)

    while en_bienvenida:
        reloj.tick(40) # Limita FPS
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = evento.pos
                if rect_boton_jugar.collidepoint(pos_mouse):
                    accion_elegida = "jugar"
                    en_bienvenida = False
                elif rect_boton_salir.collidepoint(pos_mouse):
                    accion_elegida = "salir"
                    en_bienvenida = False
                elif boton_regresar_rect.collidepoint(pos_mouse):
                    mostrar_niveles()
                    en_bienvenida = False
                off_on_vol(evento)

        ventana.fill(azul_cielo)
        ventana.blit(fondo_bienvenida, (0, 0))
        ventana.blit(gato_img_estatica, pos_gato) # Gato estático
        ventana.blit(letras_bienvenida, (400, 5))
        
        # Dibujar botones de JUGAR y SALIR
        pygame.draw.rect(ventana, verde, rect_boton_jugar, border_radius=20)
        pygame.draw.rect(ventana, rojo, rect_boton_salir, border_radius=20)
        
        # Dibujar texto en los botones
        ventana.blit(texto_jugar, rect_texto_jugar)
        ventana.blit(texto_salir, rect_texto_salir)
        
        # Dibujar botón de REGRESAR
        pygame.draw.rect(ventana, (255, 255, 255), boton_regresar_rect, border_radius=15)
        pygame.draw.rect(ventana, color_borde, boton_regresar_rect, 2, border_radius=15)
        ventana.blit(texto_regresar, rect_texto_regresar)
        off_on_vol()
        pygame.display.flip()

        if accion_elegida == "jugar":
            return
        elif accion_elegida == "salir":
            pygame.quit()
            exit()
def mostrar_niveles():
    en_niveles = True
    fuente_niveles = fuente_principal

    # Textos y rectángulos de los botones de nivel
    texto_nivel1 = fuente_niveles.render("Nivel 1", True, negro)
    texto_nivel2 = fuente_niveles.render("Nivel 2", True, negro)
   
    rect_boton_nivel1 = pygame.Rect(350, 480, 280, 80)  
    rect_boton_nivel2 = pygame.Rect(670, 480, 280, 80)

    while en_niveles:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_boton_nivel1.collidepoint(evento.pos):
                    pantalla_bienvenida() # Regresar a la bienvenida antes de iniciar el juego
                    main_nivel_1() # Iniciar el juego principal
                elif rect_boton_nivel2.collidepoint(evento.pos):
                    pantalla_bienvenida()
                    siguiente()
                    main_nivel_2()
                off_on_vol(evento)
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    en_niveles = False # Salir de la pantalla de niveles
        
        ventana.fill(azul_cielo)
        ventana.blit(fondo_bienvenida, (0, 0))
        ventana.blit(letras_bienvenida, (400, 5))
        
        texto_titulo_niveles = fuente_principal.render("NIVEL DE DIFICULTAD", True, naranja)
        ventana.blit(texto_titulo_niveles, texto_titulo_niveles.get_rect(center=(ancho // 2, 340)))


        # ---------- Dibujo de botón Nivel 1 ----------
        pygame.draw.rect(ventana, (255,255,255), rect_boton_nivel1, border_radius=24)       # Fondo blanco, esquinas redondeadas
        pygame.draw.rect(ventana, color_borde, rect_boton_nivel1, width=4, border_radius=24) # Borde azul, ancho 4
        ventana.blit( texto_nivel1,texto_nivel1.get_rect(center=rect_boton_nivel1.center) )

        # ---------- Dibujo de botón Nivel 2 ----------
        pygame.draw.rect(ventana, (255,255,255), rect_boton_nivel2, border_radius=24)
        pygame.draw.rect(ventana, color_borde, rect_boton_nivel2, width=4, border_radius=24)
        ventana.blit(texto_nivel2, texto_nivel2.get_rect(center=rect_boton_nivel2.center))
        off_on_vol()

        pygame.display.flip()
def finalizar_juego(aciertos, errores):
    en_fin_juego = True
    reloj = pygame.time.Clock()
    fuente_fin = pygame.font.SysFont("Arial", 48, True)
    fuente_botones = fuente_principal # Fuente para los botones SI/NO

    # Botones SI y NO
    texto_si_btn = fuente_botones.render("SI", True, negro)
    texto_no_btn = fuente_botones.render("NO", True, negro)
    rect_si_texto = texto_si_btn.get_rect(center=(700, 500))
    rect_no_texto = texto_no_btn.get_rect(center=(900, 500))
    boton_si_rect = rect_si_texto.inflate(40, 20)
    boton_no_rect = rect_no_texto.inflate(40, 20)

    while en_fin_juego:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_si_rect.collidepoint(evento.pos):
                    mostrar_niveles() # Regresar a la selección de niveles
                    return # Sale de esta función para que el juego continúe
                elif boton_no_rect.collidepoint(evento.pos):
                    en_fin_juego = False # Termina el bucle de fin de juego
                    pygame.quit()
                    exit()
                off_on_vol(evento)
        ventana.fill(azul_cielo)
        ventana.blit(fondo_bienvenida, (0, 0))
        ventana.blit(gato_img_estatica, pos_gato)

        texto_resultados = fuente_principal.render(f"ACIERTOS: {aciertos}   ERRORES: {errores}", True, rojo)
        rect_texto_resultados = texto_resultados.get_rect(center=(800, 150))
        ventana.blit(texto_resultados, rect_texto_resultados)

        texto_pregunta = fuente_fin.render("¿Quieres volver a intentar?", True, negro)
        rect_texto_pregunta = texto_pregunta.get_rect(center=(800, 300))
        ventana.blit(texto_pregunta, rect_texto_pregunta)
        
        # Dibujar botones SI/NO
        pygame.draw.rect(ventana, amarillo, boton_si_rect, border_radius=15)
        pygame.draw.rect(ventana, negro, boton_si_rect, 2, border_radius=15)
        ventana.blit(texto_si_btn, rect_si_texto)

        pygame.draw.rect(ventana, amarillo, boton_no_rect, border_radius=15)
        pygame.draw.rect(ventana, negro, boton_no_rect, 2, border_radius=15)
        ventana.blit(texto_no_btn, rect_no_texto) 
        off_on_vol()
        pygame.display.flip()
def pantalla_informativa():
    global volumen
    en_info = True
    fuente_info = fuente_principal
    texto_continuar_btn = fuente_info.render("CONTINUAR", True, negro)
    rect_texto_continuar = texto_continuar_btn.get_rect(center=(ancho // 2, 610))
    btn_continuar_rect = rect_texto_continuar.inflate(40, 20)
    
    while en_info:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if btn_continuar_rect.collidepoint(evento.pos):
                    en_info = False  # Sale de la pantalla informativa
                off_on_vol(evento)
        ventana.fill(azul_cielo)
        ventana.blit(fondo_bienvenida, (0, 0))
        
        # Centrar la imagen de información
        ventana.blit(info, (265, 25))

        # Dibujar el botón
        pygame.draw.rect(ventana, (255, 255, 255), btn_continuar_rect, border_radius=15)
        pygame.draw.rect(ventana, negro, btn_continuar_rect, 2, border_radius=15)
        ventana.blit(texto_continuar_btn, rect_texto_continuar) 
        off_on_vol()
        pygame.display.flip()
def off_on_vol(momen=None):
    global volumen
    if momen is not None and momen.type == pygame.MOUSEBUTTONDOWN:
        if volumen_rect.collidepoint(momen.pos):
            if volumen==0:
                volumen=1
                sonido_musica.set_volume(0.3)
            else:
                volumen=0
                sonido_musica.set_volume(0)
    if volumen==0:
        ventana.blit(vol_off,volumen_rect.topleft)
    else:
        ventana.blit(vol_on,volumen_rect.topleft) 
def reglas():
    regla = True
    while regla:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                regla = False

        ventana.fill(azul_cielo)
        ventana.blit(fondo_bienvenida, (0, 0))
        ventana.blit(gato_img_estatica, pos_gato)
        ventana.blit(letras_bienvenida, (400, 5))
       
        rect_img = img_reglas.get_rect(center=( 850, 500))
        ventana.blit(img_reglas, rect_img)
        
        pygame.display.flip()

if __name__ == "__main__":
    pantalla_informativa()
    reglas()
    mostrar_niveles()                                                                                         