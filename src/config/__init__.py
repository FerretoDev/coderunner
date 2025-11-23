"""
Módulo de configuración.

Contiene toda la configuración del juego
(constantes, colores, configuración de laberinto).
"""

from .colores import PaletaColores
from .config import ConfigJuego, Colores
from .config_laberinto import ConfigLaberinto
from .constants import PASSWORD

__all__ = ["ConfigJuego", "Colores", "PaletaColores", "PASSWORD", "ConfigLaberinto"]
