from datetime import datetime


class Registro:
    """
    Representa un registro individual en el Salón de la Fama.

    Almacena información de una partida: jugador, puntaje, laberinto y fecha.
    """

    def __init__(
        self,
        nombre_jugador: str,
        puntaje: int,
        laberinto: str,
        fecha: str | None = None,
    ):
        """
        Crea un nuevo registro de partida.

        Args:
            nombre_jugador: Nombre del jugador
            puntaje: Puntos obtenidos en la partida
            laberinto: Nombre o ID del laberinto jugado
            fecha: Fecha en formato ISO (si es None, usa fecha actual)
        """
        self.nombre_jugador = nombre_jugador
        self.puntaje = puntaje
        self.laberinto = laberinto

        # Si no se proporciona fecha, usar la actual
        if fecha is None:
            self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.fecha = fecha

    def __repr__(self) -> str:
        """Representación legible del registro"""
        return (
            f"Registro({self.nombre_jugador}: {self.puntaje} pts en {self.laberinto})"
        )

    def __str__(self) -> str:
        """String formateado del registro"""
        return f"{self.nombre_jugador} - {self.puntaje} puntos - {self.laberinto} - {self.fecha}"
