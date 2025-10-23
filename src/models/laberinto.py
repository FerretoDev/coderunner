import json

import pygame

from .obsequio import Obsequio

AZUL = (0, 0, 255)  # Color de los muros del laberinto


class Laberinto:
    """
    Clase que representa el laberinto del juego.
    
    El laberinto está compuesto por:
        Muros: Paredes que el jugador no puede atravesar
        Pasillos: Espacios por donde el jugador puede moverse
        Obsequios: Items que el jugador puede recolectar
    """

    def __init__(
        self,
    ):
        
        """
        Inicializa un nuevo laberinto vacío.
        Las listas de muros, pasillos y obsequios se llenarán al cargar el nivel.
        """
        
        self._muros = list[tuple[int, int]]
        self._pasillos = list[tuple[int, int]]
        self._obsequios = list[tuple[int, int]]

    def es_paso_valido(self, posicion: tuple[int, int]) -> bool:
        """
        Verifica si una posición es válida para el movimiento del jugador.

        Parámetros:
            posicion: Coordenadas (x, y) a verificar
        Retorna:
            bool: True si es un pasillo u obsequio, False si es un muro
        """
        return posicion in self._pasillos or posicion in self._obsequios

    def obtener_obsequio(self, posicion: tuple[int, int]) -> Obsequio | None:
        """Verifica si hay un obsequio en la posición dada y lo elimina si es así"""
        ...

    def cargar_desde_archivo(self, archivo: str) -> None:
        """Carga el laberinto desde un archivo."""
        ...

    def validar_estructura(self, datos: dict) -> bool:
        """Valida que el laberinto tenga una estructura correcta."""
        return True

    import pygame

    TAM_CELDA = 32

    laberinto = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    def obtener_rectangulos(self):
        """
        Genera los rectángulos de colisión para los muros del laberinto.

        Retorna:
            list: Lista de objetos Rect de pygame que representan los muros
        """
        rectangulos = []
        for fila in range(len(self.laberinto)):
            for col in range(len(self.laberinto[0])):
                if self.laberinto[fila][col] == 1:  # 1 representa un muro
                    x = col * self.TAM_CELDA
                    y = fila * self.TAM_CELDA
                    rect = pygame.Rect(x, y, self.TAM_CELDA, self.TAM_CELDA)
                    rectangulos.append(rect)
        return rectangulos

    def dibujar_laberinto(self, pantalla):
        """
        Dibuja el laberinto en la pantalla.

        Los muros se dibujan como rectángulos azules.

        Parámetros:
            pantalla: Superficie de pygame donde se dibujará el laberinto
        """
        for fila in range(len(self.laberinto)):
            for col in range(len(self.laberinto[0])):
                if self.laberinto[fila][col] == 1:
                    x = col * self.TAM_CELDA
                    y = fila * self.TAM_CELDA
                    pygame.draw.rect(
                        pantalla, AZUL, (x, y, self.TAM_CELDA, self.TAM_CELDA)
                    )
