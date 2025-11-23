"""
Panel decorativo estilo pixel art.
Basado en: Shovel Knight (marcos decorados), Hyper Light Drifter (translúcidos).
"""

import pygame
from interfaz.paleta_ui import PaletaUI


class Panel:
    """
    Panel/marco decorativo estilo retro.

    Tipos disponibles:
    - 'gba': Caja de diálogo estilo GBA (Zelda Minish Cap)
    - 'translucido': Panel semi-transparente (Hyper Light Drifter)
    - 'decorado': Marco dorado con esquinas (Shovel Knight)
    - 'simple': Panel básico sin decoración
    """

    def __init__(self, x, y, width, height, tipo="simple", color_fondo=None, alpha=255):
        """
        Inicializa el panel.

        Args:
            x: Posición X
            y: Posición Y
            width: Ancho
            height: Alto
            tipo: Tipo de panel ('gba', 'translucido', 'decorado', 'simple')
            color_fondo: Color de fondo personalizado (opcional)
            alpha: Transparencia 0-255
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.tipo = tipo
        self.alpha = alpha

        # Color de fondo según tipo
        if color_fondo:
            self.color_fondo = color_fondo
        else:
            self.color_fondo = self._obtener_color_fondo_defecto()

        # Crear surface con alpha si es necesario
        if alpha < 255:
            self.surface = pygame.Surface(
                (width, height), pygame.SRCALPHA
            ).convert_alpha()
        else:
            self.surface = pygame.Surface((width, height)).convert()

    def _obtener_color_fondo_defecto(self):
        """Retorna el color de fondo según el tipo."""
        colores = {
            "gba": PaletaUI.DARK,
            "translucido": PaletaUI.DARK,
            "decorado": PaletaUI.BLUE,
            "simple": PaletaUI.DARK,
        }
        return colores.get(self.tipo, PaletaUI.DARK)

    def dibujar(self, surface):
        """
        Dibuja el panel en la superficie.

        Args:
            surface: pygame.Surface donde dibujar
        """
        # Limpiar surface
        self.surface.fill((*self.color_fondo, self.alpha))

        if self.tipo == "gba":
            self._dibujar_estilo_gba()
        elif self.tipo == "translucido":
            self._dibujar_estilo_translucido()
        elif self.tipo == "decorado":
            self._dibujar_estilo_decorado()
        else:  # simple
            self._dibujar_estilo_simple()

        # Blit en la superficie principal
        surface.blit(self.surface, self.rect)

    def _dibujar_estilo_simple(self):
        """Dibuja panel simple con borde."""
        w, h = self.surface.get_size()

        # Borde exterior blanco
        pygame.draw.rect(self.surface, PaletaUI.LIGHT, (0, 0, w, h), 2)

    def _dibujar_estilo_gba(self):
        """Dibuja panel estilo GBA (Zelda Minish Cap)."""
        w, h = self.surface.get_size()

        # Borde exterior blanco (2px)
        pygame.draw.rect(self.surface, PaletaUI.WHITE, (0, 0, w, h), 2)

        # Borde interior azul (1px)
        pygame.draw.rect(self.surface, PaletaUI.BLUE, (2, 2, w - 4, h - 4), 1)

        # Esquinas decorativas doradas (triángulos pequeños 4x4)
        self._dibujar_esquina_decorada(4, 4, "superior_izquierda")
        self._dibujar_esquina_decorada(w - 8, 4, "superior_derecha")
        self._dibujar_esquina_decorada(4, h - 8, "inferior_izquierda")
        self._dibujar_esquina_decorada(w - 8, h - 8, "inferior_derecha")

    def _dibujar_estilo_translucido(self):
        """Dibuja panel translúcido (Hyper Light Drifter)."""
        w, h = self.surface.get_size()

        # Borde exterior azul neón (2px)
        pygame.draw.rect(self.surface, PaletaUI.BLUE_LIGHT, (0, 0, w, h), 2)

        # Borde interior azul oscuro (1px)
        pygame.draw.rect(self.surface, PaletaUI.BLUE, (2, 2, w - 4, h - 4), 1)

    def _dibujar_estilo_decorado(self):
        """Dibuja panel decorado estilo Shovel Knight."""
        w, h = self.surface.get_size()

        # Marco dorado grueso (4px)
        pygame.draw.rect(self.surface, PaletaUI.GOLD, (0, 0, w, h), 4)

        # Sombra del marco (offset diagonal)
        pygame.draw.line(
            self.surface, PaletaUI.GOLD_DARK, (4, h - 1), (w - 1, h - 1), 2
        )
        pygame.draw.line(
            self.surface, PaletaUI.GOLD_DARK, (w - 1, 4), (w - 1, h - 1), 2
        )

        # Esquinas decorativas más elaboradas
        tamaño_esquina = 8
        self._dibujar_esquina_decorada(
            4, 4, "superior_izquierda", tamaño=tamaño_esquina
        )
        self._dibujar_esquina_decorada(
            w - 4 - tamaño_esquina, 4, "superior_derecha", tamaño=tamaño_esquina
        )
        self._dibujar_esquina_decorada(
            4, h - 4 - tamaño_esquina, "inferior_izquierda", tamaño=tamaño_esquina
        )
        self._dibujar_esquina_decorada(
            w - 4 - tamaño_esquina,
            h - 4 - tamaño_esquina,
            "inferior_derecha",
            tamaño=tamaño_esquina,
        )

    def _dibujar_esquina_decorada(self, x, y, posicion, tamaño=4):
        """
        Dibuja una esquina decorativa.

        Args:
            x: Posición X
            y: Posición Y
            posicion: 'superior_izquierda', 'superior_derecha', etc.
            tamaño: Tamaño de la decoración
        """
        color = PaletaUI.GOLD

        # Triángulo simple en la esquina
        if posicion == "superior_izquierda":
            points = [(x, y), (x + tamaño, y), (x, y + tamaño)]
        elif posicion == "superior_derecha":
            points = [(x + tamaño, y), (x, y), (x + tamaño, y + tamaño)]
        elif posicion == "inferior_izquierda":
            points = [(x, y + tamaño), (x + tamaño, y + tamaño), (x, y)]
        else:  # inferior_derecha
            points = [
                (x + tamaño, y + tamaño),
                (x, y + tamaño),
                (x + tamaño, y),
            ]

        pygame.draw.polygon(self.surface, color, points)
