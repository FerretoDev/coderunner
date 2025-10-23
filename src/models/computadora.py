import math
from collections import deque

import pygame

from .personaje import Personaje


class Computadora(Personaje):
    """Enemiga que persigue al jugador con IA mejorada"""

    def __init__(self, x: int, y: int, radio: int = 10, velocidad: float = 2.5):
        super().__init__(x, y, radio, velocidad)
        self.color = (255, 50, 50)
        # Rect de colisión más ajustado al círculo visual
        # Usamos radio*1.8 en vez de radio*2 para mejor precisión
        size = int(radio * 1.8)
        offset = (radio * 2 - size) // 2
        self.computadora_principal = pygame.Rect(x + offset, y + offset, size, size)
        # Estado para BFS
        self._bfs_camino: list[tuple[int, int]] | None = None
        self._bfs_target_cell: tuple[int, int] | None = None
        self._bfs_recalc_cooldown = 0

    def _cell_from_pos(self, x_px: int, y_px: int, tam_celda: int) -> tuple[int, int]:
        col = max(0, x_px // tam_celda)
        fila = max(0, y_px // tam_celda)
        return int(fila), int(col)

    def _pos_center_of_cell(
        self, fila: int, col: int, tam_celda: int
    ) -> tuple[int, int]:
        cx = col * tam_celda + tam_celda // 2
        cy = fila * tam_celda + tam_celda // 2
        return cx, cy

    def _calcular_camino_bfs(
        self, mapa: list[list[int]], start: tuple[int, int], goal: tuple[int, int]
    ):
        max_filas = len(mapa)
        max_cols = len(mapa[0]) if max_filas > 0 else 0

        def vecinos(c):
            f, c0 = c
            for df, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nf, nc = f + df, c0 + dc
                if 0 <= nf < max_filas and 0 <= nc < max_cols and mapa[nf][nc] != 1:
                    yield (nf, nc)

        cola = deque([start])
        visitado: dict[tuple[int, int], tuple[int, int] | None] = {start: None}

        while cola:
            actual = cola.popleft()
            if actual == goal:
                break
            for v in vecinos(actual):
                if v not in visitado:
                    visitado[v] = actual
                    cola.append(v)

        if goal not in visitado:
            return None

        # Reconstruir camino del goal al start
        camino: list[tuple[int, int]] = []
        cur: tuple[int, int] | None = goal
        while cur is not None:
            camino.append(cur)
            cur = visitado[cur]
        camino.reverse()
        return camino

    def perseguir_bfs(
        self, jugador, mapa: list[list[int]], tam_celda: int, recalc_every: int = 6
    ):
        """Persigue al jugador usando BFS sobre el grid del laberinto.
        - Recalcula camino si el objetivo cambia de celda o cada `recalc_every` frames.
        - Se mueve suavemente hacia el centro de la siguiente celda.
        """
        # Celda actual de la compu y del jugador (usar centro)
        comp_cx, comp_cy = self.computadora_principal.center
        fila_c, col_c = self._cell_from_pos(comp_cx, comp_cy, tam_celda)
        jug_cx, jug_cy = jugador.jugador_principal.center
        fila_j, col_j = self._cell_from_pos(jug_cx, jug_cy, tam_celda)

        objetivo = (fila_j, col_j)

        # Recalcular cuando sea necesario
        self._bfs_recalc_cooldown = max(0, self._bfs_recalc_cooldown - 1)
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

        if not self._bfs_camino or len(self._bfs_camino) <= 1:
            return  # ya estamos en la celda objetivo o no hay camino

        # Siguiente celda a la que debemos ir (omitir la celda actual que es [0])
        siguiente_celda = self._bfs_camino[1]
        target_px = self._pos_center_of_cell(*siguiente_celda, tam_celda)

        # Mover suavemente hacia el centro de la siguiente celda
        ax, ay = self.computadora_principal.center
        tx, ty = target_px
        dx, dy = tx - ax, ty - ay
        dist = math.hypot(dx, dy)
        if dist > 0:
            ux, uy = dx / dist, dy / dist
            paso_x = ux * self.velocidad
            paso_y = uy * self.velocidad
            nuevo_cx = ax + paso_x
            nuevo_cy = ay + paso_y

            # Aplicar en top-left con casteo a int (Rect usa enteros)
            self.computadora_principal.centerx = int(nuevo_cx)
            self.computadora_principal.centery = int(nuevo_cy)
            self.x = self.computadora_principal.x
            self.y = self.computadora_principal.y

        # Si estamos muy cerca del centro de la siguiente celda, avanzar en la ruta
        ax2, ay2 = self.computadora_principal.center
        if math.hypot(tx - ax2, ty - ay2) <= self.velocidad + 0.5:
            # Alinear exacto al centro de la celda y avanzar
            self.computadora_principal.centerx = int(tx)
            self.computadora_principal.centery = int(ty)
            self.x = self.computadora_principal.x
            self.y = self.computadora_principal.y
            # Consumir el primer paso (la celda actual) para ir a la siguiente
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
        """Dibuja a la computadora con efecto de peligro dinámico"""
        centro = self.computadora_principal.center

        # Efecto pulsante basado en frame count
        frame_count = getattr(self, "_frame_count", 0)
        self._frame_count = frame_count + 1

        # Crear efecto de pulsación
        pulso = abs(math.sin(frame_count * 0.2)) * 3
        radio_pulso = self.radio + pulso

        # Color que varía con la pulsación
        intensidad = int(200 + 55 * abs(math.sin(frame_count * 0.15)))
        color_principal = (intensidad, 50, 50)

        # Dibujar círculo principal con pulsación
        pygame.draw.circle(screen, color_principal, centro, int(radio_pulso))

        # Borde blanco
        pygame.draw.circle(screen, (255, 255, 255), centro, int(radio_pulso), 2)

        # Centro más oscuro para definir mejor la forma
        pygame.draw.circle(screen, (180, 30, 30), centro, int(self.radio * 0.6))

        # Pequeños "ojos" o puntos brillantes para hacerla más visible
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
