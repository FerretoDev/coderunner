from .jugador import Jugador
from .laberinto import Laberinto
from .personaje import Personaje


class Computadora(Personaje):
    """Clase que representa al jugador en el juego, hereda de Personaje"""

    def __init__(
        self,
        posicion: tuple[int, int],
        velocidad: float = 1.1,
    ):
        super().__init__(posicion, velocidad)

    def perseguir(self, jugador: Jugador, laberinto: Laberinto) -> None:
        """Mueve al jugador hacia la posición del objetivo (computadora)"""
        pass

    def mover(self, direccion: str) -> None:
        """Mueve a la computadora en la dirección especificada."""
        pass
