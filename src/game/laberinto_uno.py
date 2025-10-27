"""
Demo de laberinto con jugador y colisiones rectangulares.

- Crea una ventana, un laberinto por matriz (1=pared, 0=libre) y un jugador.
- Mueve al jugador con el teclado y evita que atraviese muros.
"""

import sys  # Para cerrar la app con sys.exit()

import pygame  # Librería para ventana, eventos y rectángulos

from models.jugador import Jugador  # Clase del jugador (mueve y dibuja)
from models.laberinto import Laberinto  # Clase que construye muros y los dibuja


# Tamaño de cada celda de la grilla (coherente con tu Laberinto y Jugador)
TAM_CELDA = 32

# Mapa del laberinto: 1 = pared, 0 = espacio libre
laberinto = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Ventana y color de fondo
ANCHO = 640
ALTO = 480
NEGRO = (12, 0, 0)


class Juego:
    """Administra ventana, loop principal, jugador, laberinto y colisiones."""

    def __init__(self) -> None:
        pygame.init()  # Inicializa módulos de Pygame (ventana, eventos, etc.)
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))  # Crea la ventana
        self.bucle = True  # Controla si el juego sigue corriendo
        self.reloj = pygame.time.Clock()  # Limita FPS y mide tiempo
        self.jugador_principal = Jugador(32, 32, 16)  # x, y, tamaño (coincide con tu modelo)
        self.laberinto = Laberinto()  # Construye los muros a partir del mapa
        self.muros = self.laberinto.obtener_rectangulos()  # Lista de Rect de paredes

    def bucle_principal(self):
        """Loop del juego: eventos → movimiento → colisiones → dibujado."""
        while self.bucle:
            # Eventos de sistema (cerrar ventana)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.bucle = False
                    sys.exit()  # Sale inmediatamente del programa

            # Fondo
            self.pantalla.fill(NEGRO)  # Limpia la pantalla cada frame

            # Teclas presionadas para mover al jugador
            teclas = pygame.key.get_pressed()  # Estado actual de todas las teclas

            # Guardar posición anterior para deshacer si choca
            pos_x = self.jugador_principal.jugador_principal.x  # X previa del rect del jugador
            pos_y = self.jugador_principal.jugador_principal.y  # Y previa del rect del jugador

            # Mover jugador según teclas (la clase Jugador aplica la velocidad)
            self.jugador_principal.mover(teclas)

            # Colisiones con muros: si hay choque, vuelve a la posición anterior
            for muro in self.muros:
                if self.jugador_principal.jugador_principal.colliderect(muro):
                    self.jugador_principal.jugador_principal.x = pos_x  # Deshacer X
                    self.jugador_principal.jugador_principal.y = pos_y  # Deshacer Y
                    break  # No hace falta seguir comprobando

            # Dibujar laberinto y jugador
            self.laberinto.dibujar_laberinto(self.pantalla)  # Pinta los muros
            self.jugador_principal.dibujar_jugador_principal(self.pantalla)  # Pinta el jugador

            # Tiempo y refresco
            self.reloj.tick(60)  # Limita a 60 FPS para suavidad y menor consumo
            pygame.display.flip()  # Muestra en pantalla lo dibujado

# Ejecutar solo si se llama directamente este archivo
if __name__ == "__main__":
    juego = Juego()  # Crea la instancia del juego
    juego.bucle_principal()  # Inicia el loop principal
