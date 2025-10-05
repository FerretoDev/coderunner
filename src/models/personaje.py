from abc import ABC, abstractmethod


class Personaje(ABC):
    """Clase abstracta que define comportamientos comunes entre Jugador y Computadora"""

    def __init__(
        self,
        posicion: tuple[int, int],
        velocidad: float = 1.0,
    ):
        self._posicion = posicion
        self._velocidad = velocidad

    @property
    def posicion(self) -> tuple[int, int]:
        return self._posicion

    @posicion.setter
    def posicion(self, nueva_posicion: tuple[int, int]) -> None:
        self._posicion = nueva_posicion

    @property
    def velocidad(self) -> float:
        return self._velocidad

    @velocidad.setter
    def velocidad(self, nueva_velocidad: float) -> None:
        self._velocidad = nueva_velocidad

    @abstractmethod
    def mover(self, direccion: str) -> None:
        """Método abstracto para mover al personaje en una dirección dada"""
        pass
