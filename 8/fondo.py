#==============================
#       FONDO DEL JUEGO
# =============================
 
# Importamos las herramientas que vamos a usar

import pygame                      # Esta es la libreria que usamos para hacer el videojuego en Python.
import random                      # Nos permite usar numeros al azar. Muy util para que las nubes no sean todas iguales.
import os                          # Nos ayuda a buscar archivos (como imagenes) en carpetas de la computadora.
from constantes import ANCHO, ALTO # Importamos el ancho y alto de la pantalla desde otro archivo. 

# Creamos una clase llamada Fondo, que se va a encargar de dibujar el cielo, montañas, nubes y algunas imagenes PNG.

class Fondo:

    def __init__(self, cantidad_nubes = 7):

        # Al iniciar la clase, se crean varias nubes al azar usando una funcion especial.

        self.nubes = [self._crear_nube() for _ in range(cantidad_nubes)]

        # Creamos la ruta donde estan las imagenes PNG de los fondos.

        ruta_base = os.path.join(os.path.dirname(__file__), "imagenes")

        # Cargamos varias imagenes PNG para superponerlas al fondo.

        self.imagenes_superpuestas = [
            {"imagen": self._cargar_imagen(os.path.join(ruta_base, "Fondo1.png")), "pos": (0, 0)},
            {"imagen": self._cargar_imagen(os.path.join(ruta_base, "Fondo2.png")), "pos": (0, 0)},
            {"imagen": self._cargar_imagen(os.path.join(ruta_base, "Fondo3.png")), "pos": (0, 0)},
            {"imagen": self._cargar_imagen(os.path.join(ruta_base, "Fondo4.png")), "pos": (0, 0)},
            {"imagen": self._cargar_imagen(os.path.join(ruta_base, "Fondo5.png")), "pos": (0, 0)},
            {"imagen": self._cargar_imagen(os.path.join(ruta_base, "Fondo6.png")), "pos": (0, 0)},
            {"imagen": self._cargar_imagen(os.path.join(ruta_base, "Fondo7.png")), "pos": (0, 0)}
        ]

# Funcion para cargar una imagen desde el archivo y escalarla al tamaño de la pantalla

    def _cargar_imagen(self, ruta):
      try:
           
           # Cargamos la imagen con transparencia (convert_alpha)

           imagen = pygame.image.load(ruta).convert_alpha()

           # Ajustamos el tamaño de la imagen para que cubra toda la pantalla

           imagen_escalada = pygame.transform.scale(imagen, (ANCHO, ALTO))
           return imagen_escalada
      except pygame.error as e:
          
          # Si hay un error (por ejemplo, la imagen no existe), mostramos un mensaje

          print(f"No se pudo cargar la imagen {ruta}: {e}")
          return pygame.Surface((0, 0), pygame.SRCALPHA) # Devolvemos una imagen vacia invisible
      
# Esta funcion crea una nube con posiciones y tamaños al azar

    def _crear_nube(self):
     return {
         "x": random.randint(0, ANCHO), # Posicion horizontal aleatoria
         "y": random.randint(20, 150), # Altura aleatoria, cerca del cielo
         "escala": random.randint(30, 60), # Tamaño de la nube
         "velocidad": random.uniform(0.2, 0.8), # Que tan rapido se mueve
         "transparencia": random.randint(140, 220) # Que tan transparente es (como humo suave)
    }

# Esta funcion mueve las nubes hacia la derecha todo el tiempo

    def actualizar(self):
     for nube in self.nubes:
      nube["x"] += nube["velocidad"] # Avanza segun su velocidad
      if nube ["x"] > ANCHO + 100: # Si la nube ya salio de la pantalla
         nueva = self._crear_nube() # Se reemplaza por una nueva nube
         nueva ["x"] = -120 # Que empieza desde la izquierda
         nube.update(nueva) # Actualizamos la nube vieja con los nuevos datos

# Esta funcion dibuja todo el fondo: Cielo, Montañas, Imagenes PNG y Nubes

    def dibujar(self, pantalla):
      pantalla.fill((135, 206, 250)) # Color azul clarito como el cielo
      self._dibujar_montañas(pantalla)
      self._dibujar_imagenes_png(pantalla)
      self._dibujar_nubes(pantalla)

# Dibuja montañas usando triangulos (poligonos)

    def _dibujar_montañas(self, pantalla):
     pygame.draw.polygon(pantalla, (80, 80, 100), [(0, ALTO), (200, 320), (400, ALTO)])
     pygame.draw.polygon(pantalla, (90, 90, 110), [(300, ALTO), (500, 280), (700, ALTO)])
     pygame.draw.polygon(pantalla, (100, 100, 120), [(600, ALTO), (750, 360), (ANCHO, ALTO)])

   # Cada montaña es un triangulo con color diferente

   # Dibuja las imagenes PNG cargadas encima del fondo (como arboles, castillos, etc)

    def _dibujar_imagenes_png(self, pantalla):
      for item in self.imagenes_superpuestas:
         pantalla.blit(item["imagen"], item["pos"]) # Pega la imagen en la pantalla

# Dibuja todas las nubes usando circulos con transparencia

    def _dibujar_nubes(self, pantalla):
     for nube in self.nubes:
      x      = int(nube["x"])
      y      = int(nube["y"])
      escala = nube["escala"]
      alfa   = nube["transparencia"]

      # Creamos una superficie donde vamos a dibujar la nube (con transparencia)

      superficie = pygame.Surface((escala * 4, escala * 2), pygame.SRCALPHA)

      # Dibujamos tres circulos que forman la nube

      pygame.draw.circle(superficie, (255, 255, 255, alfa), (escala, escala), escala)
      pygame.draw.circle(superficie, (255, 255, 255, alfa), (escala * 2, escala), escala)
      pygame.draw.circle(superficie, (240, 240, 240, alfa), (int(1.5 * escala), escala - escala // 2), escala)

      # Pegamos la nube en la pantalla principal

      pantalla.blit(superficie, (x,y))
