import json
import os
import shutil
from datetime import datetime

from utils import guardar_json, resolver_ruta_laberinto

from .config_laberinto import ConfigLaberinto
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

    def cargar_laberinto(
        self, ruta_archivo: str, copiar_externo: bool = True
    ) -> tuple[Laberinto | None, str]:
        """
        Carga un laberinto desde un archivo .json y valida su estructura.
        Si el archivo está fuera de src/data/laberintos/, lo copia automáticamente.

        Args:
            ruta_archivo: Ruta completa al archivo del laberinto
            copiar_externo: Si True, copia archivos externos a src/data/laberintos/

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

            # Verificar si el archivo está fuera de src/data/laberintos/
            ruta_normalizada = os.path.normpath(os.path.abspath(ruta_archivo))
            directorio_laberintos = os.path.normpath(
                os.path.abspath("src/data/laberintos")
            )

            mensaje_copia = ""
            ruta_final = ruta_archivo

            if copiar_externo and not ruta_normalizada.startswith(
                directorio_laberintos
            ):
                # El archivo está fuera, copiarlo
                ruta_final_temp = self._copiar_laberinto_externo(ruta_archivo, datos)
                if ruta_final_temp:
                    ruta_final = ruta_final_temp
                    mensaje_copia = f"\n(Copiado a: {os.path.basename(ruta_final)})"
                else:
                    # Si falla la copia, usar el archivo original
                    mensaje_copia = "\n(No se pudo copiar, usando archivo original)"

            # Guardar la ruta del laberinto cargado para uso posterior
            ConfigLaberinto.guardar_laberinto_activo(ruta_final)

            # Crear el laberinto solo si pygame está disponible e inicializado
            try:
                import pygame

                if pygame.get_init():
                    laberinto = Laberinto(
                        ruta_final if ruta_final.endswith(".json") else datos
                    )
                    return (
                        laberinto,
                        f"Laberinto '{laberinto.nombre}' cargado exitosamente{mensaje_copia}",
                    )
                else:
                    # pygame no está inicializado, solo guardar configuración
                    nombre = datos.get("nombre", "Laberinto")
                    return (
                        None,
                        f"Laberinto '{nombre}' configurado exitosamente{mensaje_copia}\n(Se cargará al iniciar el juego)",
                    )
            except:
                # pygame no disponible, solo guardar la configuración
                nombre = datos.get("nombre", "Laberinto")
                return (
                    None,
                    f"Laberinto '{nombre}' configurado exitosamente{mensaje_copia}\n(Se cargará al iniciar el juego)",
                )

        except json.JSONDecodeError:
            return None, "El archivo no contiene JSON válido"
        except Exception as e:
            return None, f"Error al cargar laberinto: {str(e)}"

    def _copiar_laberinto_externo(self, ruta_origen: str, datos: dict) -> str | None:
        """
        Copia un archivo de laberinto externo a src/data/laberintos/.

        Args:
            ruta_origen: Ruta del archivo original
            datos: Datos del laberinto para generar nombre único

        Returns:
            Ruta del archivo copiado o None si falla
        """
        try:
            # Crear directorio si no existe
            directorio_destino = "src/data/laberintos"
            os.makedirs(directorio_destino, exist_ok=True)

            # Generar nombre único para evitar sobrescribir
            nombre_base = os.path.splitext(os.path.basename(ruta_origen))[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_destino = f"{nombre_base}_{timestamp}.json"

            # Si el archivo ya tiene un nombre descriptivo, usarlo
            if "nombre" in datos and datos["nombre"]:
                nombre_laberinto = datos["nombre"].replace(" ", "_").lower()
                nombre_destino = f"{nombre_laberinto}_{timestamp}.json"

            ruta_destino = os.path.join(directorio_destino, nombre_destino)

            # Copiar el archivo
            shutil.copy2(ruta_origen, ruta_destino)

            return ruta_destino

        except Exception as e:
            print(f"Error al copiar laberinto: {e}")
            return None

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
