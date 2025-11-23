"""
Modal para mostrar mensajes al usuario.
"""

import pygame

from interfaz.componentes.input_texto import Boton
from interfaz.componentes.overlay import Overlay, Panel
from interfaz.gestor_fuentes import GestorFuentes
from config.colores import PaletaColores


class MensajeModal:
    """Cuadro de diálogo simple para mostrar mensajes y confirmar con OK."""

    def __init__(self, screen, titulo, mensaje, tipo="info"):
        self.screen = screen
        self.ancho = screen.get_width()
        self.alto = screen.get_height()
        self.titulo = titulo
        self.mensaje = mensaje
        self.tipo = tipo

        # Usar gestor de fuentes compartido
        fuentes = GestorFuentes()
        self.font_titulo = fuentes.titulo_pequeño
        self.font_mensaje = fuentes.texto_grande

        # Overlay reutilizable
        self.overlay = Overlay(self.ancho, self.alto, PaletaColores.FONDO_OVERLAY, 200)

        # Panel del modal
        self.panel = Panel(
            self.ancho // 2 - 250,
            self.alto // 2 - 100,
            500,
            200,
            PaletaColores.FONDO_MODAL,
            PaletaColores.obtener_color_tipo(tipo),
        )

        # Botón OK centrado bajo el mensaje
        self.btn_ok = Boton(self.ancho // 2 - 75, self.alto // 2 + 60, 150, 50, "OK")

        # Color de acento según el tipo
        self.color_acento = PaletaColores.obtener_color_tipo(tipo)

    def dibujar(self):
        """Dibuja fondo translúcido, caja con borde, textos y el botón OK."""
        # Overlay semitransparente
        self.overlay.dibujar(self.screen)

        # Panel del modal
        self.panel.dibujar(self.screen)

        # Título centrado
        titulo_surface = self.font_titulo.render(self.titulo, True, self.color_acento)
        titulo_rect = titulo_surface.get_rect(
            center=(self.ancho // 2, self.alto // 2 - 50)
        )
        self.screen.blit(titulo_surface, titulo_rect)

        # Mensaje principal
        mensaje_surface = self.font_mensaje.render(
            self.mensaje, True, PaletaColores.TEXTO_PRINCIPAL
        )
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
