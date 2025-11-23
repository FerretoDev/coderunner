"""
Pantalla para ingresar el nombre del jugador antes de iniciar partida.
"""

import pygame

from interfaz.componentes.boton_adaptable import BotonGrande
from interfaz.componentes.input_texto import InputTexto
from interfaz.componentes.titulo_arcade import (
    LineaDecorativa,
    SubtituloArcade,
    TituloArcade,
)
from interfaz.gestor_fuentes import GestorFuentes


class PantallaIniciarJuego:
    """Pantalla para ingresar nombre del jugador y continuar o volver."""

    def __init__(self, screen):
        self.screen = screen
        self.ancho = screen.get_width()
        self.alto = screen.get_height()

        fuentes = GestorFuentes()
        self.font_titulo = fuentes.titulo_normal
        self.font_texto = fuentes.titulo_pequeño

        # Componentes arcade
        self.titulo = TituloArcade("NUEVO JUEGO", y=60, estilo="grande")
        self.subtitulo = SubtituloArcade("Ingresa tu nombre para comenzar", y=130)
        self.linea = LineaDecorativa(y=160, ancho_porcentaje=50, doble=True)

        # Campo de texto para el nombre con placeholder
        self.input_nombre = InputTexto(
            self.ancho // 2 - 200, 210, 400, 50, "Ingresa tu nombre"
        )

        # Botones arcade
        self.btn_continuar = BotonGrande(self.ancho // 2, 300, "Continuar")
        self.btn_continuar.centrar_horizontalmente(self.ancho)

        self.btn_volver = BotonGrande(self.ancho // 2, 375, "Volver")
        self.btn_volver.centrar_horizontalmente(self.ancho)

    def dibujar(self):
        """Dibuja fondo, textos, input y botones."""
        self.screen.fill((20, 20, 30))

        # Componentes arcade
        self.titulo.dibujar(self.screen)
        self.subtitulo.dibujar(self.screen)
        self.linea.dibujar(self.screen)

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
