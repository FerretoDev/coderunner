import json
import os

import pygame

from .obsequio import Obsequio

AZUL = (0, 0, 255)  # Color de los muros del laberinto


class Laberinto:
    """
    Clase que representa el laberinto del juego.

    El laberinto está compuesto por:
        Muros: Paredes que el jugador no puede atravesar
        Pasillos: Espacios por donde el jugador puede moverse
        Obsequios: Items que el jugador puede recolectar
    """

    TAM_CELDA = 32

    def __init__(self, archivo_json: str):
        """
        Inicializa un nuevo laberinto cargando desde un archivo JSON.

        Parámetros:
            archivo_json: Ruta al archivo JSON con el laberinto (obligatorio)
        """
        self._muros: list[tuple[int, int]] = []
        self._pasillos: list[tuple[int, int]] = []
        self._obsequios: dict[tuple[int, int], Obsequio] = {}
        self.laberinto: list[list[int]] = []
        self.nombre = "Laberinto"
        self.dificultad = "normal"
        self.jugador_inicio: tuple[int, int] = (1, 1)
        self.computadora_inicio: tuple[int, int] = (18, 12)

        self.cargar_desde_archivo(archivo_json)

    def cargar_desde_archivo(self, archivo: str) -> None:
        """
        Carga el laberinto desde un archivo JSON.

        Parámetros:
            archivo: Ruta al archivo JSON con la estructura del laberinto
        """
        try:
            # Si la ruta es relativa, buscar desde el directorio data
            if not os.path.isabs(archivo):
                # Obtener el directorio del módulo actual
                dir_actual = os.path.dirname(os.path.abspath(__file__))
                # Subir un nivel y entrar a data
                archivo = os.path.join(dir_actual, "..", "data", archivo)

            with open(archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)

            if not self.validar_estructura(datos):
                raise ValueError("Estructura del archivo JSON inválida")

            # Cargar datos del laberinto
            self.nombre = datos.get("nombre", "Laberinto")
            self.dificultad = datos.get("dificultad", "normal")
            self.laberinto = datos["mapa"]

            # Cargar posiciones iniciales (formato [col, fila] en JSON)
            if "jugador_inicio" in datos:
                col, fila = datos["jugador_inicio"]
                self.jugador_inicio = (col, fila)

            if "computadora_inicio" in datos:
                col, fila = datos["computadora_inicio"]
                self.computadora_inicio = (col, fila)

            # Procesar el mapa para identificar muros y pasillos
            self._procesar_laberinto()

            # Cargar obsequios
            if "obsequios" in datos:
                for obsequio_data in datos["obsequios"]:
                    col, fila = obsequio_data["posicion"]
                    valor = obsequio_data.get("valor", 10)
                    posicion = (col, fila)
                    self._obsequios[posicion] = Obsequio(posicion, valor)

            print(f"Laberinto '{self.nombre}' cargado exitosamente")
            print(f"Dimensiones: {len(self.laberinto[0])}x{len(self.laberinto)}")
            print(f"Obsequios: {len(self._obsequios)}")

        except FileNotFoundError:
            raise FileNotFoundError(
                f"No se encontró el archivo de laberinto: {archivo}"
            )
        except json.JSONDecodeError:
            raise ValueError(f"El archivo {archivo} no es un JSON válido")
        except Exception as e:
            raise RuntimeError(f"Error inesperado al cargar laberinto: {e}")

    def _procesar_laberinto(self):
        """Procesa el mapa para identificar muros y pasillos"""
        self._muros = []
        self._pasillos = []

        for fila in range(len(self.laberinto)):
            for col in range(len(self.laberinto[0])):
                posicion = (col, fila)
                if self.laberinto[fila][col] == 1:
                    self._muros.append(posicion)
                else:
                    self._pasillos.append(posicion)

    def validar_estructura(self, datos: dict) -> bool:
        """
        Valida que el laberinto tenga una estructura correcta.

        Parámetros:
            datos: Diccionario con los datos del JSON

        Retorna:
            bool: True si la estructura es válida
        """
        if "mapa" not in datos:
            return False

        mapa = datos["mapa"]
        if not isinstance(mapa, list) or len(mapa) == 0:
            return False

        # Verificar que todas las filas tengan el mismo tamaño
        ancho = len(mapa[0])
        for fila in mapa:
            if not isinstance(fila, list) or len(fila) != ancho:
                return False

        return True

    def es_paso_valido(self, posicion: tuple[int, int]) -> bool:
        """
        Verifica si una posición es válida para el movimiento del jugador.

        Parámetros:
            posicion: Coordenadas (x, y) a verificar
        Retorna:
            bool: True si es un pasillo u obsequio, False si es un muro
        """
        return posicion in self._pasillos or posicion in self._obsequios

    def obtener_obsequio(self, posicion: tuple[int, int]) -> Obsequio | None:
        """
        Verifica si hay un obsequio en la posición dada y lo retorna.

        Parámetros:
            posicion: Coordenadas (col, fila) a verificar

        Retorna:
            Obsequio si existe en esa posición, None si no hay
        """
        return self._obsequios.get(posicion)

    def recolectar_obsequio(self, posicion: tuple[int, int]) -> int:
        """
        Recolecta un obsequio en la posición dada y lo elimina del mapa.

        Parámetros:
            posicion: Coordenadas (col, fila) del obsequio

        Retorna:
            int: Puntos obtenidos, 0 si no había obsequio
        """
        if posicion in self._obsequios:
            obsequio = self._obsequios.pop(posicion)
            return obsequio.valor
        return 0

    def obtener_rectangulos(self):
        """
        Genera los rectángulos de colisión para los muros del laberinto.

        Retorna:
            list: Lista de objetos Rect de pygame que representan los muros
        """
        rectangulos = []
        for fila in range(len(self.laberinto)):
            for col in range(len(self.laberinto[0])):
                if self.laberinto[fila][col] == 1:  # 1 representa un muro
                    x = col * self.TAM_CELDA
                    y = fila * self.TAM_CELDA
                    rect = pygame.Rect(x, y, self.TAM_CELDA, self.TAM_CELDA)
                    rectangulos.append(rect)
        return rectangulos

    def dibujar_laberinto(self, pantalla):
        """
        Dibuja el laberinto en la pantalla.

        Los muros se dibujan como rectángulos azules.

        Parámetros:
            pantalla: Superficie de pygame donde se dibujará el laberinto
        """
        for fila in range(len(self.laberinto)):
            for col in range(len(self.laberinto[0])):
                if self.laberinto[fila][col] == 1:
                    x = col * self.TAM_CELDA
                    y = fila * self.TAM_CELDA
                    pygame.draw.rect(
                        pantalla, AZUL, (x, y, self.TAM_CELDA, self.TAM_CELDA)
                    )

    def dibujar_obsequios(
        self, pantalla, frame_count=0, tam_celda=None, offset_x=0, offset_y=0
    ):
        """
        Dibuja los obsequios en el laberinto con efecto de brillo pulsante.

        Parámetros:
            pantalla: Superficie de pygame donde se dibujarán los obsequios
            frame_count: Contador de frames para animación (opcional)
            tam_celda: Tamaño de celda (si no se pasa, usa self.TAM_CELDA)
            offset_x: Desplazamiento horizontal para centrado
            offset_y: Desplazamiento vertical para centrado
        """
        import math

        # Usar tam_celda pasado o el predeterminado
        celda_size = tam_celda if tam_celda is not None else self.TAM_CELDA

        for posicion, obsequio in self._obsequios.items():
            col, fila = posicion
            x = col * celda_size + celda_size // 2 + offset_x
            y = fila * celda_size + celda_size // 2 + offset_y

            # Efecto pulsante
            pulso = abs(math.sin(frame_count * 0.1)) * 2
            radio_base = 8
            radio_pulso = radio_base + pulso

            # Círculo exterior con brillo
            pygame.draw.circle(pantalla, (255, 240, 100), (x, y), int(radio_pulso + 2))
            # Círculo principal dorado
            pygame.draw.circle(pantalla, (255, 215, 0), (x, y), int(radio_pulso))
            # Centro brillante
            pygame.draw.circle(
                pantalla, (255, 255, 200), (x, y), int(radio_pulso * 0.5)
            )
            # Punto de luz
            pygame.draw.circle(pantalla, (255, 255, 255), (x - 2, y - 2), 2)
