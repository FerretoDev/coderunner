import json
import os
from datetime import datetime
from typing import List

from .registro import Registro


class SalonFama:
    """
    Gestor del Salón de la Fama que mantiene los mejores puntajes.

    Almacena registros de partidas con nombre, puntaje, laberinto y fecha.
    Permite guardar, cargar, mostrar y reiniciar el ranking.
    """

    def __init__(self, archivo: str = "src/data/salon_fama.json"):
        """
        Inicializa el salón de la fama.

        Args:
            archivo: Ruta al archivo JSON donde se guardan los registros
        """
        self._archivo = archivo
        self._registros: list[Registro] = []
        self.cargar_datos()  # Cargar datos al inicializar

    def guardar_puntaje(self, registro: Registro):
        """
        Añade un nuevo registro de puntaje al salón.

        Args:
            registro: Objeto Registro con los datos de la partida
        """
        self._registros.append(registro)
        self.guardar_datos()  # Persistir inmediatamente

    def mostrar_mejores(self, limite: int = 10) -> list[dict]:
        """
        Devuelve los mejores puntajes en orden descendente.

        Args:
            limite: Cantidad máxima de registros a retornar (default: 10)

        Returns:
            Lista de diccionarios con los datos de cada registro
        """
        # Ordenar por puntaje descendente
        registros_ordenados = sorted(
            self._registros, key=lambda r: r.puntaje, reverse=True
        )

        # Convertir a diccionarios para fácil uso en UI
        resultado = []
        for registro in registros_ordenados[:limite]:
            resultado.append(
                {
                    "nombre_jugador": registro.nombre_jugador,
                    "puntaje": registro.puntaje,
                    "laberinto": registro.laberinto,
                    "fecha": registro.fecha if hasattr(registro, "fecha") else "N/A",
                }
            )

        return resultado

    def cargar_datos(self):
        """
        Carga los registros desde el archivo JSON al iniciar el programa.

        Si el archivo no existe, inicializa con lista vacía.
        """
        # Si el archivo no existe, no hay nada que cargar
        if not os.path.exists(self._archivo):
            self._registros = []
            return

        try:
            with open(self._archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)

                # Verificar estructura del JSON
                if "registros" not in datos:
                    print(
                        f"Advertencia: Archivo {self._archivo} con formato incorrecto"
                    )
                    self._registros = []
                    return

                # Convertir cada item en un objeto Registro
                self._registros = []
                for item in datos["registros"]:
                    registro = Registro(
                        nombre_jugador=item.get("nombre_jugador", "Anónimo"),
                        puntaje=item.get("puntaje", 0),
                        laberinto=item.get("laberinto", "desconocido"),
                        fecha=item.get("fecha"),  # Opcional, puede ser None
                    )
                    self._registros.append(registro)

                # Para debugging
                # print(
                #    f"Cargados {len(self._registros)} registros del salón de la fama"
                # )

        except json.JSONDecodeError:
            print(f"Error: No se pudo leer {self._archivo}, archivo JSON corrupto")
            self._registros = []
        except Exception as e:
            print(f"Error al cargar salón de la fama: {e}")
            self._registros = []

    def guardar_datos(self):
        """
        Escribe los registros al archivo JSON al actualizar.

        Guarda automáticamente después de añadir un nuevo puntaje.
        """
        try:
            # Crear directorio si no existe
            directorio = os.path.dirname(self._archivo)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio)

            # Convertir registros a diccionarios
            datos = {
                "registros": [
                    {
                        "nombre_jugador": r.nombre_jugador,
                        "puntaje": r.puntaje,
                        "laberinto": r.laberinto,
                        "fecha": r.fecha if hasattr(r, "fecha") else None,
                    }
                    for r in self._registros
                ]
            }

            # Escribir al archivo con formato legible
            with open(self._archivo, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)

            print(f"✓ Salón de la fama guardado ({len(self._registros)} registros)")

        except Exception as e:
            print(f"Error al guardar salón de la fama: {e}")

    def reiniciar(self):
        """
        Borra todos los registros del salón de la fama.

        Útil para limpiar datos de prueba o resetear el ranking.
        """
        self._registros = []
        self.guardar_datos()
        print("✓ Salón de la fama reiniciado")

    def obtener_estadisticas(self) -> dict:
        """
        Calcula estadísticas generales del salón de la fama.

        Returns:
            Diccionario con total de partidas, mejor puntaje, promedio, etc.
        """
        if not self._registros:
            return {
                "total_partidas": 0,
                "mejor_puntaje": 0,
                "promedio": 0,
                "jugador_top": "N/A",
            }

        puntajes = [r.puntaje for r in self._registros]
        mejor_registro = max(self._registros, key=lambda r: r.puntaje)

        return {
            "total_partidas": len(self._registros),
            "mejor_puntaje": max(puntajes),
            "promedio": sum(puntajes) / len(puntajes),
            "jugador_top": mejor_registro.nombre_jugador,
        }

    def obtener_ranking_por_jugador(self, nombre_jugador: str):
        """
        Obtiene todas las partidas de un jugador específico.

        Args:
            nombre_jugador: Nombre del jugador a buscar

        Returns:
            Lista de registros del jugador ordenados por puntaje
        """
        registros_jugador = [
            r
            for r in self._registros
            if r.nombre_jugador.lower() == nombre_jugador.lower()
        ]

        return sorted(registros_jugador, key=lambda r: r.puntaje, reverse=True)
