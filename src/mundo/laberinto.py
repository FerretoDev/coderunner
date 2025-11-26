import json
import os

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

    def __init__(self, archivo_json_o_datos: str | dict):
        """
        Inicializa un nuevo laberinto cargando desde un archivo JSON o directamente desde un diccionario de datos.

        El archivo JSON o el diccionario debe tener la estructura:
        {
            "nombre": "Nombre del laberinto",
            "dificultad": "normal",
            "mapa": [[0, 1, 0, ...], ...],
            "jugador_inicio": [col, fila],
            "computadora_inicio": [col, fila],
            "obsequios": [{"posicion": [col, fila], "valor": 10}, ...]
        }

        Args:
            archivo_json_o_datos: Ruta al archivo JSON con el laberinto (relativa a /data)
                                  o un diccionario con los datos del laberinto.
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

        # Crear superficie de color para pasillos
        self.imagen_pasillo = pygame.Surface((self.TAM_CELDA, self.TAM_CELDA))
        self.imagen_pasillo.fill((50, 50, 50))

        if isinstance(archivo_json_o_datos, dict):
            self._cargar_desde_diccionario(archivo_json_o_datos)
        elif isinstance(archivo_json_o_datos, str):
            self._cargar_desde_archivo_path(archivo_json_o_datos)
        else:
            raise TypeError(
                "El argumento para Laberinto debe ser una ruta de archivo (str) o un diccionario de datos."
            )

    def _cargar_desde_archivo_path(self, archivo: str) -> None:
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
                # Si la ruta ya comienza con 'src/data/', usarla desde la raíz del proyecto
                if archivo.startswith("src/data/"):
                    # Obtener directorio raíz del proyecto (dos niveles arriba desde models/)
                    dir_actual = os.path.dirname(os.path.abspath(__file__))
                    proyecto_root = os.path.join(dir_actual, "..", "..")
                    archivo = os.path.join(proyecto_root, archivo)
                else:
                    # Obtener el directorio del módulo actual (models/)
                    dir_actual = os.path.dirname(os.path.abspath(__file__))
                    # Subir un nivel (src/) y entrar a data/
                    archivo = os.path.join(dir_actual, "..", "data", archivo)

            # === PASO 2: Leer archivo JSON ===
            with open(archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)

            self._procesar_datos_laberinto(datos)

        except FileNotFoundError as exc:
            raise FileNotFoundError(
                f"No se encontró el archivo de laberinto: {archivo}"
            ) from exc
        except json.JSONDecodeError as exc:
            raise ValueError(f"El archivo {archivo} no es un JSON válido") from exc
        except Exception as e:
            raise RuntimeError(f"Error inesperado al cargar laberinto: {e}") from e

    def _cargar_desde_diccionario(self, datos: dict) -> None:
        """
        Carga el laberinto directamente desde un diccionario de datos.

        Args:
            datos: Diccionario con los datos del laberinto.

        Raises:
            ValueError: Si la estructura del diccionario es inválida.
            RuntimeError: Si ocurre un error inesperado.
        """
        try:
            self._procesar_datos_laberinto(datos)
        except Exception as e:
            raise RuntimeError(
                f"Error inesperado al cargar laberinto desde diccionario: {e}"
            ) from e

    def _procesar_datos_laberinto(self, datos: dict) -> None:
        """
        Procesa los datos del laberinto (común a cargar desde archivo o diccionario).

        Args:
            datos: Diccionario con los datos parseados del JSON o directamente proporcionados.

        Raises:
            ValueError: Si la estructura JSON es inválida.
        """
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
        if "inicio_jugador" in datos:
            col, fila = datos["inicio_jugador"].values()
            self.jugador_inicio = (col, fila)

        if "inicio_computadora" in datos:
            col, fila = datos["inicio_computadora"].values()
            self.computadora_inicio = (col, fila)

        # === PASO 5: Procesar el mapa ===
        # Identificar qué celdas son muros y cuáles pasillos
        self._procesar_laberinto()

        # === PASO 6: Cargar obsequios ===
        if "obsequios" in datos:
            for obsequio_data in datos["obsequios"]:
                col, fila = obsequio_data["posicion"]
                valor = obsequio_data.get("valor", 10)  # Valor por defecto: 10 puntos
                posicion = (col, fila)
                self._obsequios[posicion] = Obsequio(posicion, valor)

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
                else:
                    # Dibuja pasillo con imagen
                    pantalla.blit(self.imagen_pasillo, (x, y))

    def dibujar_obsequios(
        self, pantalla, frame_count=0, tam_celda=None, offset_x=0, offset_y=0
    ):
        """
        Dibuja los obsequios en el laberinto.

        Cada obsequio se renderiza como el Hilo de Ariadna (ovillo dorado):
        - Ovillo de hilo enrollado
        - Pulsación de brillo dorado
        - Efecto de resplandor mítico
        - Tema mitológico griego

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
            cx = col * celda_size + celda_size // 2 + offset_x
            cy = fila * celda_size + celda_size // 2 + offset_y

            # === Efecto de pulsación del resplandor ===
            pulso_brillo = abs(math.sin(frame_count * 0.08)) * 0.3 + 0.7
            pulso_tamano = abs(math.sin(frame_count * 0.06)) * 2

            radio_base = 9
            radio_ovillo = radio_base + pulso_tamano

            # === Aura dorada exterior (resplandor mítico) ===
            for r in range(5, 0, -1):
                intensidad = int(255 * pulso_brillo * (r / 5.0))
                color_aura = (intensidad, int(intensidad * 0.84), 0)  # Dorado
                pygame.draw.circle(
                    pantalla, color_aura, (cx, cy), int(radio_ovillo + r * 3), 1
                )

            # === Ovillo base (círculo dorado) ===
            color_oro = (218, 165, 32)  # Oro antiguo
            pygame.draw.circle(pantalla, color_oro, (cx, cy), int(radio_ovillo))

            # === Líneas de hilo enrollado (textura del ovillo) ===
            num_lineas = 8
            for i in range(num_lineas):
                angulo = (frame_count * 0.03 + i * (2 * math.pi / num_lineas)) % (
                    2 * math.pi
                )

                # Líneas curvas simulando hilo enrollado
                inicio_x = cx + (radio_ovillo - 3) * math.cos(angulo)
                inicio_y = cy + (radio_ovillo - 3) * math.sin(angulo)
                fin_x = cx + (radio_ovillo - 7) * math.cos(angulo + 0.5)
                fin_y = cy + (radio_ovillo - 7) * math.sin(angulo + 0.5)

                pygame.draw.line(
                    pantalla,
                    (184, 134, 11),  # Oro más oscuro para textura
                    (int(inicio_x), int(inicio_y)),
                    (int(fin_x), int(fin_y)),
                    2,
                )

            # === Borde brillante del ovillo ===
            color_brillo = (
                int(255 * pulso_brillo),
                int(215 * pulso_brillo),
                int(100 * pulso_brillo),
            )
            pygame.draw.circle(pantalla, color_brillo, (cx, cy), int(radio_ovillo), 2)

            # === Destello central (núcleo del hilo) ===
            pygame.draw.circle(pantalla, (255, 235, 150), (cx - 2, cy - 2), 3)
            pygame.draw.circle(pantalla, (255, 255, 200), (cx - 2, cy - 2), 1)

    def generar_muros_rect(
        self, tam_celda: int, offset_x: int, offset_y: int
    ) -> list[pygame.Rect]:
        """
        Genera una lista de Rects para todos los muros del laberinto.

        Args:
            tam_celda: Tamaño de cada celda en píxeles
            offset_x: Desplazamiento horizontal para centrado
            offset_y: Desplazamiento vertical para centrado

        Returns:
            Lista de pygame.Rect, uno por cada muro
        """
        muros = []
        for fila in range(len(self.laberinto)):
            for col in range(len(self.laberinto[0])):
                if self.laberinto[fila][col] == 1:  # 1 = muro
                    x = col * tam_celda + offset_x
                    y = fila * tam_celda + offset_y
                    rect = pygame.Rect(x, y, tam_celda, tam_celda)
                    muros.append(rect)
        return muros

    def calcular_posicion_spawn(
        self,
        posicion_celda: tuple[int, int],
        radio: int,
        tam_celda: int,
        offset_x: int,
        offset_y: int,
    ) -> tuple[int, int]:
        """
        Calcula la posición en píxeles para un personaje basado en su celda inicial.

        Centra el personaje dentro de la celda considerando su radio.

        Args:
            posicion_celda: (col, fila) en el mapa
            radio: Radio del personaje en píxeles
            tam_celda: Tamaño de cada celda en píxeles
            offset_x: Desplazamiento horizontal del laberinto
            offset_y: Desplazamiento vertical del laberinto

        Returns:
            (x, y) posición en píxeles para el personaje
        """
        col, fila = posicion_celda
        x = col * tam_celda + (tam_celda - radio * 2) // 2 + offset_x
        y = fila * tam_celda + (tam_celda - radio * 2) // 2 + offset_y
        return (x, y)
