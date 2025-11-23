"""
Componente de botón adaptable que ajusta su tamaño según el contenido.

Este botón calcula automáticamente su ancho basándose en el texto
para evitar que se corte en fuentes pixel art como Press Start 2P.
"""

import pygame
from interfaz.gestor_fuentes import GestorFuentes


class BotonAdaptable:
    """
    Botón que ajusta automáticamente su ancho según el texto.

    Perfecto para fuentes pixel art donde el texto puede variar en longitud.
    """

    def __init__(
        self,
        x,
        y,
        texto,
        accion=None,
        padding_horizontal=30,
        padding_vertical=15,
        ancho_minimo=120,
        ancho_maximo=None,
        alto_fijo=None,
    ):
        """
        Crea un botón que se adapta al tamaño del texto.

        Args:
            x: Posición X del botón
            y: Posición Y del botón
            texto: Texto a mostrar en el botón
            accion: Identificador de acción (puede ser int, str, etc.)
            padding_horizontal: Espacio horizontal extra alrededor del texto
            padding_vertical: Espacio vertical extra alrededor del texto
            ancho_minimo: Ancho mínimo del botón
            ancho_maximo: Ancho máximo del botón (None = sin límite)
            alto_fijo: Alto fijo del botón (None = se calcula automáticamente)
        """
        self.texto = texto
        self.accion = accion
        self.padding_horizontal = padding_horizontal
        self.padding_vertical = padding_vertical
        self.ancho_minimo = ancho_minimo
        self.ancho_maximo = ancho_maximo
        self.alto_fijo = alto_fijo

        # Estado del botón
        self.hover = False
        self.presionado = False

        # Fuente y colores
        fuentes = GestorFuentes()
        self.font = fuentes.texto_pequeño

        # Colores estilo arcade vibrante
        self.COLOR_NORMAL = (50, 60, 100)
        self.COLOR_HOVER = (70, 90, 140)
        self.COLOR_PRESIONADO = (30, 40, 70)
        self.COLOR_TEXTO = (255, 255, 255)
        self.COLOR_TEXTO_HOVER = (255, 220, 60)
        self.COLOR_BORDE = (80, 100, 160)
        self.COLOR_BORDE_HOVER = (0, 200, 255)

        # Calcular tamaño del botón basado en el texto
        self._calcular_dimensiones()

        # Posicionar el botón
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)

    def _calcular_dimensiones(self):
        """Calcula el ancho y alto óptimos para el texto."""
        # Renderizar el texto para obtener sus dimensiones
        texto_surface = self.font.render(self.texto, False, self.COLOR_TEXTO)
        ancho_texto = texto_surface.get_width()
        alto_texto = texto_surface.get_height()

        # Calcular ancho con padding
        self.ancho = ancho_texto + (self.padding_horizontal * 2)

        # Aplicar límites de ancho
        if self.ancho < self.ancho_minimo:
            self.ancho = self.ancho_minimo
        if self.ancho_maximo and self.ancho > self.ancho_maximo:
            self.ancho = self.ancho_maximo

        # Calcular alto
        if self.alto_fijo:
            self.alto = self.alto_fijo
        else:
            self.alto = alto_texto + (self.padding_vertical * 2)

    def cambiar_texto(self, nuevo_texto):
        """Cambia el texto del botón y recalcula dimensiones."""
        self.texto = nuevo_texto
        x_actual = self.rect.x
        y_actual = self.rect.y
        self._calcular_dimensiones()
        self.rect = pygame.Rect(x_actual, y_actual, self.ancho, self.alto)

    def centrar_horizontalmente(self, ancho_pantalla):
        """Centra el botón horizontalmente en la pantalla."""
        self.rect.x = (ancho_pantalla - self.ancho) // 2

    def manejar_evento(self, evento, mouse_pos):
        """Maneja eventos del mouse."""
        self.hover = self.rect.collidepoint(mouse_pos)

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.hover:
                self.presionado = True
                return True

        if evento.type == pygame.MOUSEBUTTONUP:
            self.presionado = False

        return False

    def dibujar(self, screen):
        """Dibuja el botón con efectos pixel art."""
        # Color de fondo según estado
        if self.presionado:
            color_fondo = self.COLOR_PRESIONADO
        elif self.hover:
            color_fondo = self.COLOR_HOVER
        else:
            color_fondo = self.COLOR_NORMAL

        color_borde = self.COLOR_BORDE_HOVER if self.hover else self.COLOR_BORDE
        color_texto = self.COLOR_TEXTO_HOVER if self.hover else self.COLOR_TEXTO

        # Dibujar fondo del botón
        pygame.draw.rect(screen, color_fondo, self.rect)
        pygame.draw.rect(screen, color_borde, self.rect, 2)

        # Efecto 3D pixel art en hover
        if self.hover and not self.presionado:
            # Líneas de luz (arriba e izquierda)
            color_luz = tuple(min(255, c + 40) for c in color_fondo)
            pygame.draw.line(
                screen,
                color_luz,
                (self.rect.left, self.rect.top),
                (self.rect.right - 1, self.rect.top),
                2,
            )
            pygame.draw.line(
                screen,
                color_luz,
                (self.rect.left, self.rect.top),
                (self.rect.left, self.rect.bottom - 1),
                2,
            )

            # Líneas de sombra (abajo y derecha)
            color_sombra = tuple(max(0, c - 20) for c in color_fondo)
            pygame.draw.line(
                screen,
                color_sombra,
                (self.rect.left + 1, self.rect.bottom - 1),
                (self.rect.right - 1, self.rect.bottom - 1),
                2,
            )
            pygame.draw.line(
                screen,
                color_sombra,
                (self.rect.right - 1, self.rect.top + 1),
                (self.rect.right - 1, self.rect.bottom - 1),
                2,
            )

        # Dibujar texto centrado
        texto_surface = self.font.render(self.texto, False, color_texto)
        texto_rect = texto_surface.get_rect(center=self.rect.center)

        # Efecto de presionado (texto se mueve un pixel)
        if self.presionado:
            texto_rect.y += 1

        screen.blit(texto_surface, texto_rect)


class BotonGrande(BotonAdaptable):
    """Botón grande para títulos y acciones principales."""

    def __init__(self, x, y, texto, accion=None):
        fuentes = GestorFuentes()
        self.font = fuentes.texto_normal  # Fuente más grande
        super().__init__(
            x,
            y,
            texto,
            accion,
            padding_horizontal=40,
            padding_vertical=20,
            ancho_minimo=180,
            alto_fijo=60,
        )


class BotonPequeño(BotonAdaptable):
    """Botón pequeño para acciones secundarias."""

    def __init__(self, x, y, texto, accion=None):
        fuentes = GestorFuentes()
        self.font = fuentes.texto_info  # Fuente más pequeña
        super().__init__(
            x,
            y,
            texto,
            accion,
            padding_horizontal=20,
            padding_vertical=10,
            ancho_minimo=100,
            alto_fijo=40,
        )
