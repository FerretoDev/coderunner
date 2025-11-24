"""
Pantalla de autenticación para el administrador.
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


class PantallaAdministracion:
    """Solicita la clave de administrador y la devuelve para validarla afuera."""

    def __init__(self, screen):
        self.screen = screen
        self.ancho = screen.get_width()
        self.alto = screen.get_height()
        self.autenticado = False

        fuentes = GestorFuentes()
        self.font_hint = fuentes.texto_info

        # Componentes arcade
        self.titulo = TituloArcade("ADMINISTRACION", y=50, estilo="mediano")
        self.subtitulo = SubtituloArcade("Ingresa la clave de administrador", y=120)
        self.linea = LineaDecorativa(y=150, ancho_porcentaje=50, doble=True)

        # Input de clave con placeholder
        self.input_clave = InputTexto(
            self.ancho // 2 - 200, 200, 400, 50, "Ingresa la clave"
        )

        # Botones arcade
        self.btn_ingresar = BotonGrande(self.ancho // 2, 290, "Ingresar")
        self.btn_ingresar.centrar_horizontalmente(self.ancho)

        self.btn_volver = BotonGrande(self.ancho // 2, 365, "Volver")
        self.btn_volver.centrar_horizontalmente(self.ancho)

    def dibujar(self):
        """Dibuja la pantalla de autenticación con input, botones y un hint."""
        self.screen.fill((20, 20, 30))

        # Componentes arcade
        self.titulo.dibujar(self.screen)
        self.subtitulo.dibujar(self.screen)
        self.linea.dibujar(self.screen)

        # Input
        self.input_clave.dibujar(self.screen)

        # Botones
        self.btn_ingresar.dibujar(self.screen)
        self.btn_volver.dibujar(self.screen)

        # Hint con icono de candado
        hint = self.font_hint.render(
            "🔒 Clave por defecto: admin123", True, (100, 120, 150)
        )
        hint_rect = hint.get_rect(center=(self.ancho // 2, self.alto - 40))
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
