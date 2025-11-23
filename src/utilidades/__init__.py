"""
Módulo de utilidades.

Funciones y clases auxiliares reutilizables en todo el proyecto
(conversión de coordenadas, helpers generales).
"""

from .coordenadas import ConversorCoordenadas
from .helpers import resolver_ruta_laberinto

__all__ = ["ConversorCoordenadas", "resolver_ruta_laberinto"]
