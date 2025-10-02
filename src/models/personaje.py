from abc import ABC
class Personaje(ABC):
    """Clase base para todos los personajes del juego."""
    def __init__(self, posicion: tuple[int, int], velocidad: float):
        self._posicion = posicion
        self._velocidad = velocidad

    @property
    def posicion(self) -> tuple[int, int]:
        return self._posicion

    @posicion.setter
    def posicion(self, posicion: tuple[int, int]):
        self._posicion = posicion
    
    @property
    def velocidad(self) -> float:
        return self._velocidad
    
    @velocidad.setter
    def velocidad(self, velocidad: float):
        self._velocidad = velocidad

    def mover(self, nueva_posicion: tuple[int, int]):
        """Mueve al personaje a una nueva posición."""
        self._posicion = nueva_posicion













