'''
Parámetros disponibles para usar
'''
import os.path
# No modificar

ANCHO_LABERINTO = 16
LARGO_LABERINTO = 16

DURACION_NIVEL_INICIAL = 120 # Corresponde a la duración en el primer laberinto, en segundos
VELOCIDAD_LOBO = 5 # Corresponde a la velocidad en el primer laberinto
PONDERADOR_LABERINTO_1 = 1
PONDERADOR_LABERINTO_2 = 0.9
PONDERADOR_LABERINTO_3 = 0.8
PUNTAJE_LOBO = 3
CANTIDAD_VIDAS = 3 
VELOCIDAD_CONEJO = 10
VELOCIDAD_ZANAHORIA = 8

TIEMPO_BOMBA = 5
PUNTAJE_INF = 350

# Agregue los parámetros necesarios

# Constantes para las ventanas
DIM_CASILLA = 48                    #Alto y ancho de casillas del juego; debe ser divisible en 3
JUEGO_ALTO = DIM_CASILLA * 16       #Alto de ventana de juego
JUEGO_ANCHO = DIM_CASILLA * 24      #Ancho de ventana de juego

# Calculo correspondiente para los ponderadores
POND_ACUMULADOS = [PONDERADOR_LABERINTO_1,
                   PONDERADOR_LABERINTO_1 * PONDERADOR_LABERINTO_2,
                   PONDERADOR_LABERINTO_1 * PONDERADOR_LABERINTO_2 * PONDERADOR_LABERINTO_3]

# Frecuencia arbitraria elegida para el disparo del cañón
FRECUENCIA_CANON = VELOCIDAD_ZANAHORIA / 20


# Frecuencia de refresco de sprite por cada casilla que avance.
#     Cuando el valor es 1, el sprite es estático
#     Entre 1 y 2, se ocupan dos sprites
#     Sobre 2 se ocupa los tres sprites
#     Sobre 3 se reutilizan los sprites
INTERCALADO_LOBO = 3
INTERCALADO_CONEJO = 3

# Diccionarios para componer paths
SPRITES_CONEJO = {"s": ["conejo_abajo_1.png", "conejo_abajo_2.png", "conejo_abajo_3.png"],
                  "w": ["conejo_arriba_1.png", "conejo_arriba_2.png", "conejo_arriba_3.png"],
                  "a": ["conejo_izquierda_1.png", "conejo_izquierda_2.png", 
                           "conejo_izquierda_3.png"],
                  "d": ["conejo_derecha_1.png", "conejo_derecha_2.png", 
                            "conejo_derecha_3.png"]}

SPRITES_LOBOS = {"a": ["lobo_horizontal_izquierda_1.png", "lobo_horizontal_izquierda_2.png",
                        "lobo_horizontal_izquierda_3.png", ],
                  "d": ["lobo_horizontal_derecha_1.png", "lobo_horizontal_derecha_2.png",
                        "lobo_horizontal_derecha_3.png", ],
                  "w": ["lobo_vertical_arriba_1.png", "lobo_vertical_arriba_2.png",
                        "lobo_vertical_arriba_3.png", ],
                  "s": ["lobo_vertical_abajo_1.png", "lobo_vertical_abajo_2.png",
                        "lobo_vertical_abajo_3.png", ]}

SPRITES_CANON = {"w": "canon_arriba.png", "a": "canon_izquierda.png", 
                 "s": "canon_abajo.png", "d": "canon_derecha.png"}

SPRITES_ZANAH = {"w": "zanahoria_arriba.png", "a": "zanahoria_izquierda.png", 
                 "s": "zanahoria_abajo.png", "d": "zanahoria_derecha.png"}

INGLES_A_TECLA = {"U": "w", "D": "s", "L": "a", "R": "d"}


# Paths fijos
PATH_LOGO = os.path.join("assets", "sprites", "logo.png")
PATH_TABLERO_1 = os.path.join("assets", "laberintos", "tablero_1.txt")
PATH_TABLERO_2 = os.path.join("assets", "laberintos", "tablero_2.txt")
PATH_TABLERO_3 = os.path.join("assets", "laberintos", "tablero_3.txt")
PATH_B_FONDO = os.path.join("assets", "sprites", "bloque_fondo.jpeg")
PATH_B_PARED = os.path.join("assets", "sprites", "bloque_pared.jpeg")
PATH_DERROTA = os.path.join("assets", "sonidos", "derrota.wav")
PATH_VICTORIA = os.path.join("assets", "sonidos", "victoria.wav")