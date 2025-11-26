import math

import pygame

from config.config import ConfigJuego

from .personaje import Personaje


class Jugador(Personaje):
    """
    Clase que representa al jugador controlado por el usuario.

    Esta clase maneja:
        El movimiento del jugador usando las teclas de dirección
        El sistema de vidas (3 vidas iniciales)
        El sistema de puntaje
        La representación visual con efecto de esfera pulsante
    """

    def __init__(self, x, y, radio):
        """
        Comienza un nuevo jugador.

        Parámetros:
            x (int): Posición inicial en el eje X
            y (int): Posición inicial en el eje Y
            radio (int): Tamaño del círculo que representa al jugador
        """
        super().__init__(x, y, radio, velocidad=4)
        self._nombre = ""
        self._vidas = 3
        self._puntaje = 0

        # Posiciones de spawn para respawn
        self.spawn_x = x
        self.spawn_y = y

        # Contador de frames para animación de esfera pulsante
        self._frame_count = 0

        # Cargar sprite de Teseo
        try:
            import os

            ruta_sprite = "src/assets/imagenes/teseo.png"
            if not os.path.exists(ruta_sprite):
                print(f"⚠️ No se encontró el sprite en: {ruta_sprite}")
                self.sprite_teseo = None
                self.frames_teseo = []
            else:
                spritesheet = pygame.image.load(ruta_sprite).convert_alpha()

                # Dimensiones del spritesheet: 112x150
                # Suponiendo 4 columnas x 3 filas = 12 frames
                # Tamaño de cada frame: 28x50 (112/4 = 28, 150/3 = 50)
                frame_width = 28
                frame_height = 50

                # Extraer frames del spritesheet
                self.frames_teseo = []
                for fila in range(3):  # 3 filas
                    for col in range(4):  # 4 columnas
                        x = col * frame_width
                        y = fila * frame_height

                        # Crear superficie para el frame
                        frame = pygame.Surface(
                            (frame_width, frame_height), pygame.SRCALPHA
                        )
                        frame.blit(
                            spritesheet, (0, 0), (x, y, frame_width, frame_height)
                        )

                        # Escalar el frame al tamaño de celda
                        tamano_celda = ConfigJuego.TAM_CELDA
                        frame_escalado = pygame.transform.scale(
                            frame, (tamano_celda, tamano_celda)
                        )
                        self.frames_teseo.append(frame_escalado)

                # Frame actual para animación
                self.frame_index = 0
                self.sprite_teseo = self.frames_teseo[0] if self.frames_teseo else None

                print(
                    f"✅ Sprite de Teseo cargado: {len(self.frames_teseo)} frames, {tamano_celda}x{tamano_celda} cada uno"
                )
        except Exception as e:
            print(f"❌ Error al cargar sprite de Teseo: {e}")
            self.sprite_teseo = None
            self.frames_teseo = []

        # Rect de colisión más ajustado al círculo visual
        # Usamos FACTOR_RECT_COLISION para mejor precisión
        size = int(radio * ConfigJuego.FACTOR_RECT_COLISION)
        offset = (radio * 2 - size) // 2
        self._rect = pygame.Rect(x + offset, y + offset, size, size)

    @property
    def jugador_principal(self) -> pygame.Rect:
        """Rect de colisión del jugador (propiedad de solo lectura)."""
        return self._rect

    def mover(self, teclas) -> None:
        # ya no se usa, se una en pantalla_juego.py
        """
        Controla el movimiento del jugador según las teclas presionadas.

        El jugador se mueve usando las flechas del teclado:
            Flecha izquierda: mueve a la izquierda
            Flecha derecha: mueve a la derecha
            Flecha arriba: mueve hacia arriba
            Flecha abajo: mueve hacia abajo
        """
        if teclas[pygame.K_LEFT]:
            self._rect.x -= int(self.velocidad)
        if teclas[pygame.K_RIGHT]:
            self._rect.x += int(self.velocidad)
        if teclas[pygame.K_UP]:
            self._rect.y -= int(self.velocidad)
        if teclas[pygame.K_DOWN]:
            self._rect.y += int(self.velocidad)

    # === PROPERTIES PARA ENCAPSULACIÓN ===

    @property
    def vidas(self) -> int:
        """Obtiene el número de vidas restantes"""
        return self._vidas

    @property
    def puntaje(self) -> int:
        """Obtiene el puntaje actual"""
        return self._puntaje

    @property
    def nombre(self) -> str:
        """Obtiene el nombre del jugador"""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Establece el nombre del jugador"""
        self._nombre = valor

    # === MÉTODOS DE JUEGO ===

    def sumar_puntos(self, puntos: int) -> None:
        """
        incrementa puntos al puntaje del jugador.
        """
        self._puntaje += puntos

    def perder_vida(self):
        """
        Reduce una vida del jugador cuando es atrapado.
        Solo se ejecuta si el jugador tiene vidas disponibles.
        """
        if self._vidas > 0:
            self._vidas -= 1

    def esta_vivo(self) -> bool:
        """
        Verifica si el jugador aún tiene vidas restantes.

        Retorna:
            bool: True si tiene al menos una vida, False si ya no le quedan vidas
        """
        return self._vidas > 0

    def dibujar_jugador_principal(self, pantalla):
        """
        Dibuja al jugador usando el sprite animado de Teseo.
        """
        if not self.frames_teseo:
            # Si no se cargaron los frames, dibujar un rectángulo de placeholder
            pygame.draw.rect(pantalla, (0, 255, 255), self._rect)
            pygame.draw.rect(pantalla, (255, 255, 255), self._rect, 2)
            return

        # Actualizar animación (cambiar frame cada 8 frames del juego)
        self._frame_count += 1
        if self._frame_count >= 8:
            self._frame_count = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames_teseo)
            self.sprite_teseo = self.frames_teseo[self.frame_index]

        # Dibujar sprite centrado en el rect
        rect_sprite = self.sprite_teseo.get_rect(center=self._rect.center)
        pantalla.blit(self.sprite_teseo, rect_sprite)

    def actualizar_movimiento(self, dx, dy):
        """
        Actualiza el estado de movimiento del jugador.

        Args:
            dx: Cambio en X
            dy: Cambio en Y
        """
        # Método mantenido para compatibilidad con gestor de movimiento
        pass

    def respawn(self):
        """Reposiciona al jugador en su punto de spawn inicial."""
        self._rect.x = self.spawn_x
        self._rect.y = self.spawn_y
