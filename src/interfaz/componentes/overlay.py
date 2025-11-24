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
    Panel con fondo y borde estilo pixel art.

    Componente reutilizable para cajas de diálogo, ventanas modales, etc.
    Estilo retro sin bordes redondeados.
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
        estilo_pixel=True,
    ):
        """
        Inicializa el panel.

        Args:
            x, y: Posición del panel
            ancho, alto: Dimensiones del panel
            color_fondo: Color de fondo (tuple RGB)
            color_borde: Color del borde (tuple RGB)
            grosor_borde: Grosor del borde en pixels
            estilo_pixel: Si usar bordes pixelados (True) o redondeados (False)
        """
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color_fondo = color_fondo
        self.color_borde = color_borde
        self.grosor_borde = grosor_borde
        self.estilo_pixel = estilo_pixel

    def dibujar(self, screen):
        """
        Dibuja el panel en la pantalla con estilo pixel art.

        Args:
            screen: Surface donde dibujar
        """
        # Dibujar fondo
        pygame.draw.rect(screen, self.color_fondo, self.rect)

        # Dibujar borde exterior
        pygame.draw.rect(screen, self.color_borde, self.rect, self.grosor_borde)

        # Efecto 3D pixel art: líneas de luz y sombra
        if self.estilo_pixel and self.grosor_borde > 1:
            # Línea de luz superior e izquierda (más clara)
            color_luz = tuple(min(255, c + 40) for c in self.color_borde)
            pygame.draw.line(
                screen,
                color_luz,
                (self.rect.left, self.rect.top),
                (self.rect.right - 1, self.rect.top),
                1,
            )
            pygame.draw.line(
                screen,
                color_luz,
                (self.rect.left, self.rect.top),
                (self.rect.left, self.rect.bottom - 1),
                1,
            )

            # Línea de sombra inferior y derecha (más oscura)
            color_sombra = tuple(max(0, c - 40) for c in self.color_borde)
            pygame.draw.line(
                screen,
                color_sombra,
                (self.rect.left, self.rect.bottom - 1),
                (self.rect.right, self.rect.bottom - 1),
                1,
            )
            pygame.draw.line(
                screen,
                color_sombra,
                (self.rect.right - 1, self.rect.top),
                (self.rect.right - 1, self.rect.bottom),
                1,
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
