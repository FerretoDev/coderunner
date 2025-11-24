"""
Menú principal del juego.

Muestra el título y opciones principales del juego.
"""

import pygame

from config.colores import PaletaColores
from config.config import ConfigJuego
from interfaz.componentes.boton_adaptable import BotonGrande
from interfaz.componentes.titulo_arcade import (
    FooterArcade,
    LineaDecorativa,
    SubtituloArcade,
    TituloArcade,
)


class MenuPrincipal:
    """Menú principal con componentes arcade reutilizables.

    Muestra el título y botones adaptables con efectos pixel art.
    """

    def __init__(self, screen):
        self.screen = screen
        self.ancho = screen.get_width()
        self.alto = screen.get_height()

        # Crear componentes visuales
        self.titulo = TituloArcade(ConfigJuego.TITULO, 60, "grande")
        # self.subtitulo = SubtituloArcade("El laberinto retro", 130)
        self.linea_decorativa = LineaDecorativa(160, ancho_porcentaje=50, doble=True)
        self.footer = FooterArcade("Usa el mouse para seleccionar")

        # Crear los botones adaptativos
        self._crear_botones()

    def _crear_botones(self):
        """Crea los botones del menú principal con componentes adaptables."""
        opciones = [
            ("Iniciar Juego", 1),
            ("Salón de la Fama", 2),
            ("Administración", 3),
            ("Salir", 4),
        ]

        # Comenzar los botones justo después de la línea decorativa
        y_inicial = 200
        alto_boton = 60
        espacio = 15  # Espacio compacto entre botones

        self.botones = []
        for i, (texto, accion) in enumerate(opciones):
            y = y_inicial + i * (alto_boton + espacio)
            # Crear botón adaptable (se ajusta automáticamente al texto)
            boton = BotonGrande(0, y, texto, accion)
            # Centrarlo horizontalmente
            boton.centrar_horizontalmente(self.ancho)
            self.botones.append(boton)

    def dibujar(self):
        """Dibuja el menú con todos sus componentes."""
        self.screen.fill(PaletaColores.FONDO_PRINCIPAL)

        # Dibujar componentes visuales
        self.titulo.dibujar(self.screen)
        self.linea_decorativa.dibujar(self.screen)
        # self.subtitulo.dibujar(self.screen)
        self.footer.dibujar(self.screen)

        # Dibujar botones
        for boton in self.botones:
            boton.dibujar(self.screen)

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

            # Redibujar constantemente para actualizar efectos hover
            self.dibujar()
            pygame.display.flip()
