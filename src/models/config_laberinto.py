"""
Configuración y gestión de laberintos.

Maneja la configuración del laberinto activo y funciones relacionadas.
"""

import json
import os
from datetime import datetime


class ConfigLaberinto:
    """Gestiona la configuración del laberinto activo."""

    RUTA_CONFIG = "src/data/config_laberinto.json"

    @staticmethod
    def obtener_laberinto_activo() -> str | None:
        """
        Obtiene la ruta del laberinto activo desde la configuración.

        Returns:
            Ruta del laberinto activo o None si no hay ninguno configurado
        """
        try:
            if os.path.exists(ConfigLaberinto.RUTA_CONFIG):
                with open(ConfigLaberinto.RUTA_CONFIG, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    ruta = config.get("laberinto_activo")
                    # Verificar que el archivo todavía existe
                    if ruta and os.path.exists(ruta):
                        return ruta
            return None
        except Exception as e:
            print(f"Error al leer configuración de laberinto: {e}")
            return None

    @staticmethod
    def guardar_laberinto_activo(ruta: str) -> bool:
        """
        Guarda la ruta del laberinto activo en el archivo de configuración.

        Args:
            ruta: Ruta del archivo de laberinto a guardar como activo

        Returns:
            True si se guardó correctamente, False si hubo error
        """
        try:
            config = {
                "laberinto_activo": ruta,
                "fecha_carga": datetime.now().isoformat(),
            }

            # Crear directorio si no existe
            directorio = os.path.dirname(ConfigLaberinto.RUTA_CONFIG)
            if directorio:
                os.makedirs(directorio, exist_ok=True)

            with open(ConfigLaberinto.RUTA_CONFIG, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True

        except Exception as e:
            print(f"Error al guardar configuración de laberinto: {e}")
            return False
