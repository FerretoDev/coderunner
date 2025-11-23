"""
Componente de overlay (fondo semitransparente) para modales.
"""

import pygame


class Overlay:
    """
    Crea un fondo semitransparente sobre la pantalla.

    Útil para modales, pausas y menús que necesitan destacar
    sobre el contenido de fondo.
    """

    def __init__(self, ancho, alto, color=(0, 0, 0), alpha=200):
        """
        Inicializa el overlay.

        Args:
            ancho: Ancho de la pantalla
            alto: Alto de la pantalla
            color: Color del overlay (tuple RGB), default negro
            alpha: Transparencia (0-255), default 200
        """
        self.surface = pygame.Surface((ancho, alto))
        self.surface.set_alpha(alpha)
        self.surface.fill(color)

    def dibujar(self, screen, posicion=(0, 0)):
        """
        Dibuja el overlay en la pantalla.

        Args:
            screen: Surface donde dibujar
            posicion: Posición (x, y), default (0, 0)
        """
        screen.blit(self.surface, posicion)

    def cambiar_alpha(self, nuevo_alpha):
        """
        Cambia la transparencia del overlay.

        Args:
            nuevo_alpha: Nuevo valor de transparencia (0-255)
        """
        self.surface.set_alpha(nuevo_alpha)

    def cambiar_color(self, nuevo_color):
        """
        Cambia el color del overlay.

        Args:
            nuevo_color: Nuevo color (tuple RGB)
        """
        self.surface.fill(nuevo_color)


class Panel:
    """
    Panel con fondo, borde redondeado y opcionalmente título.

    Componente reutilizable para cajas de diálogo, ventanas modales, etc.
    """

    def __init__(
        self,
        x,
        y,
        ancho,
        alto,
        color_fondo=(40, 40, 60),
        color_borde=(100, 150, 255),
        grosor_borde=3,
        radio_borde=15,
    ):
        """
        Inicializa el panel.

        Args:
            x, y: Posición del panel
            ancho, alto: Dimensiones del panel
            color_fondo: Color de fondo (tuple RGB)
            color_borde: Color del borde (tuple RGB)
            grosor_borde: Grosor del borde en pixels
            radio_borde: Radio de las esquinas redondeadas
        """
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color_fondo = color_fondo
        self.color_borde = color_borde
        self.grosor_borde = grosor_borde
        self.radio_borde = radio_borde

    def dibujar(self, screen):
        """
        Dibuja el panel en la pantalla.

        Args:
            screen: Surface donde dibujar
        """
        # Dibujar fondo
        pygame.draw.rect(
            screen, self.color_fondo, self.rect, border_radius=self.radio_borde
        )

        # Dibujar borde
        pygame.draw.rect(
            screen,
            self.color_borde,
            self.rect,
            self.grosor_borde,
            border_radius=self.radio_borde,
        )

    def obtener_centro(self):
        """Retorna la posición del centro del panel."""
        return self.rect.center

    def cambiar_color_fondo(self, nuevo_color):
        """Cambia el color de fondo del panel."""
        self.color_fondo = nuevo_color

    def cambiar_color_borde(self, nuevo_color):
        """Cambia el color del borde del panel."""
        self.color_borde = nuevo_color
