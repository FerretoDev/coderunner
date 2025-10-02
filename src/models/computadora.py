from personaje import Personaje
from jugador import Jugador
from laberinto import Leberinto
class Computadora(Personaje):

    def __init__(self, posicion, velocidad):
        super().__init__(posicion, velocidad)


    def perseguir(self, jugador: Jugador, laberinto: Leberinto)->None:
        ...

    def mover(self, nueva_posicion)-> None:
        "TODO"

        #return super().mover(nueva_posicion)

    