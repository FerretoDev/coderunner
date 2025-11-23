"""
Pantalla para cargar archivos de laberinto.
"""

import pygame

from utilidades.helpers import resolver_ruta_laberinto

from interfaz.componentes.input_texto import Boton, InputTexto


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

        self.COLORES = {
            "fondo": (20, 20, 30),
            "texto": (255, 255, 255),
            "acento": (0, 150, 255),
        }

        self.font_titulo = pygame.font.Font(None, 52)
        self.font_texto = pygame.font.Font(None, 28)
        self.font_info = pygame.font.Font(None, 22)

        # Input para la ruta del archivo
        self.input_ruta = InputTexto(
            self.ancho // 2 - 300,
            220,
            600,
            50,
            "Ruta del archivo (ej: src/data/laberintos/laberinto1.json)",
        )

        # Botones
        self.btn_cargar = Boton(self.ancho // 2 - 200, 320, 190, 50, "Cargar")
        self.btn_volver = Boton(self.ancho // 2 + 10, 320, 190, 50, "Cancelar")

        # Botones de acceso rápido a archivos comunes (fila 1)
        self.btn_lab1 = Boton(
            self.ancho // 2 - 310, 410, 200, 40, "Laberinto 1 (Fácil)", accion="lab1"
        )
        self.btn_lab2 = Boton(
            self.ancho // 2 - 100, 410, 200, 40, "Laberinto 2 (Medio)", accion="lab2"
        )
        self.btn_lab3 = Boton(
            self.ancho // 2 + 110,
            410,
            200,
            40,
            "Laberinto 3 (Difícil)",
            accion="lab3",
        )

        # Botón de ejemplo (fila 2)
        self.btn_lab_ejemplo = Boton(
            self.ancho // 2 - 100,
            460,
            200,
            40,
            "Laberinto Ejemplo",
            accion="ejemplo",
        )

        self.archivo_seleccionado = None
        self.nombre_archivo = ""

    def dibujar(self):
        """Dibuja la pantalla de carga de laberinto."""
        self.screen.fill(self.COLORES["fondo"])

        # Título
        titulo = self.font_titulo.render(
            "Cargar Laberinto", True, self.COLORES["acento"]
        )
        titulo_rect = titulo.get_rect(center=(self.ancho // 2, 100))
        self.screen.blit(titulo, titulo_rect)

        # Instrucción
        instruccion = self.font_texto.render(
            "Ingresa la ruta del archivo:", True, (200, 200, 200)
        )
        instruccion_rect = instruccion.get_rect(center=(self.ancho // 2, 170))
        self.screen.blit(instruccion, instruccion_rect)

        # Input de ruta
        self.input_ruta.dibujar(self.screen)

        # Botones principales
        self.btn_cargar.dibujar(self.screen)
        self.btn_volver.dibujar(self.screen)

        # Línea separadora
        pygame.draw.line(
            self.screen,
            (80, 80, 100),
            (self.ancho // 2 - 320, 395),
            (self.ancho // 2 + 320, 395),
            2,
        )

        # Texto de acceso rápido
        acceso_texto = self.font_info.render(
            "Acceso rápido a laberintos:", True, (180, 180, 200)
        )
        acceso_rect = acceso_texto.get_rect(center=(self.ancho // 2, 385))
        self.screen.blit(acceso_texto, acceso_rect)

        # Botones de acceso rápido (fila 1)
        self.btn_lab1.dibujar(self.screen)
        self.btn_lab2.dibujar(self.screen)
        self.btn_lab3.dibujar(self.screen)

        # Botón de ejemplo (fila 2)
        self.btn_lab_ejemplo.dibujar(self.screen)

        # Información adicional
        info = self.font_info.render(
            "Formato: .json | Rutas relativas desde: src/data/",
            True,
            (120, 120, 140),
        )
        info_rect = info.get_rect(center=(self.ancho // 2, self.alto - 30))
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
