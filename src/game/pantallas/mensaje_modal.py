"""
Modal para mostrar mensajes al usuario.
"""

import pygame

from ..componentes.input_texto import Boton


class MensajeModal:
    """Cuadro de diálogo simple para mostrar mensajes y confirmar con OK."""

    def __init__(self, screen, titulo, mensaje, tipo="info"):
        self.screen = screen
        self.ancho = screen.get_width()
        self.alto = screen.get_height()
        self.titulo = titulo
        self.mensaje = mensaje
        self.tipo = tipo

        self.font_titulo = pygame.font.Font(None, 48)
        self.font_mensaje = pygame.font.Font(None, 32)

        # Botón OK centrado bajo el mensaje
        self.btn_ok = Boton(self.ancho // 2 - 75, self.alto // 2 + 60, 150, 50, "OK")

        # Colores de acento según el tipo de mensaje
        colores = {
            "info": (0, 150, 255),
            "success": (0, 200, 100),
            "error": (255, 50, 50),
            "warning": (255, 200, 0),
        }
        self.color_acento = colores.get(tipo, colores["info"])

    def dibujar(self):
        """Dibuja fondo translúcido, caja con borde, textos y el botón OK."""
        # Fondo semitransparente para centrar la atención
        overlay = pygame.Surface((self.ancho, self.alto))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Caja central del modal
        modal_rect = pygame.Rect(self.ancho // 2 - 250, self.alto // 2 - 100, 500, 200)
        pygame.draw.rect(self.screen, (40, 40, 60), modal_rect, border_radius=15)
        pygame.draw.rect(
            self.screen, self.color_acento, modal_rect, 3, border_radius=15
        )

        # Título centrado
        titulo_surface = self.font_titulo.render(self.titulo, True, self.color_acento)
        titulo_rect = titulo_surface.get_rect(
            center=(self.ancho // 2, self.alto // 2 - 50)
        )
        self.screen.blit(titulo_surface, titulo_rect)

        # Mensaje principal
        mensaje_surface = self.font_mensaje.render(self.mensaje, True, (255, 255, 255))
        mensaje_rect = mensaje_surface.get_rect(
            center=(self.ancho // 2, self.alto // 2)
        )
        self.screen.blit(mensaje_surface, mensaje_rect)

        # Botón OK
        self.btn_ok.dibujar(self.screen)

        pygame.display.flip()

    def ejecutar(self):
        """Loop del modal: se cierra con OK, Enter/Escape o al cerrar la ventana."""
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return

                if evento.type == pygame.KEYDOWN:
                    if evento.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                        return

                if self.btn_ok.manejar_evento(evento, mouse_pos):
                    return

            self.dibujar()
