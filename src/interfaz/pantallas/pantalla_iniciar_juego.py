"""
Pantalla para ingresar el nombre del jugador antes de iniciar partida.
"""

import pygame

from interfaz.componentes.input_texto import Boton, InputTexto


class PantallaIniciarJuego:
    """Pantalla para ingresar nombre del jugador y continuar o volver."""

    def __init__(self, screen):
        self.screen = screen
        self.ancho = screen.get_width()
        self.alto = screen.get_height()

        self.font_titulo = pygame.font.Font(None, 56)
        self.font_texto = pygame.font.Font(None, 32)

        # Campo de texto para el nombre con placeholder
        self.input_nombre = InputTexto(
            self.ancho // 2 - 200, 250, 400, 50, "Ingresa tu nombre"
        )

        # Botones de acción
        self.btn_continuar = Boton(self.ancho // 2 - 100, 350, 200, 50, "Continuar")
        self.btn_volver = Boton(self.ancho // 2 - 100, 420, 200, 50, "Volver")

    def dibujar(self):
        """Dibuja fondo, textos, input y botones."""
        self.screen.fill((20, 20, 30))

        # Título
        titulo = self.font_titulo.render("Nuevo Juego", True, (255, 255, 255))
        titulo_rect = titulo.get_rect(center=(self.ancho // 2, 100))
        self.screen.blit(titulo, titulo_rect)

        # Instrucción
        instruccion = self.font_texto.render(
            "Ingresa tu nombre para comenzar:", True, (200, 200, 200)
        )
        instruccion_rect = instruccion.get_rect(center=(self.ancho // 2, 180))
        self.screen.blit(instruccion, instruccion_rect)

        # Input de nombre
        self.input_nombre.dibujar(self.screen)

        # Botones
        self.btn_continuar.dibujar(self.screen)
        self.btn_volver.dibujar(self.screen)

        pygame.display.flip()

    def ejecutar(self):
        """Loop: recoge nombre por Enter o botón, o vuelve con Escape/Volver."""
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

                # Input: si manejar_evento devuelve True, se presionó Enter
                if self.input_nombre.manejar_evento(evento):
                    nombre = self.input_nombre.obtener_texto()
                    if nombre:
                        return nombre

                # Botón Continuar: intenta confirmar el nombre
                if self.btn_continuar.manejar_evento(evento, mouse_pos):
                    nombre = self.input_nombre.obtener_texto()
                    if nombre:
                        return nombre

                # Botón Volver: regresa sin nombre
                if self.btn_volver.manejar_evento(evento, mouse_pos):
                    return None

            self.dibujar()
