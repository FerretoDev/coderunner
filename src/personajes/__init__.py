"""
Módulo de personajes del juego.

Contiene las clases que representan a los personajes jugables
y no jugables del videojuego (Jugador, Computadora).
"""

from .personaje import Personaje
from .jugador import Jugador
from .computadora import Computadora

__all__ = ["Personaje", "Jugador", "Computadora"]
