"""
Clase base abstracta para pantallas del juego.

Proporciona funcionalidad común para reducir código duplicado:
- Loop principal estandarizado
- Manejo básico de eventos
- Métodos de dibujo comunes
"""

import pygame
from abc import ABC, abstractmethod
from interfaz.gestor_fuentes import GestorFuentes


class PantallaBase(ABC):
    """
    Clase base abstracta para todas las pantallas del juego.

    Implementa el patrón Template Method para el loop principal
    y proporciona métodos helper comunes.
    """

    def __init__(self, screen):
        self.screen = screen
        self.ancho = screen.get_width()
        self.alto = screen.get_height()

        # Fuentes comunes desde GestorFuentes
        fuentes = GestorFuentes()
        self.font_titulo = fuentes.titulo_normal
        self.font_subtitulo = fuentes.titulo_pequeño
        self.font_texto = fuentes.texto_normal
        self.font_info = fuentes.texto_pequeño

        # Colores comunes
        self.COLORES = {
            "fondo": (20, 20, 30),
            "texto": (255, 255, 255),
            "texto_secundario": (200, 200, 200),
            "acento": (0, 150, 255),
            "info": (100, 100, 120),
        }

    @abstractmethod
    def dibujar(self):
        """Método abstracto para dibujar la pantalla. Debe ser implementado por subclases."""
        pass

    @abstractmethod
    def manejar_evento_especifico(self, evento, mouse_pos):
        """
        Método abstracto para manejar eventos específicos de la pantalla.

        Args:
            evento: Evento de pygame
            mouse_pos: Tupla con la posición del mouse

        Returns:
            Objeto resultado si la pantalla debe cerrarse, None para continuar
        """
        pass

    def ejecutar(self, fps=60):
        """
        Loop principal estandarizado para todas las pantallas.

        Args:
            fps: Frames por segundo (default 60)

        Returns:
            Resultado devuelto por manejar_evento_especifico o None
        """
        clock = pygame.time.Clock()

        while True:
            clock.tick(fps)
            mouse_pos = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                # Manejo común de eventos
                if evento.type == pygame.QUIT:
                    return self.manejar_cierre()

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return self.manejar_escape()

                # Delegar eventos específicos a la subclase
                resultado = self.manejar_evento_especifico(evento, mouse_pos)
                if resultado is not None:
                    return resultado

            self.dibujar()

    def manejar_cierre(self):
        """Maneja el cierre de la ventana. Puede ser sobrescrito."""
        return None

    def manejar_escape(self):
        """Maneja la tecla Escape. Puede ser sobrescrito."""
        return None

    def dibujar_fondo(self, color=None):
        """Dibuja el fondo de la pantalla."""
        color = color or self.COLORES["fondo"]
        self.screen.fill(color)

    def dibujar_titulo(self, texto, y=100, color=None):
        """
        Dibuja un título centrado con sombra.

        Args:
            texto: Texto del título
            y: Posición vertical
            color: Color del texto (default blanco)
        """
        color = color or self.COLORES["texto"]

        # Sombra
        sombra = self.font_titulo.render(texto, True, (10, 10, 20))
        sombra_rect = sombra.get_rect(center=(self.ancho // 2 + 3, y + 3))
        self.screen.blit(sombra, sombra_rect)

        # Título
        titulo = self.font_titulo.render(texto, True, color)
        titulo_rect = titulo.get_rect(center=(self.ancho // 2, y))
        self.screen.blit(titulo, titulo_rect)

    def dibujar_texto_centrado(self, texto, y, fuente=None, color=None):
        """
        Dibuja texto centrado horizontalmente.

        Args:
            texto: Texto a dibujar
            y: Posición vertical
            fuente: Font de pygame (default font_texto)
            color: Color del texto
        """
        fuente = fuente or self.font_texto
        color = color or self.COLORES["texto"]

        superficie = fuente.render(texto, True, color)
        rect = superficie.get_rect(center=(self.ancho // 2, y))
        self.screen.blit(superficie, rect)

    def dibujar_footer(self, texto, color=None):
        """
        Dibuja un footer en la parte inferior de la pantalla.

        Args:
            texto: Texto del footer
            color: Color del texto
        """
        color = color or self.COLORES["info"]
        footer = self.font_info.render(texto, True, color)
        footer_rect = footer.get_rect(center=(self.ancho // 2, self.alto - 30))
        self.screen.blit(footer, footer_rect)

    def dibujar_linea_horizontal(self, y, longitud=300, color=None):
        """
        Dibuja una línea horizontal centrada.

        Args:
            y: Posición vertical
            longitud: Longitud de la línea
            color: Color de la línea
        """
        color = color or self.COLORES["acento"]
        x_inicio = (self.ancho - longitud) // 2
        x_fin = x_inicio + longitud
        pygame.draw.line(self.screen, color, (x_inicio, y), (x_fin, y), 3)

    def actualizar_pantalla(self):
        """Actualiza la pantalla después de dibujar."""
        pygame.display.flip()
