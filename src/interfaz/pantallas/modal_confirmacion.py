"""
Modal de confirmación para acciones críticas.
"""

import pygame

from interfaz.componentes.input_texto import Boton


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

        self.font_titulo = pygame.font.Font(None, 44)
        self.font_mensaje = pygame.font.Font(None, 28)

        # Botones
        self.btn_si = Boton(self.ancho // 2 - 160, self.alto // 2 + 50, 140, 50, "✓ Sí")
        self.btn_no = Boton(self.ancho // 2 + 20, self.alto // 2 + 50, 140, 50, "✗ No")

    def dibujar(self):
        """Dibuja el modal de confirmación."""
        # Fondo semitransparente
        overlay = pygame.Surface((self.ancho, self.alto))
        overlay.set_alpha(220)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Caja del modal
        modal_rect = pygame.Rect(self.ancho // 2 - 300, self.alto // 2 - 120, 600, 240)
        pygame.draw.rect(self.screen, (40, 40, 60), modal_rect, border_radius=15)
        pygame.draw.rect(self.screen, (255, 200, 0), modal_rect, 3, border_radius=15)

        # Título
        titulo_surface = self.font_titulo.render(self.titulo, True, (255, 200, 0))
        titulo_rect = titulo_surface.get_rect(
            center=(self.ancho // 2, self.alto // 2 - 70)
        )
        self.screen.blit(titulo_surface, titulo_rect)

        # Mensaje (puede tener múltiples líneas)
        lineas = self.mensaje.split("\n")
        y_offset = -20
        for linea in lineas:
            mensaje_surface = self.font_mensaje.render(linea, True, (255, 255, 255))
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
