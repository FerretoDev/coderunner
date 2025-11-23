"""
Gestor de movimiento y colisiones para el jugador.

Maneja:
- Movimiento por celdas con cooldown
- Detección de colisiones con muros
- Validación de límites del laberinto
- Sistema de historial para revertir movimientos inválidos
"""

import pygame


class GestorMovimiento:
    """
    Gestiona el movimiento del jugador y las colisiones.

    Responsabilidades:
    - Procesar entrada del teclado
    - Mover jugador por celdas con cooldown
    - Detectar colisiones con muros
    - Validar límites del laberinto
    - Modo pixel a pixel (legacy)
    """

    def __init__(
        self,
        jugador,
        muros: list[pygame.Rect],
        tam_celda: int,
        offset_x: int,
        offset_y: int,
        mapa: list[list[int]],
        frames_cooldown: int = 8,
        movimiento_por_celdas: bool = True,
    ):
        """
        Inicializa el gestor de movimiento.

        Args:
            jugador: Instancia del jugador a mover
            muros: Lista de Rects de muros para colisiones
            tam_celda: Tamaño de cada celda en píxeles
            offset_x: Offset horizontal del laberinto
            offset_y: Offset vertical del laberinto
            mapa: Matriz del laberinto (para calcular límites)
            frames_cooldown: Frames de espera entre movimientos
            movimiento_por_celdas: True para movimiento discreto, False para continuo
        """
        self.jugador = jugador
        self.muros = muros
        self.tam_celda = tam_celda
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.mapa = mapa
        self.frames_cooldown = frames_cooldown
        self.movimiento_por_celdas = movimiento_por_celdas

        # Sistema de cooldown
        self.cooldown_actual = 0
        self.ultima_tecla = None

        # Historial de posiciones para revertir
        self.pos_anterior_x = jugador.jugador_principal.x
        self.pos_anterior_y = jugador.jugador_principal.y

    def guardar_posicion_anterior(self):
        """Guarda la posición actual para poder revertirla si hay colisión."""
        self.pos_anterior_x = self.jugador.jugador_principal.x
        self.pos_anterior_y = self.jugador.jugador_principal.y

    def revertir_posicion(self):
        """Revierte el jugador a la última posición válida."""
        self.jugador.jugador_principal.x = self.pos_anterior_x
        self.jugador.jugador_principal.y = self.pos_anterior_y

    def detectar_colision(self) -> bool:
        """
        Verifica si el jugador está colisionando con algún muro.

        Returns:
            True si NO hay colisión, False si está chocando
        """
        for muro in self.muros:
            if self.jugador.jugador_principal.colliderect(muro):
                return False
        return True

    def procesar_entrada_teclado(self):
        """
        Procesa las teclas presionadas y mueve al jugador.

        Maneja cooldown para evitar movimientos múltiples en un frame.
        """
        if self.cooldown_actual > 0:
            self.cooldown_actual -= 1
            return

        keys = pygame.key.get_pressed()

        # Determinar dirección presionada (prioridad: arriba, abajo, izquierda, derecha)
        tecla_actual = None
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            tecla_actual = "up"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            tecla_actual = "down"
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            tecla_actual = "left"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            tecla_actual = "right"

        if tecla_actual:
            if self.movimiento_por_celdas:
                self._mover_por_celdas(tecla_actual)
            else:
                self._mover_continuo(tecla_actual)
            self.cooldown_actual = self.frames_cooldown

        self.ultima_tecla = tecla_actual

    def _mover_por_celdas(self, direccion: str):
        """
        Mueve al jugador exactamente una celda en la dirección especificada.

        Valida que:
        - No se salga de los límites del laberinto
        - No colisione con muros

        Args:
            direccion: "up", "down", "left" o "right"
        """
        rect = self.jugador.jugador_principal
        nueva_x = rect.x
        nueva_y = rect.y

        # Calcular desplazamiento para el sprite
        dx = 0
        dy = 0

        # Calcular nueva posición según dirección
        if direccion == "up":
            nueva_y = rect.y - self.tam_celda
            dy = -self.tam_celda
            limite_min = self.offset_y
            if nueva_y < limite_min:
                return
        elif direccion == "down":
            nueva_y = rect.y + self.tam_celda
            dy = self.tam_celda
            limite_max = self.offset_y + (len(self.mapa) * self.tam_celda)
            if nueva_y + rect.height > limite_max:
                return
        elif direccion == "left":
            nueva_x = rect.x - self.tam_celda
            dx = -self.tam_celda
            limite_min = self.offset_x
            if nueva_x < limite_min:
                return
        elif direccion == "right":
            nueva_x = rect.x + self.tam_celda
            dx = self.tam_celda
            limite_max = self.offset_x + (len(self.mapa[0]) * self.tam_celda)
            if nueva_x + rect.width > limite_max:
                return

        # Validar colisión con muros
        temp_rect = pygame.Rect(nueva_x, nueva_y, rect.width, rect.height)
        if not any(temp_rect.colliderect(m) for m in self.muros):
            rect.x = nueva_x
            rect.y = nueva_y

            # Actualizar estado de movimiento del sprite del jugador
            self.jugador.actualizar_movimiento(dx, dy)

    def _mover_continuo(self, direccion: str):
        """
        Mueve al jugador píxel a píxel (modo legacy).

        Args:
            direccion: "up", "down", "left" o "right"
        """
        self.guardar_posicion_anterior()
        rect = self.jugador.jugador_principal
        velocidad = self.jugador.velocidad

        # Calcular desplazamiento para el sprite
        dx = 0
        dy = 0

        # Aplicar movimiento
        if direccion == "up":
            rect.y -= velocidad
            dy = -velocidad
        elif direccion == "down":
            rect.y += velocidad
            dy = velocidad
        elif direccion == "left":
            rect.x -= velocidad
            dx = -velocidad
        elif direccion == "right":
            rect.x += velocidad
            dx = velocidad

        # Aplicar límites del laberinto
        limite_x_min = self.offset_x
        limite_x_max = self.offset_x + (len(self.mapa[0]) * self.tam_celda) - rect.width
        limite_y_min = self.offset_y
        limite_y_max = self.offset_y + (len(self.mapa) * self.tam_celda) - rect.height

        rect.x = max(limite_x_min, min(rect.x, limite_x_max))
        rect.y = max(limite_y_min, min(rect.y, limite_y_max))

        # Revertir si hay colisión
        if not self.detectar_colision():
            self.revertir_posicion()
        else:
            # Actualizar estado de movimiento del sprite del jugador
            self.jugador.actualizar_movimiento(dx, dy)

    def actualizar_muros(self, nuevos_muros: list[pygame.Rect]):
        """Actualiza la lista de muros (útil si el laberinto cambia)."""
        self.muros = nuevos_muros
