"""
Sistema de barra de vida pixel art.
Basado en: The Legend of Zelda (corazones), Dead Cells (barra segmentada).
"""

import pygame
from interfaz.paleta_ui import PaletaUI


class BarraVida:
    """
    Barra de vida con dos estilos:
    - 'corazones': Sistema de corazones estilo Zelda
    - 'segmentada': Barra con segmentos estilo Dead Cells
    """

    def __init__(self, x, y, max_vida, estilo="segmentada"):
        """
        Inicializa la barra de vida.

        Args:
            x: Posición X
            y: Posición Y
            max_vida: Vida máxima
            estilo: 'corazones' o 'segmentada'
        """
        self.x = x
        self.y = y
        self.max_vida = max_vida
        self.vida_actual = max_vida
        self.estilo = estilo

        # Configuración según estilo
        if estilo == "corazones":
            self.tamaño_corazon = 16
            self.espaciado = 2
            self.max_corazones = 10
            self.width = (
                self.max_corazones * self.tamaño_corazon
                + (self.max_corazones - 1) * self.espaciado
            )
            self.height = self.tamaño_corazon
        else:  # segmentada
            self.width = 160
            self.height = 12
            self.num_segmentos = 20
            self.ancho_segmento = (
                self.width - (self.num_segmentos + 1)
            ) // self.num_segmentos

    def actualizar(self, vida_actual):
        """
        Actualiza la vida actual.

        Args:
            vida_actual: Nueva cantidad de vida
        """
        self.vida_actual = max(0, min(vida_actual, self.max_vida))

    def dibujar(self, surface):
        """
        Dibuja la barra de vida.

        Args:
            surface: pygame.Surface donde dibujar
        """
        if self.estilo == "corazones":
            self._dibujar_corazones(surface)
        else:
            self._dibujar_segmentada(surface)

    def _dibujar_corazones(self, surface):
        """Dibuja sistema de corazones estilo Zelda."""
        corazones_totales = self.max_vida / 2  # Cada corazón = 2 puntos de vida
        corazones_llenos = int(self.vida_actual / 2)
        medio_corazon = (self.vida_actual % 2) == 1

        for i in range(int(corazones_totales)):
            x = self.x + i * (self.tamaño_corazon + self.espaciado)
            y = self.y

            if i < corazones_llenos:
                # Corazón lleno
                self._dibujar_corazon(surface, x, y, "lleno")
            elif i == corazones_llenos and medio_corazon:
                # Medio corazón
                self._dibujar_corazon(surface, x, y, "medio")
            else:
                # Corazón vacío
                self._dibujar_corazon(surface, x, y, "vacio")

    def _dibujar_corazon(self, surface, x, y, estado):
        """
        Dibuja un corazón pixel art.

        Args:
            surface: Superficie donde dibujar
            x, y: Posición
            estado: 'lleno', 'medio', 'vacio'
        """
        tamaño = self.tamaño_corazon

        # Colores según estado
        if estado == "lleno":
            color_principal = PaletaUI.RED
            color_sombra = PaletaUI.RED_DARK
        elif estado == "medio":
            color_principal = PaletaUI.GOLD
            color_sombra = PaletaUI.GOLD_DARK
        else:  # vacio
            color_principal = None
            color_sombra = PaletaUI.GRAY

        # Dibujar forma de corazón simplificada (rectángulos)
        # Parte superior (2 lóbulos)
        if color_principal:
            pygame.draw.rect(
                surface, color_principal, (x + 2, y + 2, tamaño // 3, tamaño // 3)
            )
            pygame.draw.rect(
                surface,
                color_principal,
                (x + 2 + tamaño // 2, y + 2, tamaño // 3, tamaño // 3),
            )

        # Parte central (cuerpo del corazón)
        if color_principal:
            pygame.draw.rect(
                surface, color_principal, (x + 2, y + 6, tamaño - 4, tamaño // 2)
            )

        # Parte inferior (punta)
        if color_principal:
            for i in range(tamaño // 4):
                pygame.draw.rect(
                    surface,
                    color_principal,
                    (
                        x + 2 + i * 2,
                        y + 10 + i * 2,
                        tamaño - 4 - i * 4,
                        2,
                    ),
                )

        # Contorno (siempre visible)
        pygame.draw.rect(surface, color_sombra, (x, y, tamaño, tamaño), 1)

    def _dibujar_segmentada(self, surface):
        """Dibuja barra segmentada estilo Dead Cells."""
        # Calcular cuántos segmentos están llenos
        porcentaje = self.vida_actual / self.max_vida
        segmentos_llenos = int(self.num_segmentos * porcentaje)

        # Fondo de la barra
        rect_fondo = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, PaletaUI.DARK, rect_fondo)

        # Dibujar segmentos
        for i in range(self.num_segmentos):
            x_seg = self.x + 2 + i * (self.ancho_segmento + 1)
            y_seg = self.y + 2
            rect_seg = pygame.Rect(x_seg, y_seg, self.ancho_segmento, self.height - 4)

            if i < segmentos_llenos:
                # Segmento lleno con color según vida
                color = PaletaUI.obtener_color_vida(porcentaje)
                pygame.draw.rect(surface, color, rect_seg)
            else:
                # Segmento vacío
                pygame.draw.rect(surface, PaletaUI.GRAY, rect_seg)

        # Borde exterior
        pygame.draw.rect(surface, PaletaUI.WHITE, rect_fondo, 1)
