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
        self._registros.append(registro)

    def mostrar_mejores(self) -> list:
        """Devuelve los puntajes en orden descendente"""
        return sorted(self._registros, key=lambda r: r.puntaje, reverse=True)

    def cargar_datos(self):
        """Carga los registros desde archivo al iniciar el programa"""
        if not os.path.exists(self._archivo):
            return

        with open(self._archivo, "r") as f:
            datos = json.load(f)
            for item in datos:
                registro = Registro(
                    nombre_jugador=item["nombre_jugador"],
                    puntaje=item["puntaje"],
                    laberinto=item["laberinto"],
                )
                self._registros.append(registro)

    def guardar_datos(self):
        """Escribe los registros al archivo al actualizar"""
        ...

    def reiniciar(self):
        """Borra todo el salón de la fama"""
        ...
