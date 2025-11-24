"""
Gestor centralizado de fuentes para evitar recreación innecesaria.

Singleton que mantiene todas las fuentes pre-creadas y listas para usar
en cualquier pantalla, mejorando el rendimiento y uso de memoria.
"""

from pathlib import Path

import pygame


class GestorFuentes:
    """
    Singleton que gestiona todas las fuentes del juego.

    Evita crear múltiples instancias de la misma fuente,
    lo cual es costoso en memoria y rendimiento.
    """

    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializado = False
        return cls._instancia

    def __init__(self):
        # Solo inicializar una vez
        if self._inicializado:
            return

        # Intentar cargar la fuente Press Start 2P descargada
        font_path = Path("src/assets/fonts/PressStart2P-Regular.ttf")
        usar_press_start = font_path.exists()

        if usar_press_start:
            # Fuentes para títulos (Press Start 2P)
            self.titulo_grande = pygame.font.Font(str(font_path), 48)
            self.titulo_normal = pygame.font.Font(str(font_path), 36)
            self.titulo_mediano = pygame.font.Font(str(font_path), 32)
            self.titulo_pequeño = pygame.font.Font(str(font_path), 28)
            self.titulo_mini = pygame.font.Font(str(font_path), 24)

            # Fuentes para texto normal (Press Start 2P)
            self.texto_grande = pygame.font.Font(str(font_path), 20)
            self.texto_normal = pygame.font.Font(str(font_path), 16)
            self.texto_pequeño = pygame.font.Font(str(font_path), 14)
            self.texto_mini = pygame.font.Font(str(font_path), 12)
            self.texto_info = pygame.font.Font(str(font_path), 10)

            # Fuentes específicas del juego (HUD)
            self.hud_titulo = pygame.font.Font(str(font_path), 28)
            self.hud_normal = pygame.font.Font(str(font_path), 18)
            self.hud_pequeño = pygame.font.Font(str(font_path), 14)

            # Fuente monoespaciada
            self.monoespaciada = pygame.font.Font(str(font_path), 16)

            self.fuente_pixel_nombre = "Press Start 2P (TTF)"

        else:
            # Fallback: Buscar fuentes pixel art en el sistema
            fuentes_pixel_preferidas = [
                "courier new",
                "courier",
                "mono",
                "monospace",
            ]

            fuente_pixel = None
            for nombre in fuentes_pixel_preferidas:
                try:
                    test = pygame.font.SysFont(nombre, 16)
                    if test:
                        fuente_pixel = nombre
                        break
                except:
                    continue

            if fuente_pixel:
                # Usar fuente del sistema
                self.titulo_grande = pygame.font.SysFont(fuente_pixel, 56, bold=True)
                self.titulo_normal = pygame.font.SysFont(fuente_pixel, 42, bold=True)
                self.titulo_mediano = pygame.font.SysFont(fuente_pixel, 36)
                self.titulo_pequeño = pygame.font.SysFont(fuente_pixel, 32)
                self.titulo_mini = pygame.font.SysFont(fuente_pixel, 28)

                self.texto_grande = pygame.font.SysFont(fuente_pixel, 24)
                self.texto_normal = pygame.font.SysFont(fuente_pixel, 20)
                self.texto_pequeño = pygame.font.SysFont(fuente_pixel, 16)
                self.texto_mini = pygame.font.SysFont(fuente_pixel, 14)
                self.texto_info = pygame.font.SysFont(fuente_pixel, 12)

                self.hud_titulo = pygame.font.SysFont(fuente_pixel, 32, bold=True)
                self.hud_normal = pygame.font.SysFont(fuente_pixel, 22)
                self.hud_pequeño = pygame.font.SysFont(fuente_pixel, 16)

                self.monoespaciada = pygame.font.SysFont(fuente_pixel, 18)

                self.fuente_pixel_nombre = f"{fuente_pixel} (Sistema)"
            else:
                # Último fallback: fuente default de pygame
                self.titulo_grande = pygame.font.Font(None, 72)
                self.titulo_normal = pygame.font.Font(None, 56)
                self.titulo_mediano = pygame.font.Font(None, 52)
                self.titulo_pequeño = pygame.font.Font(None, 48)
                self.titulo_mini = pygame.font.Font(None, 44)

                self.texto_grande = pygame.font.Font(None, 32)
                self.texto_normal = pygame.font.Font(None, 28)
                self.texto_pequeño = pygame.font.Font(None, 24)
                self.texto_mini = pygame.font.Font(None, 22)
                self.texto_info = pygame.font.Font(None, 20)

                self.hud_titulo = pygame.font.Font(None, 48)
                self.hud_normal = pygame.font.Font(None, 32)
                self.hud_pequeño = pygame.font.Font(None, 24)

                self.monoespaciada = pygame.font.Font(None, 24)

                self.fuente_pixel_nombre = "Default (pygame.font.Font)"

        self._inicializado = True

    def render_pixel(self, fuente, texto, color):
        """
        Renderiza texto con estilo pixel art (sin antialiasing).

        Args:
            fuente: Objeto Font a usar
            texto: Texto a renderizar
            color: Color del texto (tuple RGB)

        Returns:
            Surface con el texto renderizado
        """
        return fuente.render(texto, False, color)  # False = sin antialiasing

    @classmethod
    def obtener(cls):
        """Método alternativo para obtener la instancia."""
        return cls()

    def renderizar_texto(self, texto, fuente_nombre, color, antialias=True):
        """
        Renderiza texto usando una fuente del gestor.

        Args:
            texto: Texto a renderizar
            fuente_nombre: Nombre del atributo de fuente ('titulo_grande', 'texto_normal', etc.)
            color: Color del texto (tuple RGB)
            antialias: Si usar antialiasing (default True)

        Returns:
            Surface con el texto renderizado
        """
        fuente = getattr(self, fuente_nombre, self.texto_normal)
        return fuente.render(texto, antialias, color)
