import pygame
from models.sistema_sonido import SistemaSonido

from models.computadora import Computadora
from models.jugador import Jugador
from models.laberinto import Laberinto
from models.registro import Registro
from models.salon_fama import SalonFama


class Juego:
    """
    Clase que maneja la lógica principal del juego.
    """

    def __init__(self):
        self._jugador = None
        self._enemigo = None
        self._laberinto = None
        self._sonido = SistemaSonido()
        self._salon_fama = SalonFama()
        self._estado = "en curso"

        # Pygame
        self.screen = None
        self.clock = pygame.time.Clock()

    def iniciar(self, nombre: str):
        """Arranca el juego con un jugador, crea los objetos iniciales"""
        ...

    def actualizar(self):
        """Cada ciclo: mover enemigo, detectar colisiones, actualizar puntaje"""

    def mostrar_estado(self):
        """Muestra cuántos puntos y vidas tiene el jugador"""

    def terminar(self):
        """Cierra el juego y guarda en el Salón de la Fama"""

    def salir(self):
        """Maneja la confirmación y cierre ordenado de la aplicación"""
