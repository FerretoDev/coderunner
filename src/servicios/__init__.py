"""
Módulo de servicios del juego.

Contiene servicios globales y utilidades del sistema
(administrador, sistema de sonido).
"""

from .administrador import Administrador
from .sistema_sonido import SistemaSonido

__all__ = ["Administrador", "SistemaSonido"]
