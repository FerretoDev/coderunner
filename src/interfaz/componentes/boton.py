"""
Componente de botón pixel art estilo retro.
Basado en: Shovel Knight, Zelda Minish Cap.
"""

import pygame
from interfaz.paleta_ui import PaletaUI
from interfaz.gestor_fuentes import GestorFuentes


class Boton:
    """
    Botón estilo pixel art con estados (normal, hover, pressed).

    Características:
    - Bordes pixelados de 2px
    - Sombra diagonal pronunciada
    - Cambio de color por estado
    - Texto centrado con sombra
    """

    def __init__(self, x, y, width, height, texto, callback=None):
        """
        Inicializa el botón.

        Args:
            x: Posición X
            y: Posición Y
            width: Ancho del botón
            height: Alto del botón
            texto: Texto a mostrar
            callback: Función a ejecutar al hacer clic
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.texto = texto
        self.callback = callback

        # Estados
        self.estado = "normal"  # normal, hover, pressed, disabled
        self.habilitado = True

        # Fuente
        gestor = GestorFuentes.obtener()
        self.fuente = gestor.texto_normal

    def manejar_evento(self, evento):
        """
        Maneja eventos de mouse.

        Args:
            evento: pygame.Event

        Returns:
            bool: True si el botón fue clickeado
        """
        if not self.habilitado:
            return False

        if evento.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(evento.pos):
                self.estado = "hover"
            else:
                self.estado = "normal"

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos):
                self.estado = "pressed"

        elif evento.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(evento.pos) and self.estado == "pressed":
                if self.callback:
                    self.callback()
                self.estado = "hover"
                return True

        return False

    def actualizar(self, pos_mouse):
        """
        Actualiza el estado del botón según la posición del mouse.

        Args:
            pos_mouse: Tupla (x, y) con posición del mouse
        """
        if not self.habilitado:
            self.estado = "disabled"
        elif self.rect.collidepoint(pos_mouse):
            if self.estado == "normal":
                self.estado = "hover"
        else:
            self.estado = "normal"

    def dibujar(self, surface):
        """
        Dibuja el botón en la superficie.

        Args:
            surface: pygame.Surface donde dibujar
        """
        # Colores según estado
        if self.estado == "normal":
            color_fondo = PaletaUI.BUTTON_NORMAL
            color_borde = PaletaUI.LIGHT
            color_sombra = PaletaUI.DARK
        elif self.estado == "hover":
            color_fondo = PaletaUI.BUTTON_HOVER
            color_borde = PaletaUI.WHITE
            color_sombra = PaletaUI.BLUE
        elif self.estado == "pressed":
            color_fondo = PaletaUI.BUTTON_PRESSED
            color_borde = PaletaUI.GRAY
            color_sombra = (0, 0, 0)
        else:  # disabled
            color_fondo = PaletaUI.BUTTON_DISABLED
            color_borde = PaletaUI.GRAY
            color_sombra = PaletaUI.DARK

        # Dibujar sombra (offset 2px diagonal abajo-derecha)
        rect_sombra = self.rect.copy()
        if self.estado != "pressed":
            rect_sombra.x += 2
            rect_sombra.y += 2
            pygame.draw.rect(surface, color_sombra, rect_sombra)

        # Dibujar fondo del botón
        pygame.draw.rect(surface, color_fondo, self.rect)

        # Dibujar borde (2px de grosor)
        pygame.draw.rect(surface, color_borde, self.rect, 2)

        # Renderizar texto con sombra
        color_texto = PaletaUI.WHITE if self.habilitado else PaletaUI.GRAY
        texto_render = self.fuente.render(self.texto, True, color_texto)
        texto_rect = texto_render.get_rect(center=self.rect.center)

        # Sombra del texto (1px offset)
        if self.habilitado:
            texto_sombra = self.fuente.render(self.texto, True, PaletaUI.DARK)
            sombra_rect = texto_rect.copy()
            sombra_rect.x += 1
            sombra_rect.y += 1
            surface.blit(texto_sombra, sombra_rect)

        # Texto principal
        surface.blit(texto_render, texto_rect)

    def set_habilitado(self, habilitado):
        """
        Habilita o deshabilita el botón.

        Args:
            habilitado: bool
        """
        self.habilitado = habilitado
        if not habilitado:
            self.estado = "disabled"
