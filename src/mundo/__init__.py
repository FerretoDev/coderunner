"""
Módulo del mundo del juego.

Contiene los modelos de datos que representan el mundo del juego
(laberinto, obsequios, salón de la fama, registros).
"""

from .laberinto import Laberinto
from .obsequio import Obsequio
from .registro import Registro
from .salon_fama import SalonFama

__all__ = ["Laberinto", "Obsequio", "Registro", "SalonFama"]
