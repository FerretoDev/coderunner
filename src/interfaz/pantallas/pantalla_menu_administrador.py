"""
Menú de opciones administrativas.
"""

import pygame

from interfaz.componentes.boton_adaptable import BotonGrande
from interfaz.componentes.titulo_arcade import (
    LineaDecorativa,
    SubtituloArcade,
    TituloArcade,
)
from interfaz.gestor_fuentes import GestorFuentes


class PantallaMenuAdministrador:
    """
    Menú administrativo con opciones para cargar laberinto,
    reiniciar salón de fama y volver al menú principal.
    """

    def __init__(self, screen):
        self.screen = screen
        self.ancho = screen.get_width()
        self.alto = screen.get_height()

        self.COLORES = {
            "fondo": (20, 20, 30),
            "texto": (255, 255, 255),
            "acento": (0, 200, 100),
        }

        fuentes = GestorFuentes()
        self.font_titulo = fuentes.titulo_grande
        self.font_subtitulo = fuentes.texto_grande

        # Componentes arcade
        self.titulo = TituloArcade("PANEL DE ADMINISTRACION", y=60, estilo="grande")
        self.subtitulo = SubtituloArcade("Selecciona una opcion", y=130)
        self.linea = LineaDecorativa(y=160, ancho_porcentaje=60, doble=True)

        # Crear botones verticales
        self._crear_botones()

    def _crear_botones(self):
        """Crea los botones del menú administrativo con estilo arcade."""
        y_inicial = 210
        espacio = 15

        self.botones = []
        textos_acciones = [
            ("Cargar Laberinto", 1),
            ("Reiniciar Salon de Fama", 2),
            ("Volver al Menu", 3),
        ]

        for i, (texto, accion) in enumerate(textos_acciones):
            y = y_inicial + (60 + espacio) * i
            boton = BotonGrande(self.ancho // 2, y, texto, accion=accion)
            boton.centrar_horizontalmente(self.ancho)
            self.botones.append(boton)

    def dibujar(self):
        """Dibuja la pantalla del menú administrativo."""
        self.screen.fill(self.COLORES["fondo"])

        # Componentes arcade
        self.titulo.dibujar(self.screen)
        self.subtitulo.dibujar(self.screen)
        self.linea.dibujar(self.screen)

        # Dibujar botones
        for boton in self.botones:
            boton.dibujar(self.screen)

        pygame.display.flip()

    def ejecutar(self):
        """
        Loop del menú administrativo.

        Returns:
            int: Opción seleccionada (1=Cargar Laberinto, 2=Reiniciar Salón, 3=Volver)
        """
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return 3  # Volver

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return 3  # Volver

                # Verificar clicks en botones
                for boton in self.botones:
                    if boton.manejar_evento(evento, mouse_pos):
                        return boton.accion

            self.dibujar()
