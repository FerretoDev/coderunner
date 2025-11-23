import pygame

from game.config import ConfigJuego

from .personaje import Personaje


class Jugador(Personaje):
    """
    Clase que representa al jugador controlado por el usuario.

    Esta clase maneja:
        El movimiento del jugador usando las teclas de dirección
        El sistema de vidas (3 vidas iniciales)
        El sistema de puntaje
        La representación visual del jugador (círculo rojo)
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
        # self.color = (255, 0, 0)

        # Cargar imagen del jugador
        self.imagen = pygame.image.load(
            "src/data/ImagenJugadorPrincipal.png"
        ).convert_alpha()

        self.imagen = pygame.transform.scale(self.imagen, (64, 64))

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
        Dibuja al jugador en la pantalla como un círculo rojo.

        Parámetros:
            pantalla: Superficie de pygame donde se dibujará el jugador
        """
        # centro = self.jugador_principal.center
        # pygame.draw.circle(pantalla, self.color, centro, self.radio)

        """
        Dibuja al jugador en la pantalla con su imagen.
        Si no se carga correctamente, dibuja un círculo rojo como respaldo.
        """
        try:
            # Obtener la posición donde se dibujará (centrando la imagen)
            centro = self._rect.center
            rect_imagen = self.imagen.get_rect(center=centro)
            pantalla.blit(self.imagen, rect_imagen)
        except AttributeError:
            # En caso de error o si no hay imagen, dibujar círculo
            pygame.draw.circle(pantalla, (255, 0, 0), self._rect.center, self.radio)
