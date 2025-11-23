"""
Módulo de configuración.

Contiene toda la configuración del juego
(constantes, colores, configuración de laberinto).
"""

from .config import ConfigJuego, Colores
from .constants import PASSWORD
from .config_laberinto import ConfigLaberinto

__all__ = ["ConfigJuego", "Colores", "PASSWORD", "ConfigLaberinto"]
