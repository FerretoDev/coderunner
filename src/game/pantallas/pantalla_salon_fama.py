"""
Pantalla del Salón de la Fama que muestra los mejores puntajes.
"""

import pygame

from ..componentes.input_texto import Boton


class PantallaSalonFama:
    """Muestra los mejores puntajes con un listado sencillo."""

    def __init__(self, screen, salon_fama):
        self.screen = screen
        self.ancho = screen.get_width()
        self.alto = screen.get_height()
        self.salon_fama = salon_fama

        # Fuentes
        self.font_titulo = pygame.font.Font(None, 56)
        self.font_header = pygame.font.Font(None, 28)
        self.font_data = pygame.font.Font(None, 24)
        self.font_info = pygame.font.Font(None, 20)
        self.font_stats = pygame.font.Font(None, 22)

        # Botones
        self.btn_volver = Boton(
            self.ancho // 2 - 220, self.alto - 80, 200, 50, "Volver"
        )

    def dibujar(self):
        """Dibuja título, encabezados, registros si hay, y el botón volver."""
        self.screen.fill((20, 20, 30))

        # Título con emoji de trofeo
        titulo = self.font_titulo.render("🏆 Salón de la Fama", True, (255, 215, 0))
        titulo_rect = titulo.get_rect(center=(self.ancho // 2, 40))
        self.screen.blit(titulo, titulo_rect)

        # Obtener registros y estadísticas
        registros = self.salon_fama.mostrar_mejores()
        stats = self.salon_fama.obtener_estadisticas()

        # Mostrar estadísticas generales
        y_stats = 90
        if registros:
            stats_texto = [
                f"Total de partidas: {stats['total_partidas']}",
                f"Mejor puntaje: {stats['mejor_puntaje']} pts",
                f"Promedio: {stats['promedio']:.1f} pts",
                f"Jugador destacado: {stats['jugador_top']}",
            ]
            for i, texto in enumerate(stats_texto):
                stat_surface = self.font_stats.render(texto, True, (180, 180, 200))
                stat_rect = stat_surface.get_rect(
                    center=(self.ancho // 2, y_stats + i * 22)
                )
                self.screen.blit(stat_surface, stat_rect)

        # Línea decorativa
        pygame.draw.line(
            self.screen,
            (0, 150, 255),
            (self.ancho // 2 - 300, 185),
            (self.ancho // 2 + 300, 185),
            2,
        )

        if not registros:
            texto_surface = self.font_header.render(
                "No hay registros todavía", True, (150, 150, 150)
            )
            texto_rect = texto_surface.get_rect(center=(self.ancho // 2, 300))
            self.screen.blit(texto_surface, texto_rect)

            # Mensaje de ayuda
            ayuda = self.font_info.render(
                "¡Juega una partida para empezar a competir!", True, (120, 120, 140)
            )
            ayuda_rect = ayuda.get_rect(center=(self.ancho // 2, 340))
            self.screen.blit(ayuda, ayuda_rect)
        else:
            # Encabezados de la tabla
            headers = ["#", "Jugador", "Puntaje", "Laberinto", "Fecha"]
            x_positions = [80, 140, 320, 430, 600]

            for header, x in zip(headers, x_positions, strict=True):
                texto_header = self.font_header.render(header, True, (150, 150, 150))
                self.screen.blit(texto_header, (x, 200))

            # Línea separadora
            pygame.draw.line(self.screen, (100, 100, 120), (60, 225), (740, 225), 2)

            # Mostrar hasta 10 registros
            for i, reg in enumerate(registros[:10]):
                y_pos = 240 + i * 30

                # Color especial para el podio (top 3)
                if i == 0:
                    color = (255, 215, 0)  # Oro
                    emoji = "🥇"
                elif i == 1:
                    color = (192, 192, 192)  # Plata
                    emoji = "🥈"
                elif i == 2:
                    color = (205, 127, 50)  # Bronce
                    emoji = "🥉"
                else:
                    color = (200, 200, 200)
                    emoji = f"{i + 1}"

                # Formatear fecha (solo mostrar fecha, no hora completa)
                fecha_str = reg.get("fecha", "N/A")
                if fecha_str != "N/A" and len(fecha_str) > 10:
                    fecha_str = fecha_str[:10]

                datos = [
                    emoji,
                    reg["nombre_jugador"][:12],
                    str(reg["puntaje"]),
                    reg["laberinto"][:15],
                    fecha_str,
                ]

                for dato, x in zip(datos, x_positions, strict=True):
                    texto_dato = self.font_data.render(dato, True, color)
                    self.screen.blit(texto_dato, (x, y_pos))

            # Footer con información adicional
            footer = self.font_info.render(
                f"Mostrando {min(len(registros), 10)} de {len(registros)} registros",
                True,
                (100, 100, 120),
            )
            footer_rect = footer.get_rect(center=(self.ancho // 2, 535))
            self.screen.blit(footer, footer_rect)

        # Botones
        self.btn_volver.dibujar(self.screen)

        pygame.display.flip()

    def ejecutar(self):
        """Loop de lectura: cierra con Volver, Escape o al cerrar ventana."""
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return

                if self.btn_volver.manejar_evento(evento, mouse_pos):
                    return

            self.dibujar()
