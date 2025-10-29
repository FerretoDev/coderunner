import json
import os
from re import A

import pygame

from .obsequio import Obsequio

AZUL = (0, 0, 255)


class Laberinto:
    """
    Clase que representa el laberinto del juego.

    Gestiona la estructura del mapa, las colisiones y los obsequios.
    El laberinto se carga desde un archivo JSON que define:
    - Matriz del mapa (0=pasillo, 1=pared)
    - Posiciones iniciales del jugador y enemigo
    - Ubicación y valor de los obsequios

    Componentes:
        Muros: Paredes que no se pueden atravesar (valor 1 en la matriz)
        Pasillos: Espacios transitables (valor 0 en la matriz)
        Obsequios: Items coleccionables que suman puntos
    """

    TAM_CELDA = 32  # Tamaño predeterminado de cada celda en píxeles

    def __init__(self, archivo_json: str):
        """
        Inicializa un nuevo laberinto cargando desde un archivo JSON.

        El archivo JSON debe tener la estructura:
        {
            "nombre": "Nombre del laberinto",
            "dificultad": "normal",
            "mapa": [[0, 1, 0, ...], ...],
            "jugador_inicio": [col, fila],
            "computadora_inicio": [col, fila],
            "obsequios": [{"posicion": [col, fila], "valor": 10}, ...]
        }

        Args:
            archivo_json: Ruta al archivo JSON con el laberinto (relativa a /data)
        """
        # Estructuras de datos principales
        self._muros: list[tuple[int, int]] = []  # Lista de posiciones de muros
        self._pasillos: list[tuple[int, int]] = []  # Lista de posiciones transitables
        self._obsequios: dict[tuple[int, int], Obsequio] = (
            {}
        )  # Diccionario {posición: Obsequio}
        self.laberinto: list[list[int]] = []  # Matriz 2D del mapa (0=pasillo, 1=muro)

        # Metadatos del laberinto
        self.nombre = "Laberinto"
        self.dificultad = "normal"

        # Posiciones iniciales (formato: columna, fila)
        self.jugador_inicio: tuple[int, int] = (1, 1)
        self.computadora_inicio: tuple[int, int] = (18, 12)

        # Cargar todo desde el archivo JSON
        self.cargar_desde_archivo(archivo_json)

    def cargar_desde_archivo(self, archivo: str) -> None:
        """
        Carga el laberinto desde un archivo JSON.

        Proceso:
        1. Resuelve la ruta del archivo (relativa al directorio /data)
        2. Lee y parsea el JSON
        3. Valida la estructura
        4. Carga los datos: nombre, dificultad, mapa, posiciones, obsequios
        5. Procesa el mapa para identificar muros y pasillos

        Args:
            archivo: Ruta al archivo JSON (ej: "laberinto1.json")

        Raises:
            FileNotFoundError: Si el archivo no existe
            ValueError: Si la estructura JSON es inválida
            RuntimeError: Si ocurre un error inesperado
        """
        try:
            # === PASO 1: Resolver ruta del archivo ===
            # Si la ruta es relativa, buscar desde el directorio data
            if not os.path.isabs(archivo):
                # Obtener el directorio del módulo actual (models/)
                dir_actual = os.path.dirname(os.path.abspath(__file__))
                # Subir un nivel (src/) y entrar a data/
                archivo = os.path.join(dir_actual, "..", "data", archivo)

            # === PASO 2: Leer archivo JSON ===
            with open(archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)

            # === PASO 3: Validar estructura ===
            if not self.validar_estructura(datos):
                raise ValueError("Estructura del archivo JSON inválida")

            # === PASO 4: Cargar datos del laberinto ===
            # Metadatos
            self.nombre = datos.get("nombre", "Laberinto")
            self.dificultad = datos.get("dificultad", "normal")

            # Matriz del mapa (lista 2D con 0=pasillo, 1=muro)
            self.laberinto = datos["mapa"]

            # Cargar posiciones iniciales (formato [col, fila] en JSON)
            if "jugador_inicio" in datos:
                col, fila = datos["jugador_inicio"]
                self.jugador_inicio = (col, fila)

            if "computadora_inicio" in datos:
                col, fila = datos["computadora_inicio"]
                self.computadora_inicio = (col, fila)

            # === PASO 5: Procesar el mapa ===
            # Identificar qué celdas son muros y cuáles pasillos
            self._procesar_laberinto()

            # === PASO 6: Cargar obsequios ===
            if "obsequios" in datos:
                for obsequio_data in datos["obsequios"]:
                    col, fila = obsequio_data["posicion"]
                    valor = obsequio_data.get(
                        "valor", 10
                    )  # Valor por defecto: 10 puntos
                    posicion = (col, fila)
                    self._obsequios[posicion] = Obsequio(posicion, valor)

            # Debug (comentado para no saturar la consola)
            # print(f"Laberinto '{self.nombre}' cargado exitosamente")
            # print(f"Dimensiones: {len(self.laberinto[0])}x{len(self.laberinto)}")
            # print(f"Obsequios: {len(self._obsequios)}")

        except FileNotFoundError:
            raise FileNotFoundError(
                f"No se encontró el archivo de laberinto: {archivo}"
            )
        except json.JSONDecodeError:
            raise ValueError(f"El archivo {archivo} no es un JSON válido")
        except Exception as e:
            raise RuntimeError(f"Error inesperado al cargar laberinto: {e}")

    def _procesar_laberinto(self):
        """
        Procesa el mapa para clasificar cada celda como muro o pasillo.

        Itera sobre toda la matriz del laberinto y genera dos listas:
        - _muros: Posiciones con valor 1 (no transitables)
        - _pasillos: Posiciones con valor 0 (transitables)

        Estas listas se usan para validación rápida de movimiento.
        """
        self._muros = []
        self._pasillos = []

        for fila in range(len(self.laberinto)):
            for col in range(len(self.laberinto[0])):
                posicion = (col, fila)
                if self.laberinto[fila][col] == 1:
                    self._muros.append(posicion)  # Es una pared
                else:
                    self._pasillos.append(posicion)  # Es un pasillo

    def validar_estructura(self, datos: dict) -> bool:
        """
        Valida que el laberinto tenga una estructura correcta.

        Verifica:
        1. Que exista la clave "mapa"
        2. Que el mapa sea una lista no vacía
        3. Que todas las filas tengan el mismo ancho (matriz rectangular)

        Args:
            datos: Diccionario con los datos parseados del JSON

        Returns:
            bool: True si la estructura es válida, False en caso contrario
        """
        # Verificar que exista el mapa
        if "mapa" not in datos:
            return False

        mapa = datos["mapa"]

        # Verificar que sea una lista válida
        if not isinstance(mapa, list) or len(mapa) == 0:
            return False

        # Verificar que todas las filas tengan el mismo tamaño (matriz rectangular)
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

        Este método es llamado por pantalla_juego.py cuando detecta que
        el jugador está en la misma celda que un obsequio.

        Args:
            posicion: Coordenadas (col, fila) del obsequio

        Returns:
            int: Puntos obtenidos (valor del obsequio), 0 si no había obsequio
        """
        if posicion in self._obsequios:
            obsequio = self._obsequios.pop(posicion)  # Eliminar del diccionario
            return obsequio.valor
        return 0  # No había obsequio en esa posición

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

        Cada obsequio se renderiza como un círculo dorado con:
        - Efecto de pulsación (tamaño variable con seno)
        - Múltiples capas de color (exterior, principal, centro, punto de luz)
        - Brillo para hacerlo más visible y atractivo

        Args:
            pantalla: Superficie de pygame donde se dibujarán los obsequios
            frame_count: Contador de frames para animación (opcional, default=0)
            tam_celda: Tamaño de celda en píxeles (si None, usa self.TAM_CELDA)
            offset_x: Desplazamiento horizontal para centrado del laberinto
            offset_y: Desplazamiento vertical para centrado del laberinto
        """
        import math

        # Usar tam_celda pasado o el predeterminado
        celda_size = tam_celda if tam_celda is not None else self.TAM_CELDA

        # Dibujar cada obsequio con animación
        for posicion, obsequio in self._obsequios.items():
            col, fila = posicion

            # Calcular posición en píxeles (centro de la celda)
            x = col * celda_size + celda_size // 2 + offset_x
            y = fila * celda_size + celda_size // 2 + offset_y

            # === Efecto de pulsación ===
            # Usar seno para crear variación suave del tamaño
            pulso = abs(math.sin(frame_count * 0.1)) * 2  # Varía entre 0 y 2
            radio_base = 8
            radio_pulso = radio_base + pulso

            # === Capas de dibujo (de exterior a interior) ===
            # Capa 1: Círculo exterior con brillo (amarillo claro)
            pygame.draw.circle(pantalla, (255, 240, 100), (x, y), int(radio_pulso + 2))

            # Capa 2: Círculo principal dorado
            pygame.draw.circle(pantalla, (255, 215, 0), (x, y), int(radio_pulso))

            # Capa 3: Centro brillante (amarillo muy claro)
            pygame.draw.circle(
                pantalla, (255, 255, 200), (x, y), int(radio_pulso * 0.5)
            )

            # Capa 4: Punto de luz superior izquierdo (destello)
            pygame.draw.circle(pantalla, (255, 255, 255), (x - 2, y - 2), 2)
            pygame.draw.circle(pantalla, (255, 255, 255), (x - 2, y - 2), 2)
