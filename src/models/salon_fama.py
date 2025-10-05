import json
import os
from typing import List

from .registro import Registro


class SalonFama:
    def __init__(self, archivo: str = "src/data/salon_fama.json"):
        self._archivo = archivo
        self._registros: list[Registro] = []

    def guardar_puntaje(self, registro: Registro):
        """Añade el puntaje del jugador actual"""
        ...

    def mostrar_mejores(self) -> list:
        """Devuelve los puntajes en orden descendente"""
        ...

    def cargar_datos(self):
        """Carga los registros desde archivo al iniciar el programa"""
        ...

    def guardar_datos(self):
        """Escribe los registros al archivo al actualizar"""
        ...

    def reiniciar(self):
        """Borra todo el salón de la fama"""
        ...
