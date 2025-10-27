from abc import ABC, abstractmethod  # Importa lo necesario para hacer una clase base (abstracta).

class Personaje(ABC):
    """Clase base para personajes, como Jugador o Computadora."""

    def __init__(
        self,
        x: int,
        y: int,
        radio: int,
        velocidad: float = 1.0,
    ):
        # Este método se llama cuando creas un personaje.
        # Guarda la posición (x, y), el tamaño (radio) y la velocidad.
        self._velocidad = velocidad     # Cuánto se mueve el personaje en cada paso.
        self._x = x                     # Posición horizontal.
        self._y = y                     # Posición vertical.
        self._radio = radio             # Tamaño del personaje.
        self._posicion = (x, y)         # Guarda la posición como tupla (x, y).

    @property
    def posicion(self) -> tuple[int, int]:
        # Devuelve la posición actual como una tupla (x, y).
        return self._posicion

    @posicion.setter
    def posicion(self, nueva_posicion: tuple[int, int]) -> None:
        # Permite cambiar la posición del personaje usando una tupla (x, y).
        self._posicion = nueva_posicion

    @property
    def velocidad(self) -> float:
        # Devuelve la velocidad actual del personaje.
        return self._velocidad

    @velocidad.setter
    def velocidad(self, nueva_velocidad: float) -> None:
        # Permite cambiar la velocidad del personaje.
        self._velocidad = nueva_velocidad

    @property
    def x(self) -> int:
        # Devuelve la posición X (horizontal).
        return self._x

    @x.setter
    def x(self, nuevo_x: int) -> None:
        # Permite cambiar la posición X.
        self._x = nuevo_x

    @property
    def y(self) -> int:
        # Devuelve la posición Y (vertical).
        return self._y

    @y.setter
    def y(self, nuevo_y: int) -> None:
        # Permite cambiar la posición Y.
        self._y = nuevo_y

    @property
    def radio(self) -> int:
        # Devuelve el tamaño del personaje.
        return self._radio

    @radio.setter
    def radio(self, nuevo_radio: int) -> None:
        # Permite cambiar el tamaño del personaje.
        self._radio = nuevo_radio

    @abstractmethod
    def mover(self, direccion: str) -> None:
        # Este método es obligatorio en las clases hijas.
        # Aquí se debe escribir cómo se mueve el personaje según la dirección (ejemplo: "arriba", "abajo").
        pass
