"""
Pantalla para cargar archivos de laberinto.
"""

import pygame

from interfaz.componentes.boton_adaptable import BotonGrande, BotonPequeño
from interfaz.componentes.input_texto import InputTexto
from interfaz.componentes.titulo_arcade import (
    LineaDecorativa,
    SubtituloArcade,
    TituloArcade,
)
from interfaz.gestor_fuentes import GestorFuentes
from utilidades.helpers import resolver_ruta_laberinto


class PantallaCargaLaberinto:
    """
    Pantalla para seleccionar y cargar un archivo de laberinto.
    Permite ingresar la ruta del archivo manualmente.
    """

    def __init__(self, screen, admin):
        self.screen = screen
        self.ancho = screen.get_width()
        self.alto = screen.get_height()
        self.admin = admin

        fuentes = GestorFuentes()
        self.font_info = fuentes.texto_normal

        # Componentes arcade
        self.titulo = TituloArcade("CARGAR LABERINTO", y=50, estilo="grande")
        self.subtitulo = SubtituloArcade("Ingresa la ruta del archivo", y=115)
        self.linea = LineaDecorativa(y=145, ancho_porcentaje=60, doble=True)

        # Input para la ruta del archivo (más ancho)
        self.input_ruta = InputTexto(
            self.ancho // 2 - 450,
            180,
            950,
            50,
            # "laberintos/laberinto1.json",
            "Ruta del archivo (ej: src/data/laberintos/laberinto1.json)",
        )

        # Botones principales
        self.btn_cargar = BotonGrande(self.ancho // 2, 270, "Cargar")
        self.btn_cargar.centrar_horizontalmente(self.ancho)

        self.btn_volver = BotonGrande(self.ancho // 2, 345, "Cancelar")
        self.btn_volver.centrar_horizontalmente(self.ancho)

        # Botones de acceso rápido (más abajo para evitar superposición)
        btn_y = 470
        centro = self.ancho // 2

        self.btn_lab1 = BotonPequeño(centro - 250, btn_y, "Laberinto 1", accion="lab1")
        self.btn_lab2 = BotonPequeño(centro - 60, btn_y, "Laberinto 2", accion="lab2")
        self.btn_lab3 = BotonPequeño(centro + 130, btn_y, "Laberinto 3", accion="lab3")

        # Botón de ejemplo centrado
        self.btn_lab_ejemplo = BotonPequeño(
            centro - 60, btn_y + 55, "Ejemplo", accion="ejemplo"
        )

        self.archivo_seleccionado = None
        self.nombre_archivo = ""

    def dibujar(self):
        """Dibuja la pantalla de carga de laberinto."""
        self.screen.fill((20, 20, 30))

        # Componentes arcade
        self.titulo.dibujar(self.screen)
        self.subtitulo.dibujar(self.screen)
        self.linea.dibujar(self.screen)

        # Input de ruta
        self.input_ruta.dibujar(self.screen)

        # Botones principales
        self.btn_cargar.dibujar(self.screen)
        self.btn_volver.dibujar(self.screen)

        # Línea separadora con texto (más abajo)
        linea_y = 440
        pygame.draw.line(
            self.screen,
            (0, 200, 255),
            (self.ancho // 2 - 280, linea_y),
            (self.ancho // 2 + 280, linea_y),
            2,
        )

        # Texto de acceso rápido
        acceso_texto = self.font_info.render("Acceso rapido", True, (180, 200, 220))
        acceso_rect = acceso_texto.get_rect(center=(self.ancho // 2, linea_y - 18))
        self.screen.blit(acceso_texto, acceso_rect)

        # Botones de acceso rápido
        self.btn_lab1.dibujar(self.screen)
        self.btn_lab2.dibujar(self.screen)
        self.btn_lab3.dibujar(self.screen)
        self.btn_lab_ejemplo.dibujar(self.screen)

        # Información adicional con icono
        info = self.font_info.render(
            "Formato: .json | Rutas relativas desde: src/data/",
            True,
            (100, 120, 150),
        )
        info_rect = info.get_rect(center=(self.ancho // 2, self.alto - 35))
        self.screen.blit(info, info_rect)

        pygame.display.flip()

    def ejecutar(self):
        """
        Loop de la pantalla de carga.

        Returns:
            tuple: (laberinto, mensaje) si se cargó exitosamente, (None, None) si se canceló
        """
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return None, None

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return None, None

                # Manejar input de texto
                if self.input_ruta.manejar_evento(evento):
                    # Enter presionado, intentar cargar
                    ruta = self.input_ruta.obtener_texto()
                    if ruta:
                        ruta = resolver_ruta_laberinto(ruta)
                        laberinto, mensaje = self.admin.cargar_laberinto(ruta)
                        return laberinto, mensaje

                # Botón Cargar
                if self.btn_cargar.manejar_evento(evento, mouse_pos):
                    ruta = self.input_ruta.obtener_texto()
                    if ruta:
                        ruta = resolver_ruta_laberinto(ruta)
                        laberinto, mensaje = self.admin.cargar_laberinto(ruta)
                        return laberinto, mensaje

                # Botón Volver
                if self.btn_volver.manejar_evento(evento, mouse_pos):
                    return None, None

                # Botones de acceso rápido
                if self.btn_lab1.manejar_evento(evento, mouse_pos):
                    self.input_ruta.texto = "src/data/laberintos/laberinto1.json"

                if self.btn_lab2.manejar_evento(evento, mouse_pos):
                    self.input_ruta.texto = "src/data/laberintos/laberinto2.json"

                if self.btn_lab3.manejar_evento(evento, mouse_pos):
                    self.input_ruta.texto = "src/data/laberintos/laberinto3.json"

                if self.btn_lab_ejemplo.manejar_evento(evento, mouse_pos):
                    self.input_ruta.texto = "src/data/laberintos/laberinto_ejemplo.json"

            self.dibujar()
