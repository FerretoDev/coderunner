from .personaje import Personaje


class Jugador(Personaje):
    """
    Clase que representa al jugador controlado por el usuario.
    """

    def __init__(
        self,
        nombre: str,
        posicion: tuple[int, int],
    ):
        super().__init__(posicion)
        self._nombre = nombre
        self._vidas = 3
        self._puntaje = 0

    def mover(self, direccion: str) -> None:
        """Mueve al jugador en la dirección especificada."""
        pass

    def sumar_puntos(self, puntos: int) -> None:
        """Suma puntos al puntaje del jugador."""
        self._puntaje += puntos

    def perder_vida(self) -> None:
        """Resta una vida cuando la computadora atrapa al jugador"""
        if self._vidas > 0:
            self._vidas -= 1

    def esta_vivo(self) -> bool:
        """Verifica si el jugador aún tiene vidas restantes."""
        return self._vidas > 0
