import math
from collections import deque

import pygame

from .personaje import Personaje


class Computadora(Personaje):
    """Enemigo que persigue al jugador usando algoritmo BFS"""

    def __init__(self, x: int, y: int, radio: int = 10, velocidad: float = 0):
        super().__init__(x, y, radio, velocidad)
        self.color = (255, 50, 50)

        # Crear rect de colisión 10% más pequeño que el círculo para precisión
        size = int(radio * 1.8)
        offset = (radio * 2 - size) // 2  # Centrar rect en círculo
        self.computadora_principal = pygame.Rect(x + offset, y + offset, size, size)

        # Variables para optimizar BFS (evitar recalcular cada frame)
        self._bfs_camino: list[tuple[int, int]] | None = None  # Ruta actual
        self._bfs_target_cell: tuple[int, int] | None = None  # Celda objetivo previa
        self._bfs_recalc_cooldown = 0  # Contador para recalcular camino

    def _cell_from_pos(
        self, x_px: int, y_px: int, tam_celda: int, offset_x: int = 0, offset_y: int = 0
    ) -> tuple[int, int]:
        """Convierte coordenadas de píxeles a índices de celda (fila, col)"""
        x_rel = x_px - offset_x  # Ajustar por offset de centrado
        y_rel = y_px - offset_y
        col = max(0, x_rel // tam_celda)
        fila = max(0, y_rel // tam_celda)
        return int(fila), int(col)

    def _pos_center_of_cell(
        self, fila: int, col: int, tam_celda: int, offset_x: int = 0, offset_y: int = 0
    ) -> tuple[int, int]:
        """Convierte índices de celda (fila, col) a píxeles del centro"""
        cx = col * tam_celda + tam_celda // 2 + offset_x
        cy = fila * tam_celda + tam_celda // 2 + offset_y
        return cx, cy

    def _calcular_camino_bfs(
        self, mapa: list[list[int]], start: tuple[int, int], goal: tuple[int, int]
    ):
        """Calcula el camino más corto usando Breadth-First Search (BFS)"""
        max_filas = len(mapa)
        max_cols = len(mapa[0]) if max_filas > 0 else 0

        def vecinos(c):
            """Retorna celdas adyacentes válidas (no muros, dentro de límites)"""
            f, c0 = c
            # Explorar las 4 direcciones: abajo, arriba, derecha, izquierda
            for df, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nf, nc = f + df, c0 + dc
                # Validar que esté en el mapa y no sea muro (1 = muro, 0 = pasillo)
                if 0 <= nf < max_filas and 0 <= nc < max_cols and mapa[nf][nc] != 1:
                    yield (nf, nc)

        # Inicializar BFS con cola FIFO
        cola = deque([start])
        visitado: dict[tuple[int, int], tuple[int, int] | None] = {start: None}

        # Explorar nivel por nivel hasta encontrar el objetivo
        while cola:
            actual = cola.popleft()
            if actual == goal:
                break  # Camino encontrado
            for v in vecinos(actual):
                if v not in visitado:
                    visitado[v] = actual  # Guardar de dónde venimos
                    cola.append(v)

        # Si no se alcanzó el objetivo, no hay camino
        if goal not in visitado:
            return None

        # Reconstruir camino siguiendo los predecesores desde goal hasta start
        camino: list[tuple[int, int]] = []
        cur: tuple[int, int] | None = goal
        while cur is not None:
            camino.append(cur)
            cur = visitado[cur]
        camino.reverse()  # Invertir para tener start -> goal
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
        Persigue al jugador usando BFS para encontrar el camino óptimo.

        Optimizaciones:
        - Recalcula camino solo si el jugador cambia de celda
        - O cada 'recalc_every' frames para adaptarse a movimientos
        - Movimiento suave interpolando entre centros de celdas
        """
        # Obtener posiciones actuales en el grid
        comp_cx, comp_cy = self.computadora_principal.center
        fila_c, col_c = self._cell_from_pos(
            comp_cx, comp_cy, tam_celda, offset_x, offset_y
        )

        jug_cx, jug_cy = jugador.jugador_principal.center
        fila_j, col_j = self._cell_from_pos(
            jug_cx, jug_cy, tam_celda, offset_x, offset_y
        )

        objetivo = (fila_j, col_j)

        # Decrementar cooldown de recálculo
        self._bfs_recalc_cooldown = max(0, self._bfs_recalc_cooldown - 1)

        # Recalcular camino si es necesario
        necesita_recalculo = (
            self._bfs_camino is None  # Primera vez
            or self._bfs_target_cell != objetivo  # Jugador cambió de celda
            or self._bfs_recalc_cooldown == 0  # Timeout de recálculo
        )

        if necesita_recalculo:
            start = (fila_c, col_c)
            path = self._calcular_camino_bfs(mapa, start, objetivo)
            self._bfs_camino = path
            self._bfs_target_cell = objetivo
            self._bfs_recalc_cooldown = recalc_every

        # Si no hay camino o ya llegamos, no hacer nada
        if not self._bfs_camino or len(self._bfs_camino) <= 1:
            return

        # Obtener siguiente celda en el camino (índice 1, ya que 0 es la actual)
        siguiente_celda = self._bfs_camino[1]
        target_px = self._pos_center_of_cell(
            *siguiente_celda, tam_celda, offset_x, offset_y
        )

        # Calcular vector de movimiento hacia el objetivo
        ax, ay = self.computadora_principal.center
        tx, ty = target_px
        dx, dy = tx - ax, ty - ay
        dist = math.hypot(dx, dy)

        if dist > 0:
            # Normalizar y aplicar velocidad
            ux, uy = dx / dist, dy / dist
            paso_x = ux * self.velocidad
            paso_y = uy * self.velocidad
            nuevo_cx = ax + paso_x
            nuevo_cy = ay + paso_y

            # Actualizar posición del rect (convertir a int para Pygame)
            self.computadora_principal.centerx = int(nuevo_cx)
            self.computadora_principal.centery = int(nuevo_cy)
            self.x = self.computadora_principal.x
            self.y = self.computadora_principal.y

        # Si llegamos al centro de la celda objetivo, avanzar al siguiente paso
        ax2, ay2 = self.computadora_principal.center
        if math.hypot(tx - ax2, ty - ay2) <= self.velocidad + 0.5:
            # Alinear exactamente al centro
            self.computadora_principal.centerx = int(tx)
            self.computadora_principal.centery = int(ty)
            self.x = self.computadora_principal.x
            self.y = self.computadora_principal.y

            # Consumir celda actual del camino
            if self._bfs_camino and len(self._bfs_camino) > 1:
                self._bfs_camino.pop(0)

    def _aplicar_movimiento(self, nueva_x, nueva_y):
        """Aplica movimiento respetando límites del laberinto"""
        # Límites basados en laberinto de 20x15 celdas de 32px
        limite_x = (20 * 32) - self.computadora_principal.width
        limite_y = (15 * 32) - self.computadora_principal.height

        # Clamp a los límites
        nueva_x = max(0, min(nueva_x, limite_x))
        nueva_y = max(0, min(nueva_y, limite_y))

        # Actualizar rect de colisión
        self.computadora_principal.x = int(nueva_x)
        self.computadora_principal.y = int(nueva_y)

        # Sincronizar con coordenadas del personaje
        self.x = self.computadora_principal.x
        self.y = self.computadora_principal.y

    def _mover_rodeando_obstaculos(self, velocidad_x, velocidad_y):
        """Prueba movimientos alternativos si hay colisión (método legacy)"""
        # Lista de vectores de movimiento alternativos a probar
        movimientos_alternativos = [
            (velocidad_x, 0),  # Solo horizontal
            (0, velocidad_y),  # Solo vertical
            (velocidad_x * 0.7, velocidad_y * 0.7),  # Diagonal principal
            (velocidad_x * 0.7, -velocidad_y * 0.7),  # Diagonal inversa
            (-velocidad_x * 0.7, velocidad_y * 0.7),  # Diagonal inversa 2
            (-velocidad_y, velocidad_x),  # Perpendicular 1
            (velocidad_y, -velocidad_x),  # Perpendicular 2
        ]

        # Probar cada movimiento alternativo
        for vel_x, vel_y in movimientos_alternativos:
            nueva_x = self.computadora_principal.x + vel_x
            nueva_y = self.computadora_principal.y + vel_y

            # Crear rect temporal para verificar colisión
            temp_rect = pygame.Rect(
                int(nueva_x),
                int(nueva_y),
                self.computadora_principal.width,
                self.computadora_principal.height,
            )

            # Verificar colisión con muros
            hay_colision = False
            for muro in getattr(self, "_muros_cache", []):
                if temp_rect.colliderect(muro):
                    hay_colision = True
                    break

            # Si no hay colisión, aplicar este movimiento
            if not hay_colision:
                self._aplicar_movimiento(nueva_x, nueva_y)
                return

        # Si ningún movimiento funciona, quedarse en posición actual

    def actualizar_muros_cache(self, muros):
        """Guarda referencia a muros para optimizar verificación de colisiones"""
        self._muros_cache = muros

    def colisiona_con_muros(self, muros):
        """Método legacy - colisiones ahora manejadas por BFS"""
        self.actualizar_muros_cache(muros)
        return False

    def dibujar_computadora_principal(self, screen):
        """Dibuja enemigo con efecto visual pulsante"""
        centro = self.computadora_principal.center

        # Contador de frames para animación
        frame_count = getattr(self, "_frame_count", 0)
        self._frame_count = frame_count + 1

        # Efecto pulsante usando seno (oscila entre -1 y 1)
        pulso = abs(math.sin(frame_count * 0.2)) * 3
        radio_pulso = self.radio + pulso

        # Variar intensidad del color rojo
        intensidad = int(200 + 55 * abs(math.sin(frame_count * 0.15)))
        color_principal = (intensidad, 50, 50)

        # Círculo principal con pulsación
        pygame.draw.circle(screen, color_principal, centro, int(radio_pulso))

        # Borde blanco para contraste
        pygame.draw.circle(screen, (255, 255, 255), centro, int(radio_pulso), 2)

        # Centro oscuro para dar profundidad
        pygame.draw.circle(screen, (180, 30, 30), centro, int(self.radio * 0.6))

        # Puntos brillantes simulando "ojos"
        ojo_offset = 4
        pygame.draw.circle(
            screen, (255, 255, 255), (centro[0] - ojo_offset, centro[1] - 2), 2
        )
        pygame.draw.circle(
            screen, (255, 255, 255), (centro[0] + ojo_offset, centro[1] - 2), 2
        )

    def mover(self, direccion: str) -> None:
        """Movimiento manual por dirección (no usado durante persecución)"""
        paso = int(round(self.velocidad))
        if paso <= 0:
            paso = 1

        # Aplicar movimiento según dirección
        if direccion == "arriba":
            self.computadora_principal.y -= paso
        elif direccion == "abajo":
            self.computadora_principal.y += paso
        elif direccion == "izquierda":
            self.computadora_principal.x -= paso
        elif direccion == "derecha":
            self.computadora_principal.x += paso

        # Sincronizar coordenadas
        self.x = self.computadora_principal.x
        self.y = self.computadora_principal.y
