# ==============================
#     CONSTANTES DEL JUEGO
# ==============================

# Aqui guardamos cosas importantes que se usan en todo el juego, como el tamaño de la pantalla, colores y tamaños de letra.

# ---------- TAMAÑO DE LA VENTANA DEL JUEGO ----------

ANCHO = 1280 # Este es el ancho de la pantalla (de izquierda a derecha).
ALTO  = 720  # Este es el alto de la pantalla (de arriba a abajo). 
FPS = 60
# ---------- CLASE QUE GUARDA COLORES QUE PUEDES USAR EN EL JUEGO ----------

class Colores:

    BLANCO      = (255, 255, 255) 
    GRIS_OSCURO = (50, 50, 50)
    AZUL        = (100, 149, 237)
    AZUL_OSCURO = (70, 70, 160)
    VERDE_CLARO = (144, 238, 144)
    NEGRO       = (0, 0, 0)

# ---------- CLASE QUE GUARDA LA FUENTE (TIPO DE LETRA) Y LOS TAMAÑOS DE TEXTO ----------

class Tipografia:

    # Nombre de la fuente (letra) que usaremos en todo el juego

    FUENTE = "Comic Sans MS" # Es una fuente divertida, facil de leer y amigable.

    # Tamaño para los diferentes textos del juego:

    TAMAÑO_TITULO         = 50 # Titulos grandes, como el nombre del juego.
    TAMAÑO_TEXTO          = 30 # Texto normal, por ejemplo instrucciones o mensajes.
    TAMAÑO_SUBTITULO      = 28 # Subtitulos, mas pequeños en el titulo.
    TAMAÑO_BOTONES        = 20 # Texto dentro de los botones.
    TAMAÑO_MENU           = 23 # Texto en el menu principal (como "Jugar", "Opciones").
    TAMAÑO_TITULO_VENTANA = 20 # Titulo de una ventana emergente (como las instrucciones).
    TAMAÑO_CUERPO_VENTANA = 14 # Texto dentro de esa ventana (detalles o explicaciones).