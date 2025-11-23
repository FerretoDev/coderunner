"""
Modal de confirmación para acciones críticas.
"""

import pygame

from interfaz.componentes.input_texto import Boton
from interfaz.componentes.overlay import Overlay, Panel
from interfaz.gestor_fuentes import GestorFuentes
from config.colores import PaletaColores


class ModalConfirmacion:
    """
    Modal de confirmación con botones Sí/No.
    Se usa para confirmar acciones críticas como salir o reiniciar datos.
    """

    def __init__(self, screen, titulo, mensaje):
        self.screen = screen
        self.ancho = screen.get_width()
        self.alto = screen.get_height()
        self.titulo = titulo
        self.mensaje = mensaje

        # Usar gestor de fuentes compartido
        fuentes = GestorFuentes()
        self.font_titulo = fuentes.titulo_mini
        self.font_mensaje = fuentes.texto_normal

        # Overlay reutilizable
        self.overlay = Overlay(self.ancho, self.alto, PaletaColores.FONDO_OVERLAY, 220)

        # Panel del modal
        self.panel = Panel(
            self.ancho // 2 - 300,
            self.alto // 2 - 120,
            600,
            240,
            PaletaColores.FONDO_MODAL,
            PaletaColores.ACENTO_WARNING,
        )

        # Botones
        self.btn_si = Boton(self.ancho // 2 - 160, self.alto // 2 + 50, 140, 50, "Sí")
        self.btn_no = Boton(self.ancho // 2 + 20, self.alto // 2 + 50, 140, 50, "No")

    def dibujar(self):
        """Dibuja el modal de confirmación."""
        # Overlay semitransparente
        self.overlay.dibujar(self.screen)

        # Panel del modal
        self.panel.dibujar(self.screen)

        # Título
        titulo_surface = self.font_titulo.render(
            self.titulo, True, PaletaColores.ACENTO_WARNING
        )
        titulo_rect = titulo_surface.get_rect(
            center=(self.ancho // 2, self.alto // 2 - 70)
        )
        self.screen.blit(titulo_surface, titulo_rect)

        # Mensaje (puede tener múltiples líneas)
        lineas = self.mensaje.split("\n")
        y_offset = -20
        for linea in lineas:
            mensaje_surface = self.font_mensaje.render(
                linea, True, PaletaColores.TEXTO_PRINCIPAL
            )
            mensaje_rect = mensaje_surface.get_rect(
                center=(self.ancho // 2, self.alto // 2 + y_offset)
            )
            self.screen.blit(mensaje_surface, mensaje_rect)
            y_offset += 35

        # Botones
        self.btn_si.dibujar(self.screen)
        self.btn_no.dibujar(self.screen)

        pygame.display.flip()

    def ejecutar(self):
        """
        Loop del modal de confirmación.

        Returns:
            bool: True si confirmó (Sí), False si canceló (No)
        """
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return False
                    if evento.key == pygame.K_RETURN:
                        return True

                # Botones
                if self.btn_si.manejar_evento(evento, mouse_pos):
                    return True
                if self.btn_no.manejar_evento(evento, mouse_pos):
                    return False

            self.dibujar()
