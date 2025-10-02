from personaje import Personaje

class Jugador(Personaje):
    """Clase que representa al jugador en el juego."""
    def __init__(self,posicion, nombre: str, vidas: int = 3, puntaje: int = 0):
        super().__init__(posicion)
        self._nombre = nombre
        self._vidas = vidas
        self._puntaje = puntaje

    def mover(self, nueva_posicion):
        return super().mover(nueva_posicion)
    
    def sumar_puntos(self, puntos: int)-> None:
        self._puntaje += puntos
    
    def perder_vida(self) -> None:
        self._vidas -= 1

    def estar_vivo(self)->bool:
        return True if self._vidas > 0 else False

    