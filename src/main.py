import os
import sys

# Agregar el directorio src al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game.juego import Juego


def main():
    juego = Juego()
    juego.iniciar("Jugador1")


if __name__ == "__main__":
    main()
