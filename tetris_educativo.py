import pygame
import random

# Configuración del juego
ANCHO_BLOQUE = 30
COLUMNAS = 10
FILAS = 20
ANCHO = COLUMNAS * ANCHO_BLOQUE
ALTO = FILAS * ANCHO_BLOQUE

# Definición de colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
COLORES = [
    (0, 240, 240),
    (0, 0, 240),
    (240, 160, 0),
    (240, 240, 0),
    (0, 240, 0),
    (160, 0, 240),
    (240, 0, 0)
]

# Formas de las piezas Tetris
PIEZAS = [
    [[1, 1, 1, 1]],
    [[2, 0, 0], [2, 2, 2]],
    [[0, 0, 3], [3, 3, 3]],
    [[4, 4], [4, 4]],
    [[0, 5, 5], [5, 5, 0]],
    [[0, 6, 0], [6, 6, 6]],
    [[7, 7, 0], [0, 7, 7]]
]

# Cada pieza tendrá un número asociado para preguntas matemáticas
NUMEROS_PIEZA = list(range(1, 10))

class Pieza:
    def __init__(self, forma):
        self.forma = forma
        self.x = COLUMNAS // 2 - len(forma[0]) // 2
        self.y = 0
        self.numero = random.choice(NUMEROS_PIEZA)

    def rotar(self):
        self.forma = [list(fila) for fila in zip(*self.forma[::-1])]


def crear_tablero():
    return [[None for _ in range(COLUMNAS)] for _ in range(FILAS)]


def colision(tablero, pieza):
    for i, fila in enumerate(pieza.forma):
        for j, valor in enumerate(fila):
            if valor and (
                j + pieza.x < 0 or
                j + pieza.x >= COLUMNAS or
                i + pieza.y >= FILAS or
                tablero[i + pieza.y][j + pieza.x] is not None
            ):
                return True
    return False


def fijar_pieza(tablero, pieza):
    for i, fila in enumerate(pieza.forma):
        for j, valor in enumerate(fila):
            if valor:
                tablero[pieza.y + i][pieza.x + j] = (pieza.numero, valor)


def filas_completas(tablero):
    completas = []
    for i, fila in enumerate(tablero):
        if None not in fila:
            completas.append(i)
    return completas


def preguntar_suma(linea, fuente, pantalla):
    numeros = [n for n, _ in linea]
    suma = sum(numeros)
    respuesta = ""
    preguntando = True
    while preguntando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    preguntando = False
                elif evento.key == pygame.K_BACKSPACE:
                    respuesta = respuesta[:-1]
                elif evento.unicode.isdigit():
                    respuesta += evento.unicode
        pantalla.fill(NEGRO)
        texto = fuente.render(f"¿Cuál es la suma de {numeros}?", True, BLANCO)
        pantalla.blit(texto, (10, ALTO // 2 - 30))
        entrada = fuente.render(respuesta, True, BLANCO)
        pantalla.blit(entrada, (10, ALTO // 2 + 10))
        pygame.display.flip()
    try:
        return int(respuesta) == suma
    except ValueError:
        return False


def eliminar_filas(tablero, filas, fuente, pantalla):
    for i in filas:
        if preguntar_suma(tablero[i], fuente, pantalla):
            del tablero[i]
            tablero.insert(0, [None for _ in range(COLUMNAS)])


def dibujar_tablero(tablero, pantalla, fuente):
    for y, fila in enumerate(tablero):
        for x, celda in enumerate(fila):
            if celda is not None:
                numero, color_idx = celda
                color = COLORES[color_idx - 1]
                pygame.draw.rect(
                    pantalla,
                    color,
                    (x * ANCHO_BLOQUE, y * ANCHO_BLOQUE, ANCHO_BLOQUE, ANCHO_BLOQUE)
                )
                texto = fuente.render(str(numero), True, NEGRO)
                pantalla.blit(texto, (x * ANCHO_BLOQUE + 8, y * ANCHO_BLOQUE + 5))
    # Dibuja la cuadrícula
    for x in range(COLUMNAS):
        for y in range(FILAS):
            rect = pygame.Rect(x * ANCHO_BLOQUE, y * ANCHO_BLOQUE, ANCHO_BLOQUE, ANCHO_BLOQUE)
            pygame.draw.rect(pantalla, BLANCO, rect, 1)


def juego():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Tetris Educativo")
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("Arial", 18)

    tablero = crear_tablero()
    pieza = Pieza(random.choice(PIEZAS))
    caida_evento = pygame.USEREVENT + 1
    pygame.time.set_timer(caida_evento, 1000)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == caida_evento:
                pieza.y += 1
                if colision(tablero, pieza):
                    pieza.y -= 1
                    fijar_pieza(tablero, pieza)
                    filas = filas_completas(tablero)
                    if filas:
                        eliminar_filas(tablero, filas, fuente, pantalla)
                    pieza = Pieza(random.choice(PIEZAS))
                    if colision(tablero, pieza):
                        pygame.quit()
                        return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    pieza.x -= 1
                    if colision(tablero, pieza):
                        pieza.x += 1
                elif evento.key == pygame.K_RIGHT:
                    pieza.x += 1
                    if colision(tablero, pieza):
                        pieza.x -= 1
                elif evento.key == pygame.K_DOWN:
                    pieza.y += 1
                    if colision(tablero, pieza):
                        pieza.y -= 1
                elif evento.key == pygame.K_UP:
                    pieza.rotar()
                    if colision(tablero, pieza):
                        for _ in range(3):
                            pieza.rotar()

        pantalla.fill(NEGRO)
        dibujar_tablero(tablero, pantalla, fuente)
        # Dibuja pieza actual
        for i, fila in enumerate(pieza.forma):
            for j, valor in enumerate(fila):
                if valor:
                    color = COLORES[valor - 1]
                    x = (pieza.x + j) * ANCHO_BLOQUE
                    y = (pieza.y + i) * ANCHO_BLOQUE
                    pygame.draw.rect(pantalla, color, (x, y, ANCHO_BLOQUE, ANCHO_BLOQUE))
                    numero = fuente.render(str(pieza.numero), True, NEGRO)
                    pantalla.blit(numero, (x + 8, y + 5))
        pygame.display.flip()
        reloj.tick(60)


if __name__ == "__main__":
    juego()
