"""
Pantalla de autenticación para el administrador.
"""

import pygame

from interfaz.componentes.input_texto import Boton, InputTexto


class PantallaAdministracion:
    """Solicita la clave de administrador y la devuelve para validarla afuera."""

    def __init__(self, screen):
        self.screen = screen
        self.ancho = screen.get_width()
        self.alto = screen.get_height()
        self.autenticado = False

        self.font_titulo = pygame.font.Font(None, 56)
        self.font_texto = pygame.font.Font(None, 32)

        # Input de clave con placeholder
        self.input_clave = InputTexto(
            self.ancho // 2 - 200, 250, 400, 50, "Ingresa la clave"
        )

        # Botones
        self.btn_ingresar = Boton(self.ancho // 2 - 100, 350, 200, 50, "Ingresar")
        self.btn_volver = Boton(self.ancho // 2 - 100, 420, 200, 50, "Volver")

    def dibujar(self):
        """Dibuja la pantalla de autenticación con input, botones y un hint."""
        self.screen.fill((20, 20, 30))

        # Título
        titulo = self.font_titulo.render("🔐 Administración", True, (255, 255, 255))
        titulo_rect = titulo.get_rect(center=(self.ancho // 2, 100))
        self.screen.blit(titulo, titulo_rect)

        # Instrucción
        instruccion = self.font_texto.render(
            "Ingresa la clave de administrador:", True, (200, 200, 200)
        )
        instruccion_rect = instruccion.get_rect(center=(self.ancho // 2, 180))
        self.screen.blit(instruccion, instruccion_rect)

        # Input y botones
        self.input_clave.dibujar(self.screen)
        self.btn_ingresar.dibujar(self.screen)
        self.btn_volver.dibujar(self.screen)

        # Hint visible al pie de pantalla
        hint = pygame.font.Font(None, 20).render(
            "Clave por defecto: admin123", True, (100, 100, 120)
        )
        hint_rect = hint.get_rect(center=(self.ancho // 2, self.alto - 30))
        self.screen.blit(hint, hint_rect)

        pygame.display.flip()

    def ejecutar(self):
        """Loop: devuelve la clave con Enter o Ingresar, o None al volver/salir."""
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return None

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return None

                # Input: Enter devuelve inmediatamente la clave
                if self.input_clave.manejar_evento(evento):
                    clave = self.input_clave.obtener_texto()
                    return clave

                # Botón Ingresar: también devuelve la clave
                if self.btn_ingresar.manejar_evento(evento, mouse_pos):
                    clave = self.input_clave.obtener_texto()
                    return clave

                # Botón Volver
                if self.btn_volver.manejar_evento(evento, mouse_pos):
                    return None

            self.dibujar()
