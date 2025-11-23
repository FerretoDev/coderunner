"""
Menú principal del juego.

Muestra el título y opciones principales del juego.
"""

import pygame

from config.colores import PaletaColores
from config.config import ConfigJuego
from interfaz.componentes.input_texto import Boton
from interfaz.gestor_fuentes import GestorFuentes


class MenuPrincipal:
    """Menú principal con botones horizontales.

    Muestra el título y cuatro botones: Iniciar, Salón de la Fama, Administración y Salir.
    Devuelve un número según la opción elegida para que el llamador actúe.
    """

    def __init__(self, screen):
        self.screen = screen
        self.ancho = screen.get_width()
        self.alto = screen.get_height()

        # Usar gestor de fuentes compartido
        fuentes = GestorFuentes()
        self.font_titulo = fuentes.titulo_grande
        self.font_subtitulo = fuentes.texto_pequeño

        # Crear los botones alineados de forma horizontal
        self._crear_botones()

    def _crear_botones(self):
        """Calcula posiciones y crea los botones del menú."""
        ancho_boton = 180
        alto_boton = 60
        espacio = 20

        num_botones = 4
        ancho_total = (ancho_boton * num_botones) + (espacio * (num_botones - 1))
        inicio_x = (self.ancho - ancho_total) // 2
        y = 350

        self.botones = []
        textos = [
            "Iniciar Juego",
            "Salón de la Fama",
            "Administración",
            "Salir",
        ]

        for i, texto in enumerate(textos):
            x = inicio_x + (ancho_boton + espacio) * i
            self.botones.append(
                Boton(x, y, ancho_boton, alto_boton, texto, accion=i + 1)
            )

    def dibujar(self):
        """Pinta el fondo, título, línea decorativa, subtítulo, botones y footer."""
        self.screen.fill(PaletaColores.FONDO_PRINCIPAL)

        # Título con pequeña sombra para contraste
        titulo = self.font_titulo.render(
            ConfigJuego.TITULO, True, PaletaColores.TEXTO_PRINCIPAL
        )
        sombra = self.font_titulo.render(
            ConfigJuego.TITULO, True, PaletaColores.TEXTO_SOMBRA
        )

        sombra_rect = sombra.get_rect(center=(self.ancho // 2 + 3, 103))
        titulo_rect = titulo.get_rect(center=(self.ancho // 2, 100))

        self.screen.blit(sombra, sombra_rect)
        self.screen.blit(titulo, titulo_rect)

        # Línea decorativa bajo el título para separar visualmente
        pygame.draw.line(
            self.screen,
            PaletaColores.ACENTO_PRINCIPAL,
            (self.ancho // 2 - 150, 150),
            (self.ancho // 2 + 150, 150),
            3,
        )

        # Subtítulo con instrucciones del juego
        subtitulo = self.font_subtitulo.render(
            "Escapa del laberinto · Recolecta obsequios · Evita al enemigo",
            True,
            PaletaColores.TEXTO_DESACTIVADO,
        )
        subtitulo_rect = subtitulo.get_rect(center=(self.ancho // 2, 180))
        self.screen.blit(subtitulo, subtitulo_rect)

        # Botones del menú
        for boton in self.botones:
            boton.dibujar(self.screen)

        # Footer con indicación de uso del mouse
        footer = self.font_subtitulo.render(
            "Usa el mouse para seleccionar", True, PaletaColores.BORDE_NORMAL
        )
        footer_rect = footer.get_rect(center=(self.ancho // 2, self.alto - 30))
        self.screen.blit(footer, footer_rect)

        pygame.display.flip()

    def ejecutar(self):
        """Loop del menú: procesa eventos y devuelve la opción elegida."""
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return 4

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return 4

                # Verifica si algún botón recibió un click válido
                for boton in self.botones:
                    if boton.manejar_evento(evento, mouse_pos):
                        return boton.accion

            self.dibujar()
