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
        Dibuja al jugador con efecto visual pulsante.
        """
        centro = self._rect.center

        # Contador de frames para animación
        self._frame_count += 1

        # Efecto pulsante usando seno (oscila entre -1 y 1)
        pulso = abs(math.sin(self._frame_count * 0.2)) * 3
        radio_pulso = self.radio + pulso

        # Variar intensidad del color cyan/azul
        intensidad = int(200 + 55 * abs(math.sin(self._frame_count * 0.15)))
        color_principal = (50, intensidad, intensidad)  # Cyan

        # Círculo principal con pulsación
        pygame.draw.circle(pantalla, color_principal, centro, int(radio_pulso))

        # Borde blanco para contraste
        pygame.draw.circle(pantalla, (255, 255, 255), centro, int(radio_pulso), 2)

        # Centro brillante para dar efecto de "energía"
        pygame.draw.circle(pantalla, (150, 255, 255), centro, int(self.radio * 0.6))

        # Puntos brillantes simulando "ojos" o núcleo
        ojo_offset = 4
        pygame.draw.circle(
            pantalla, (255, 255, 255), (centro[0] - ojo_offset, centro[1] - 2), 2
        )
        pygame.draw.circle(
            pantalla, (255, 255, 255), (centro[0] + ojo_offset, centro[1] - 2), 2
        )

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
