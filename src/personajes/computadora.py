import math
from collections import deque

import pygame

from config.config import ConfigJuego
from utilidades.coordenadas import ConversorCoordenadas

from .personaje import Personaje


class Computadora(Personaje):
    """Enemigo que persigue al jugador usando algoritmo BFS"""

    def __init__(self, x: int, y: int, radio: int = 10, velocidad: float = 0):
        super().__init__(x, y, radio, velocidad)
        self.color = (255, 50, 50)

        # Posiciones de spawn para respawn
        self.spawn_x = x
        self.spawn_y = y

        # Cargar imagen de la computadora (minotauro)
        self.imagen = pygame.image.load(
            "src/assets/imagenes/minotauro.png"
        ).convert_alpha()
        self.imagen = pygame.transform.scale(self.imagen, (44, 44))

        # Contador de frames para animación de esfera pulsante
        self._frame_count = 0

        # Crear rect de colisión usando factor de configuración
        size = int(radio * ConfigJuego.FACTOR_RECT_COLISION)
        offset = (radio * 2 - size) // 2  # Centrar rect en círculo
        self._rect = pygame.Rect(x + offset, y + offset, size, size)

        # Variables para optimizar BFS (evitar recalcular cada frame)
        self._bfs_camino: list[tuple[int, int]] | None = None  # Ruta actual
        self._bfs_target_cell: tuple[int, int] | None = None  # Celda objetivo previa
        self._bfs_recalc_cooldown = 0  # Contador para recalcular camino

    @property
    def computadora_principal(self) -> pygame.Rect:
        """Rect de colisión de la computadora (propiedad de solo lectura)."""
        return self._rect

    def _calcular_camino_bfs(
        self, mapa: list[list[int]], start: tuple[int, int], goal: tuple[int, int]
    ):
        """Calcula el camino más corto usando búsqueda de Amplitud (BFS)"""
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
        comp_cx, comp_cy = self._rect.center
        fila_c, col_c = ConversorCoordenadas.pixel_a_celda(
            comp_cx, comp_cy, tam_celda, offset_x, offset_y
        )

        jug_cx, jug_cy = jugador.jugador_principal.center
        fila_j, col_j = ConversorCoordenadas.pixel_a_celda(
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
        target_px = ConversorCoordenadas.celda_a_pixel_centro(
            *siguiente_celda, tam_celda, offset_x, offset_y
        )

        # Calcular vector de movimiento hacia el objetivo
        ax, ay = self._rect.center
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
            self._rect.centerx = int(nuevo_cx)
            self._rect.centery = int(nuevo_cy)
            self.x = self._rect.x
            self.y = self._rect.y

        # Si llegamos al centro de la celda objetivo, avanzar al siguiente paso
        ax2, ay2 = self._rect.center
        if math.hypot(tx - ax2, ty - ay2) <= self.velocidad + 0.5:
            # Alinear exactamente al centro
            self._rect.centerx = int(tx)
            self._rect.centery = int(ty)
            self.x = self._rect.x
            self.y = self._rect.y

            # Consumir celda actual del camino
            if self._bfs_camino and len(self._bfs_camino) > 1:
                self._bfs_camino.pop(0)

    def _aplicar_movimiento(self, nueva_x, nueva_y):
        """Aplica movimiento respetando límites del laberinto"""
        # Límites basados en laberinto de 20x15 celdas de 32px
        limite_x = (20 * 32) - self._rect.width
        limite_y = (15 * 32) - self._rect.height

        # Clamp a los límites
        nueva_x = max(0, min(nueva_x, limite_x))
        nueva_y = max(0, min(nueva_y, limite_y))

        # Actualizar rect de colisión
        self._rect.x = int(nueva_x)
        self._rect.y = int(nueva_y)

        # Sincronizar con coordenadas del personaje
        self.x = self._rect.x
        self.y = self._rect.y

    def _mover_rodeando_obstaculos(self, velocidad_x, velocidad_y):
        """Prueba movimientos alternativos si hay colisión (método legacy)"""
        # Lista de vectores de movimiento alternativos a probar
        movimientos_alternativos = [
            (velocidad_x, 0),  # Solo horizontal
            (0, velocidad_y),  # Solo vertical
            (
                velocidad_x * ConfigJuego.FACTOR_DIAGONAL,
                velocidad_y * ConfigJuego.FACTOR_DIAGONAL,
            ),  # Diagonal principal
            (
                velocidad_x * ConfigJuego.FACTOR_DIAGONAL,
                -velocidad_y * ConfigJuego.FACTOR_DIAGONAL,
            ),  # Diagonal inversa
            (
                -velocidad_x * ConfigJuego.FACTOR_DIAGONAL,
                velocidad_y * ConfigJuego.FACTOR_DIAGONAL,
            ),  # Diagonal inversa 2
            (-velocidad_y, velocidad_x),  # Perpendicular 1
            (velocidad_y, -velocidad_x),  # Perpendicular 2
        ]

        # Probar cada movimiento alternativo
        for vel_x, vel_y in movimientos_alternativos:
            nueva_x = self._rect.x + vel_x
            nueva_y = self._rect.y + vel_y

            # Crear rect temporal para verificar colisión
            temp_rect = pygame.Rect(
                int(nueva_x),
                int(nueva_y),
                self._rect.width,
                self._rect.height,
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
        """
        Dibuja a la computadora en la pantalla con su imagen.
        Si no se carga correctamente, dibuja un círculo rojo como respaldo.
        """
        try:
            # Obtener la posición donde se dibujará (centrando la imagen)
            centro = self._rect.center
            rect_imagen = self.imagen.get_rect(center=centro)
            screen.blit(self.imagen, rect_imagen)
        except AttributeError:
            # En caso de error o si no hay imagen, dibujar círculo con efecto pulsante
            centro = self._rect.center

            # Contador de frames para animación
            self._frame_count += 1

            # Efecto pulsante usando seno (oscila entre -1 y 1)
            pulso = abs(math.sin(self._frame_count * 0.2)) * 3
            radio_pulso = self.radio + pulso

            # Variar intensidad del color rojo
            intensidad = int(200 + 55 * abs(math.sin(self._frame_count * 0.15)))
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
        """
        Movimiento manual por dirección (no usado - la computadora usa perseguir_bfs).
        Implementado para cumplir con el contrato de la clase abstracta Personaje.
        """
        # La computadora no usa movimiento manual, se mueve con perseguir_bfs
        pass

    def respawn(self):
        """Reposiciona a la computadora en su punto de spawn inicial."""
        self._rect.x = self.spawn_x
        self._rect.y = self.spawn_y
        self._bfs_camino = None  # Limpiar camino para recalcular
        self._bfs_target_cell = None

    def verificar_captura(self, jugador, margen_captura: int = 0) -> bool:
        """
        Verifica si la computadora ha capturado al jugador.

        Args:
            jugador: Instancia del jugador
            margen_captura: Margen adicional para la captura (por defecto 0)

        Returns:
            True si capturó al jugador, False en caso contrario
        """
        dx = jugador.jugador_principal.centerx - self._rect.centerx
        dy = jugador.jugador_principal.centery - self._rect.centery
        distancia = math.sqrt(dx**2 + dy**2)

        return distancia < (jugador.radio + self.radio + margen_captura)
