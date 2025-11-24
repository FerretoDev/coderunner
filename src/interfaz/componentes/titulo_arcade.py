"""
Componente de título estilo arcade con efectos pixel art.

Crea títulos con sombras múltiples, brillos y efectos retro.
"""

import pygame
from interfaz.gestor_fuentes import GestorFuentes
from config.colores import PaletaColores


class TituloArcade:
    """Título con efectos de sombra triple estilo arcade retro."""

    def __init__(self, texto, y, estilo="grande"):
        """
        Crea un título arcade con efectos visuales.

        Args:
            texto: Texto del título
            y: Posición vertical
            estilo: 'grande', 'mediano', o 'pequeño'
        """
        self.texto = texto
        self.y = y
        self.estilo = estilo

        fuentes = GestorFuentes()
        if estilo == "grande":
            self.font = fuentes.titulo_grande
        elif estilo == "mediano":
            self.font = fuentes.titulo_normal
        else:
            self.font = fuentes.texto_grande

        # Colores para el efecto de sombra triple
        self.COLOR_SOMBRA_1 = PaletaColores.PIXEL_SOMBRA
        self.COLOR_SOMBRA_2 = PaletaColores.ACENTO_PRINCIPAL
        self.COLOR_PRINCIPAL = PaletaColores.ORO

    def dibujar(self, screen):
        """Dibuja el título con efectos de sombra triple."""
        ancho_pantalla = screen.get_width()

        # Sombra oscura (más alejada)
        sombra2 = self.font.render(self.texto, False, self.COLOR_SOMBRA_1)
        rect_sombra2 = sombra2.get_rect(center=(ancho_pantalla // 2 + 4, self.y + 4))
        screen.blit(sombra2, rect_sombra2)

        # Sombra cyan (intermedia)
        sombra1 = self.font.render(self.texto, False, self.COLOR_SOMBRA_2)
        rect_sombra1 = sombra1.get_rect(center=(ancho_pantalla // 2 + 2, self.y + 2))
        screen.blit(sombra1, rect_sombra1)

        # Texto principal (dorado)
        titulo = self.font.render(self.texto, False, self.COLOR_PRINCIPAL)
        rect_titulo = titulo.get_rect(center=(ancho_pantalla // 2, self.y))
        screen.blit(titulo, rect_titulo)


class SubtituloArcade:
    """Subtítulo sencillo centrado."""

    def __init__(self, texto, y, color=None):
        """
        Crea un subtítulo centrado.

        Args:
            texto: Texto del subtítulo
            y: Posición vertical
            color: Color del texto (None = ACENTO_INFO)
        """
        self.texto = texto
        self.y = y
        self.color = color or PaletaColores.ACENTO_INFO

        fuentes = GestorFuentes()
        self.font = fuentes.texto_normal

    def dibujar(self, screen):
        """Dibuja el subtítulo centrado."""
        ancho_pantalla = screen.get_width()
        subtitulo = self.font.render(self.texto, False, self.color)
        rect_subtitulo = subtitulo.get_rect(center=(ancho_pantalla // 2, self.y))
        screen.blit(subtitulo, rect_subtitulo)


class LineaDecorativa:
    """Línea decorativa horizontal con colores arcade."""

    def __init__(self, y, ancho_porcentaje=50, doble=True):
        """
        Crea una línea decorativa.

        Args:
            y: Posición vertical
            ancho_porcentaje: Porcentaje del ancho de pantalla (1-100)
            doble: Si True, dibuja dos líneas de colores diferentes
        """
        self.y = y
        self.ancho_porcentaje = ancho_porcentaje / 100
        self.doble = doble

        self.COLOR_1 = PaletaColores.ACENTO_PRINCIPAL
        self.COLOR_2 = PaletaColores.ACENTO_SUCCESS

    def dibujar(self, screen):
        """Dibuja la línea decorativa."""
        ancho_pantalla = screen.get_width()
        ancho_linea = int(ancho_pantalla * self.ancho_porcentaje)
        x_inicio = (ancho_pantalla - ancho_linea) // 2
        x_fin = x_inicio + ancho_linea

        if self.doble:
            # Línea cyan (arriba)
            pygame.draw.line(
                screen, self.COLOR_1, (x_inicio, self.y - 2), (x_fin, self.y - 2), 2
            )
            # Línea verde (abajo)
            pygame.draw.line(
                screen, self.COLOR_2, (x_inicio, self.y + 2), (x_fin, self.y + 2), 2
            )
        else:
            # Línea simple
            pygame.draw.line(
                screen, self.COLOR_1, (x_inicio, self.y), (x_fin, self.y), 3
            )


class FooterArcade:
    """Footer con iconos y texto en la parte inferior."""

    def __init__(self, texto, icono=""):
        """
        Crea un footer arcade.

        Args:
            texto: Texto del footer
            icono: Emoji o símbolo opcional
        """
        self.texto_completo = f"{icono} {texto}" if icono else texto

        fuentes = GestorFuentes()
        self.font = fuentes.texto_info
        self.color = PaletaColores.ACENTO_INFO

    def dibujar(self, screen):
        """Dibuja el footer en la parte inferior."""
        ancho_pantalla = screen.get_width()
        alto_pantalla = screen.get_height()

        footer = self.font.render(self.texto_completo, False, self.color)
        rect_footer = footer.get_rect(center=(ancho_pantalla // 2, alto_pantalla - 30))
        screen.blit(footer, rect_footer)
