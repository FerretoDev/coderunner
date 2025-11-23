"""
Menú de opciones administrativas.
"""

import pygame

from ..componentes.input_texto import Boton


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

        self.font_titulo = pygame.font.Font(None, 60)
        self.font_subtitulo = pygame.font.Font(None, 28)

        # Crear botones verticales
        self._crear_botones()

    def _crear_botones(self):
        """Crea los botones del menú administrativo."""
        ancho_boton = 400
        alto_boton = 60
        x = (self.ancho - ancho_boton) // 2
        y_inicial = 250
        espacio = 20

        self.botones = []
        textos_acciones = [
            ("📁 Cargar Laberinto", 1),
            ("🗑️ Reiniciar Salón de Fama", 2),
            ("⬅️ Volver al Menú", 3),
        ]

        for i, (texto, accion) in enumerate(textos_acciones):
            y = y_inicial + (alto_boton + espacio) * i
            self.botones.append(
                Boton(x, y, ancho_boton, alto_boton, texto, accion=accion)
            )

    def dibujar(self):
        """Dibuja la pantalla del menú administrativo."""
        self.screen.fill(self.COLORES["fondo"])

        # Título
        titulo = self.font_titulo.render(
            "⚙️ Panel de Administración", True, self.COLORES["acento"]
        )
        titulo_rect = titulo.get_rect(center=(self.ancho // 2, 120))
        self.screen.blit(titulo, titulo_rect)

        # Subtítulo
        subtitulo = self.font_subtitulo.render(
            "Selecciona una opción:", True, self.COLORES["texto"]
        )
        subtitulo_rect = subtitulo.get_rect(center=(self.ancho // 2, 180))
        self.screen.blit(subtitulo, subtitulo_rect)

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
