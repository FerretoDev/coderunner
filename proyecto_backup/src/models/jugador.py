import pygame

from .personaje import Personaje


class Jugador(Personaje):
    """
    Clase que representa al jugador controlado por el usuario.
    """

    def __init__(self, x, y, radio):
        super().__init__(x, y, radio, velocidad=4)
        self._nombre = ""
        self._vidas = 3
        self._puntaje = 0
        self.color = (255, 0, 0)
        self.jugador_principal = pygame.Rect(x, y, radio * 2, radio * 2)

    def mover(self, teclas) -> None:
        """Mueve al jugador en la dirección especificada."""
        if teclas[pygame.K_LEFT]:
            self.jugador_principal.x -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            self.jugador_principal.x += self.velocidad
        if teclas[pygame.K_UP]:
            self.jugador_principal.y -= self.velocidad
        if teclas[pygame.K_DOWN]:
            self.jugador_principal.y += self.velocidad

    def sumar_puntos(self, puntos: int) -> None:
        """Suma puntos al puntaje del jugador."""
        self._puntaje += puntos

    def perder_vida(self) -> None:
        """Resta una vida cuando la computadora atrapa al jugador"""
        if self._vidas > 0:
            self._vidas -= 1

    def esta_vivo(self) -> bool:
        """Verifica si el jugador aún tiene vidas restantes."""
        return self._vidas > 0

    def dibujar_jugador_principal(self, pantalla):
        centro = self.jugador_principal.center
        pygame.draw.circle(pantalla, self.color, centro, self.radio)
