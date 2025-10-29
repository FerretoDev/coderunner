import math
from collections import deque

import pygame

from .personaje import Personaje


class Computadora(Personaje):
    """
    Enemigo que persigue al jugador usando inteligencia artificial.

    Utiliza el algoritmo BFS (Breadth-First Search) para encontrar
    el camino más corto hacia el jugador evitando paredes.
    """

    def __init__(self, x: int, y: int, radio: int = 10, velocidad: float = 0):
        """
        Inicializa el enemigo controlado por IA.

        Args:
            x: Posición inicial en el eje X
            y: Posición inicial en el eje Y
            radio: Tamaño del círculo que representa al enemigo
            velocidad: Velocidad de movimiento (aumenta con la dificultad)
        """
        super().__init__(x, y, radio, velocidad)
        self.color = (255, 50, 50)  # Color rojo para identificar al enemigo

        # Rect de colisión más ajustado al círculo visual
        # Usamos radio*1.8 en vez de radio*2 para mejor precisión en colisiones
        size = int(radio * 1.8)
        offset = (radio * 2 - size) // 2
        self.computadora_principal = pygame.Rect(x + offset, y + offset, size, size)

        # Estado para el algoritmo BFS (Breadth-First Search)
        self._bfs_camino: list[tuple[int, int]] | None = (
            None  # Lista de celdas del camino calculado
        )
        self._bfs_target_cell: tuple[int, int] | None = (
            None  # Celda objetivo actual (donde está el jugador)
        )
        self._bfs_recalc_cooldown = (
            0  # Contador para evitar recalcular el camino cada frame
        )

    def _cell_from_pos(
        self,
        x_px: int,
        y_px: int,
        tam_celda: int,
        offset_x: int = 0,
        offset_y: int = 0,
    ) -> tuple[int, int]:
        """
        Convierte coordenadas de píxeles a coordenadas de celda en el grid.

        Args:
            x_px: Posición X en píxeles en la pantalla
            y_px: Posición Y en píxeles en la pantalla
            tam_celda: Tamaño de cada celda del laberinto
            offset_x: Desplazamiento horizontal del laberinto (para centrado)
            offset_y: Desplazamiento vertical del laberinto (para centrado)

        Returns:
            Tupla (fila, columna) de la celda en el grid del laberinto
        """
        # Restar offsets para obtener coordenadas relativas al laberinto
        x_rel = x_px - offset_x
        y_rel = y_px - offset_y

        # Dividir por tamaño de celda para obtener índice de celda
        col = max(0, x_rel // tam_celda)
        fila = max(0, y_rel // tam_celda)
        return int(fila), int(col)

    def _pos_center_of_cell(
        self, fila: int, col: int, tam_celda: int, offset_x: int = 0, offset_y: int = 0
    ) -> tuple[int, int]:
        """
        Convierte coordenadas de celda a coordenadas de píxeles (centro de la celda).

        Args:
            fila: Índice de fila en el grid
            col: Índice de columna en el grid
            tam_celda: Tamaño de cada celda del laberinto
            offset_x: Desplazamiento horizontal del laberinto
            offset_y: Desplazamiento vertical del laberinto

        Returns:
            Tupla (x, y) con las coordenadas en píxeles del centro de la celda
        """
        # Calcular centro en espacio del laberinto y agregar offsets
        cx = col * tam_celda + tam_celda // 2 + offset_x
        cy = fila * tam_celda + tam_celda // 2 + offset_y
        return cx, cy

    def _calcular_camino_bfs(
        self, mapa: list[list[int]], start: tuple[int, int], goal: tuple[int, int]
    ):
        """
        Calcula el camino más corto usando el algoritmo BFS (Breadth-First Search).

        BFS explora el laberinto capa por capa desde el inicio hasta encontrar el objetivo,
        garantizando que el camino encontrado sea el más corto posible.

        Args:
            mapa: Matriz 2D del laberinto (0=pasillo, 1=pared)
            start: Tupla (fila, col) de la celda inicial (posición del enemigo)
            goal: Tupla (fila, col) de la celda objetivo (posición del jugador)

        Returns:
            Lista de tuplas (fila, col) representando el camino desde start hasta goal,
            o None si no existe un camino válido.
        """
        max_filas = len(mapa)
        max_cols = len(mapa[0]) if max_filas > 0 else 0

        def vecinos(c):
            """Genera las celdas vecinas válidas (arriba, abajo, izquierda, derecha)"""
            f, c0 = c
            # Explorar en 4 direcciones: abajo, arriba, derecha, izquierda
            for df, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nf, nc = f + df, c0 + dc
                # Verificar que esté dentro de los límites y que no sea una pared
                if 0 <= nf < max_filas and 0 <= nc < max_cols and mapa[nf][nc] != 1:
                    yield (nf, nc)

        # Inicializar cola BFS con la celda inicial
        cola = deque([start])
        # Diccionario para rastrear celdas visitadas y reconstruir el camino
        # Clave: celda visitada, Valor: celda previa en el camino
        visitado: dict[tuple[int, int], tuple[int, int] | None] = {start: None}

        # Explorar mientras haya celdas en la cola
        while cola:
            actual = cola.popleft()

            # Si llegamos al objetivo, terminar la búsqueda
            if actual == goal:
                break

            # Explorar todos los vecinos de la celda actual
            for v in vecinos(actual):
                if v not in visitado:
                    visitado[v] = actual  # Guardar de dónde venimos
                    cola.append(v)  # Agregar a la cola para explorar

        # Si el objetivo no fue alcanzado, no hay camino
        if goal not in visitado:
            return None

        # Reconstruir camino del goal al start siguiendo los predecesores
        camino: list[tuple[int, int]] = []
        cur: tuple[int, int] | None = goal
        while cur is not None:
            camino.append(cur)
            cur = visitado[cur]

        # Invertir el camino para que vaya de start a goal
        camino.reverse()
        return camino

    def perseguir_bfs(
        self,
        jugador,
        mapa: list[list[int]],
        tam_celda: int,
        offset_x: int = 0,
        offset_y: int = 0,
        recalc_every: int = 6,
    ):
        """
        Persigue al jugador usando BFS sobre el grid del laberinto.

        Este es el método principal de la IA que:
        1. Obtiene las posiciones actuales del enemigo y jugador en celdas
        2. Calcula o actualiza el camino más corto usando BFS
        3. Mueve al enemigo suavemente hacia la siguiente celda del camino

        Args:
            jugador: Instancia del jugador a perseguir
            mapa: Matriz 2D del laberinto
            tam_celda: Tamaño de cada celda en píxeles
            offset_x: Desplazamiento horizontal del laberinto
            offset_y: Desplazamiento vertical del laberinto
            recalc_every: Cada cuántos frames recalcular el camino (optimización)
        """
        # === PASO 1: Obtener posiciones actuales en el grid ===
        # Celda actual de la computadora (usar centro del hitbox)
        comp_cx, comp_cy = self.computadora_principal.center
        fila_c, col_c = self._cell_from_pos(
            comp_cx, comp_cy, tam_celda, offset_x, offset_y
        )

        # Celda actual del jugador (usar centro del hitbox)
        jug_cx, jug_cy = jugador.jugador_principal.center
        fila_j, col_j = self._cell_from_pos(
            jug_cx, jug_cy, tam_celda, offset_x, offset_y
        )

        objetivo = (fila_j, col_j)

        # === PASO 2: Decidir si recalcular el camino ===
        # Reducir cooldown cada frame
        self._bfs_recalc_cooldown = max(0, self._bfs_recalc_cooldown - 1)

        # Recalcular cuando:
        # - No hay camino calculado aún
        # - El jugador cambió de celda
        # - El cooldown llegó a 0 (cada N frames para adaptarse a cambios)
        if (
            self._bfs_camino is None
            or self._bfs_target_cell != objetivo
            or self._bfs_recalc_cooldown == 0
        ):
            start = (fila_c, col_c)
            path = self._calcular_camino_bfs(mapa, start, objetivo)
            self._bfs_camino = path
            self._bfs_target_cell = objetivo
            self._bfs_recalc_cooldown = recalc_every

        # Si no hay camino válido o ya estamos en el objetivo, no hacer nada
        if not self._bfs_camino or len(self._bfs_camino) <= 1:
            return

        # === PASO 3: Moverse hacia la siguiente celda del camino ===
        # Siguiente celda a la que debemos ir (omitir la celda actual que es [0])
        siguiente_celda = self._bfs_camino[1]
        target_px = self._pos_center_of_cell(
            *siguiente_celda, tam_celda, offset_x, offset_y
        )

        # Calcular vector de movimiento hacia el centro de la siguiente celda
        ax, ay = self.computadora_principal.center
        tx, ty = target_px
        dx, dy = tx - ax, ty - ay
        dist = math.hypot(dx, dy)  # Distancia euclidiana

        if dist > 0:
            # Normalizar el vector de dirección
            ux, uy = dx / dist, dy / dist

            # Calcular el paso a dar (velocidad * dirección)
            paso_x = ux * self.velocidad
            paso_y = uy * self.velocidad
            nuevo_cx = ax + paso_x
            nuevo_cy = ay + paso_y

            # Aplicar movimiento (convertir a enteros para pygame.Rect)
            self.computadora_principal.centerx = int(nuevo_cx)
            self.computadora_principal.centery = int(nuevo_cy)
            self.x = self.computadora_principal.x
            self.y = self.computadora_principal.y

        # === PASO 4: Verificar si llegamos a la celda objetivo ===
        # Si estamos muy cerca del centro de la siguiente celda, avanzar en la ruta
        ax2, ay2 = self.computadora_principal.center
        if math.hypot(tx - ax2, ty - ay2) <= self.velocidad + 0.5:
            # Alinear exactamente al centro de la celda
            self.computadora_principal.centerx = int(tx)
            self.computadora_principal.centery = int(ty)
            self.x = self.computadora_principal.x
            self.y = self.computadora_principal.y

            # Consumir el primer elemento del camino (celda actual) para avanzar a la siguiente
            if self._bfs_camino and len(self._bfs_camino) > 1:
                self._bfs_camino.pop(0)

    def _aplicar_movimiento(self, nueva_x, nueva_y):
        """Aplica el movimiento validando límites"""
        # Validar límites del mapa (asumiendo 20x15 celdas de 32px)
        limite_x = (20 * 32) - self.computadora_principal.width
        limite_y = (15 * 32) - self.computadora_principal.height

        # Mantener dentro de los límites
        nueva_x = max(0, min(nueva_x, limite_x))
        nueva_y = max(0, min(nueva_y, limite_y))

        # Aplicar el movimiento
        self.computadora_principal.x = int(nueva_x)
        self.computadora_principal.y = int(nueva_y)

        # Actualizar coordenadas internas
        self.x = self.computadora_principal.x
        self.y = self.computadora_principal.y

    def _mover_rodeando_obstaculos(self, velocidad_x, velocidad_y):
        """Intenta movimientos alternativos para rodear obstáculos"""
        movimientos_alternativos = [
            # Intentar solo movimiento horizontal
            (velocidad_x, 0),
            # Intentar solo movimiento vertical
            (0, velocidad_y),
            # Intentar movimientos diagonales
            (velocidad_x * 0.7, velocidad_y * 0.7),
            (velocidad_x * 0.7, -velocidad_y * 0.7),
            (-velocidad_x * 0.7, velocidad_y * 0.7),
            # Movimiento perpendicular
            (-velocidad_y, velocidad_x),
            (velocidad_y, -velocidad_x),
        ]

        for vel_x, vel_y in movimientos_alternativos:
            nueva_x = self.computadora_principal.x + vel_x
            nueva_y = self.computadora_principal.y + vel_y

            # Crear rectángulo temporal
            temp_rect = pygame.Rect(
                int(nueva_x),
                int(nueva_y),
                self.computadora_principal.width,
                self.computadora_principal.height,
            )

            # Verificar si este movimiento es válido
            hay_colision = False
            for muro in getattr(self, "_muros_cache", []):
                if temp_rect.colliderect(muro):
                    hay_colision = True
                    break

            if not hay_colision:
                # Movimiento exitoso
                self._aplicar_movimiento(nueva_x, nueva_y)
                return

        # Si ningún movimiento funciona, quedarse quieto
        pass

    def actualizar_muros_cache(self, muros):
        """Actualiza el cache de muros para optimizar colisiones"""
        self._muros_cache = muros

    def colisiona_con_muros(self, muros):
        """Método legacy - ahora la lógica está en perseguir()"""
        # Actualizar cache de muros
        self.actualizar_muros_cache(muros)
        return False  # Ya no necesitamos hacer nada aquí

    def dibujar_computadora_principal(self, screen):
        """
        Dibuja a la computadora con efectos visuales dinámicos.

        Efectos aplicados:
        - Pulsación: El tamaño del enemigo varía ligeramente
        - Color variable: La intensidad del rojo cambia para dar sensación de peligro
        - Detalles visuales: Borde blanco, centro oscuro y "ojos" para hacerlo más visible

        Args:
            screen: Superficie de pygame donde se dibujará el enemigo
        """
        centro = self.computadora_principal.center

        # Mantener contador de frames para animaciones
        frame_count = getattr(self, "_frame_count", 0)
        self._frame_count = frame_count + 1

        # === Efecto 1: Pulsación ===
        # Crear efecto de pulsación usando función seno
        pulso = abs(math.sin(frame_count * 0.2)) * 3  # Varía entre 0 y 3
        radio_pulso = self.radio + pulso

        # === Efecto 2: Color variable ===
        # El rojo del enemigo varía para dar sensación de amenaza
        intensidad = int(200 + 55 * abs(math.sin(frame_count * 0.15)))
        color_principal = (intensidad, 50, 50)

        # === Capa 1: Círculo principal con pulsación ===
        pygame.draw.circle(screen, color_principal, centro, int(radio_pulso))

        # === Capa 2: Borde blanco para mejor visibilidad ===
        pygame.draw.circle(screen, (255, 255, 255), centro, int(radio_pulso), 2)

        # === Capa 3: Centro más oscuro para dar profundidad ===
        pygame.draw.circle(screen, (180, 30, 30), centro, int(self.radio * 0.6))

        # === Capa 4: "Ojos" blancos para dar personalidad ===
        ojo_offset = 4
        pygame.draw.circle(
            screen, (255, 255, 255), (centro[0] - ojo_offset, centro[1] - 2), 2
        )
        pygame.draw.circle(
            screen, (255, 255, 255), (centro[0] + ojo_offset, centro[1] - 2), 2
        )

    def mover(self, direccion: str) -> None:
        """Movimiento simple (no usado en persecución)"""
        paso = int(round(self.velocidad))
        if paso <= 0:
            paso = 1
        if direccion == "arriba":
            self.computadora_principal.y -= paso
        elif direccion == "abajo":
            self.computadora_principal.y += paso
        elif direccion == "izquierda":
            self.computadora_principal.x -= paso
        elif direccion == "derecha":
            self.computadora_principal.x += paso

        self.x = self.computadora_principal.x
        self.y = self.computadora_principal.y
