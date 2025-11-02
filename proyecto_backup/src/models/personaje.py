from abc import ABC, abstractmethod


class Personaje(ABC):
    """Clase abstracta que define comportamientos comunes entre Jugador y Computadora"""

    def __init__(
        self,
        # posicion: tuple[int, int],
        x: int,
        y: int,
        radio: int,
        velocidad: float = 1.0,
    ):
        # self._posicion = posicion
        self._velocidad = velocidad
        self._x = x
        self._y = y
        self._radio = radio

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

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, nuevo_x: int) -> None:
        self._x = nuevo_x

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, nuevo_y: int) -> None:
        self._y = nuevo_y

    @property
    def radio(self) -> int:
        return self._radio

    @radio.setter
    def radio(self, nuevo_radio: int) -> None:
        self._radio = nuevo_radio

    @abstractmethod
    def mover(self, direccion: str) -> None:
        """Método abstracto para mover al personaje en una dirección dada"""
        pass
