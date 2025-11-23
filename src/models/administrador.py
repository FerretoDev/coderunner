import json
import os
from .laberinto import Laberinto
from .salon_fama import SalonFama


class Administrador:
    """
    Clase que representa al administrador del juego.
    Gestiona las funciones administrativas como carga de laberintos
    y reinicio del salón de la fama.
    """

    def __init__(self, clave: str):
        self._clave = clave

    def autenticar(self, clave: str) -> bool:
        """Autentica al administrador con la clave proporcionada."""
        return self._clave == clave

    def cargar_laberinto(self, ruta_archivo: str) -> tuple[Laberinto | None, str]:
        """
        Carga un laberinto desde un archivo .json o .txt y valida su estructura.

        Args:
            ruta_archivo: Ruta completa al archivo del laberinto

        Returns:
            Tupla (laberinto, mensaje):
            - laberinto: Objeto Laberinto si la carga fue exitosa, None si falló
            - mensaje: Descripción del resultado (éxito o error)
        """
        try:
            # Validar que el archivo existe
            if not os.path.exists(ruta_archivo):
                return None, f"El archivo no existe: {ruta_archivo}"

            # Validar extensión del archivo
            extension = os.path.splitext(ruta_archivo)[1].lower()
            if extension != ".json":
                return None, "Solo se permiten archivos .json"

            # Leer el archivo JSON
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)

            # Validar estructura básica del laberinto
            errores = self._validar_estructura_laberinto(datos)
            if errores:
                return None, f"Estructura inválida:\n" + "\n".join(errores)

            # Crear el laberinto
            laberinto = Laberinto(datos)

            return laberinto, f"Laberinto '{laberinto.nombre}' cargado exitosamente"

        except json.JSONDecodeError:
            return None, "El archivo no contiene JSON válido"
        except Exception as e:
            return None, f"Error al cargar laberinto: {str(e)}"

    def _validar_estructura_laberinto(self, datos: dict) -> list[str]:
        """
        Valida la estructura del archivo de laberinto.

        Args:
            datos: Diccionario con los datos del laberinto

        Returns:
            Lista de errores encontrados (vacía si es válido)
        """
        errores = []

        # Validar que exista el mapa
        if "mapa" not in datos:
            errores.append("- Falta la clave 'mapa'")
        elif not isinstance(datos["mapa"], list) or len(datos["mapa"]) == 0:
            errores.append("- El 'mapa' debe ser una lista no vacía")

        # Validar posición inicial del jugador
        if "inicio_jugador" not in datos:
            errores.append("- Falta la posición inicial del jugador ('inicio_jugador')")
        elif not self._validar_posicion(datos["inicio_jugador"]):
            errores.append("- La posición 'inicio_jugador' tiene formato inválido")

        # Validar posición inicial de la computadora
        if "inicio_computadora" not in datos:
            errores.append(
                "- Falta la posición inicial de la computadora ('inicio_computadora')"
            )
        elif not self._validar_posicion(datos["inicio_computadora"]):
            errores.append("- La posición 'inicio_computadora' tiene formato inválido")

        return errores

    def _validar_posicion(self, posicion) -> bool:
        """
        Valida que una posición tenga el formato correcto.

        Args:
            posicion: Objeto a validar

        Returns:
            True si es válida, False en caso contrario
        """
        if isinstance(posicion, dict):
            return "col" in posicion and "fila" in posicion
        elif isinstance(posicion, list):
            return len(posicion) == 2 and all(isinstance(x, int) for x in posicion)
        return False

    def reiniciar_salon_fama(self, salon: SalonFama) -> str:
        """
        Reinicia el salón de la fama eliminando todos los registros.

        Args:
            salon: Instancia del SalonFama a reiniciar

        Returns:
            Mensaje de confirmación
        """
        salon.reiniciar()
        return "Salón de la fama reiniciado exitosamente"
