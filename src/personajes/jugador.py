import pygame

from config.config import ConfigJuego

from .personaje import Personaje
from .sprite_animado import SpriteTheseusRunner


class Jugador(Personaje):
    """
    Clase que representa al jugador controlado por el usuario.

    Esta clase maneja:
        El movimiento del jugador usando las teclas de dirección
        El sistema de vidas (3 vidas iniciales)
        El sistema de puntaje
        La representación visual del jugador con sprite animado de Theseus
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

        # Sprite animado de Theseus
        self.sprite = SpriteTheseusRunner(escala=0.5)  # 32x48 píxeles
        self.direccion_derecha = True
        self.moviendo = False

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
        Dibuja al jugador en la pantalla con sprite animado de Theseus.
        """
        # Actualizar animación del sprite
        self.sprite.actualizar(
            moviendo=self.moviendo,
            saltando=False,
            muriendo=not self.esta_vivo(),
            direccion_derecha=self.direccion_derecha,
        )

        # Dibujar sprite centrado en la posición del jugador
        centro = self._rect.center
        self.sprite.dibujar(pantalla, centro[0], centro[1])

    def actualizar_movimiento(self, dx, dy):
        """
        Actualiza el estado de movimiento del jugador.

        Args:
            dx: Cambio en X
            dy: Cambio en Y
        """
        # Detectar si está moviendo
        self.moviendo = dx != 0 or dy != 0

        # Detectar dirección (solo si hay movimiento horizontal)
        if dx > 0:
            self.direccion_derecha = True
        elif dx < 0:
            self.direccion_derecha = False

    def respawn(self):
        """Reposiciona al jugador en su punto de spawn inicial."""
        self._rect.x = self.spawn_x
        self._rect.y = self.spawn_y
        self.moviendo = False
