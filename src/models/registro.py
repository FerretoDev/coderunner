class Registro:
    def __init__(self, nombre_jugador: str, puntaje: int, laberinto: str):
        # Este método se llama cuando se crea un nuevo registro.
        # Guarda el nombre del jugador, el puntaje y el nombre del laberinto.
        self.nombre_jugador = nombre_jugador  # Nombre del jugador.
        self.puntaje = puntaje                # Puntaje que obtuvo el jugador.
        self.laberinto = laberinto            # Nombre o identificador del laberinto.
