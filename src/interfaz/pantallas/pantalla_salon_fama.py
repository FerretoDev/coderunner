"""
Pantalla del Salón de la Fama que muestra los mejores puntajes.
"""

import pygame

from config.colores import PaletaColores
from interfaz.componentes.boton_adaptable import BotonGrande
from interfaz.componentes.titulo_arcade import LineaDecorativa, TituloArcade
from interfaz.gestor_fuentes import GestorFuentes


class PantallaSalonFama:
    """Muestra los mejores puntajes con un listado sencillo."""

    def __init__(self, screen, salon_fama):
        self.screen = screen
        self.ancho = screen.get_width()
        self.alto = screen.get_height()
        self.salon_fama = salon_fama

        # Usar gestor de fuentes compartido
        fuentes = GestorFuentes()
        self.font_header = fuentes.texto_normal
        self.font_data = fuentes.texto_pequeño
        self.font_info = fuentes.texto_info
        self.font_stats = fuentes.texto_mini
        self.font_podio = fuentes.texto_grande

        # Componentes arcade
        self.titulo = TituloArcade("SALÓN DE LA FAMA", 35, "mediano")
        self.linea_decorativa = LineaDecorativa(90, ancho_porcentaje=60, doble=True)

        # Botón volver (se posicionará dinámicamente en dibujar())
        self.btn_volver = BotonGrande(0, 0, "Volver", accion="volver")

    def dibujar(self):
        """Dibuja título, podio, tabla de récords y botón volver con estética arcade."""
        self.screen.fill(PaletaColores.FONDO_PRINCIPAL)

        # Título con efectos arcade
        self.titulo.dibujar(self.screen)
        self.linea_decorativa.dibujar(self.screen)

        # Obtener registros y estadísticas
        registros = self.salon_fama.mostrar_mejores()
        stats = self.salon_fama.obtener_estadisticas()

        # Variable para rastrear la última posición Y usada
        ultima_y = 150

        if not registros:
            # Mensaje cuando no hay registros
            y_center = self.alto // 2 - 50
            texto_surface = self.font_header.render(
                "No hay registros todavía", False, PaletaColores.ACENTO_INFO
            )
            texto_rect = texto_surface.get_rect(center=(self.ancho // 2, y_center))
            self.screen.blit(texto_surface, texto_rect)

            ayuda = self.font_info.render(
                "¡Juega una partida para empezar a competir!", False, (150, 150, 170)
            )
            ayuda_rect = ayuda.get_rect(center=(self.ancho // 2, y_center + 40))
            self.screen.blit(ayuda, ayuda_rect)
            ultima_y = y_center + 60
        else:
            # Estadísticas generales en tarjetas
            self._dibujar_estadisticas(stats)
            ultima_y = 145

            # Podio (Top 3) con tarjetas destacadas
            self._dibujar_podio(registros[:3])
            ultima_y = 265  # Fin del podio

            # Tabla con el resto de registros
            if len(registros) > 3:
                ultima_y = self._dibujar_tabla(registros[3:10])

        # Posicionar botón volver con espacio suficiente
        y_boton = max(ultima_y + 30, self.alto - 90)
        self.btn_volver.rect.y = y_boton
        self.btn_volver.centrar_horizontalmente(self.ancho)

        # Botón volver
        self.btn_volver.dibujar(self.screen)
        pygame.display.flip()

    def _dibujar_estadisticas(self, stats):
        """Dibuja las estadísticas generales en formato compacto."""
        y_stats = 120
        stats_texto = [
            f"Partidas: {stats['total_partidas']}",
            f"Mejor: {stats['mejor_puntaje']} pts",
            f"Promedio: {stats['promedio']:.1f} pts",
        ]
        x_spacing = self.ancho // 4
        for i, texto in enumerate(stats_texto):
            stat_surface = self.font_stats.render(
                texto, False, PaletaColores.ACENTO_INFO
            )
            stat_rect = stat_surface.get_rect(center=(x_spacing * (i + 1), y_stats))
            self.screen.blit(stat_surface, stat_rect)

    def _dibujar_podio(self, top3):
        """Dibuja el podio con las 3 mejores puntuaciones en tarjetas."""
        y_podio = 155
        ancho_tarjeta = 350
        alto_tarjeta = 110
        espacio = 20

        # Configuración del podio
        podio_config = [
            {
                "emoji": "1",
                "color_borde": (255, 215, 0),
                "color_fondo": (60, 50, 30),
                "titulo": "1er Lugar",
            },
            {
                "emoji": "2",
                "color_borde": (192, 192, 192),
                "color_fondo": (45, 45, 50),
                "titulo": "2do Lugar",
            },
            {
                "emoji": "3",
                "color_borde": (205, 127, 50),
                "color_fondo": (50, 40, 35),
                "titulo": "3er Lugar",
            },
        ]

        # Calcular posición inicial para centrar las 3 tarjetas
        ancho_total = (ancho_tarjeta * 3) + (espacio * 2)
        x_inicial = (self.ancho - ancho_total) // 2

        for i, reg in enumerate(top3):
            if i >= 3:
                break

            config = podio_config[i]
            x = x_inicial + (ancho_tarjeta + espacio) * i

            # Dibujar tarjeta
            rect_tarjeta = pygame.Rect(x, y_podio, ancho_tarjeta, alto_tarjeta)
            pygame.draw.rect(self.screen, config["color_fondo"], rect_tarjeta)
            pygame.draw.rect(self.screen, config["color_borde"], rect_tarjeta, 3)

            # Emoji y posición
            emoji_surface = self.font_podio.render(
                config["emoji"], False, config["color_borde"]
            )
            emoji_rect = emoji_surface.get_rect(
                center=(x + ancho_tarjeta // 2, y_podio + 20)
            )
            self.screen.blit(emoji_surface, emoji_rect)

            # Nombre del jugador
            nombre = reg["nombre_jugador"][:12]
            nombre_surface = self.font_data.render(nombre, False, (255, 255, 255))
            nombre_rect = nombre_surface.get_rect(
                center=(x + ancho_tarjeta // 2, y_podio + 50)
            )
            self.screen.blit(nombre_surface, nombre_rect)

            # Puntaje
            puntaje_text = f"{reg['puntaje']} pts"
            puntaje_surface = self.font_header.render(
                puntaje_text, False, config["color_borde"]
            )
            puntaje_rect = puntaje_surface.get_rect(
                center=(x + ancho_tarjeta // 2, y_podio + 70)
            )
            self.screen.blit(puntaje_surface, puntaje_rect)

            # Laberinto
            laberinto = reg["laberinto"][:20]
            lab_surface = self.font_info.render(laberinto, False, (180, 180, 200))
            lab_rect = lab_surface.get_rect(
                center=(x + ancho_tarjeta // 2, y_podio + 88)
            )
            self.screen.blit(lab_surface, lab_rect)

    def _dibujar_tabla(self, registros):
        """Dibuja la tabla con los registros del 4to al 10mo lugar.

        Returns:
            int: La última posición Y utilizada
        """
        y_inicio_tabla = 280

        # Título de la tabla
        titulo_tabla = self.font_header.render(
            "Otros récords", False, PaletaColores.ACENTO_INFO
        )
        titulo_rect = titulo_tabla.get_rect(center=(self.ancho // 2, y_inicio_tabla))
        self.screen.blit(titulo_tabla, titulo_rect)

        # Encabezados
        y_headers = y_inicio_tabla + 30
        headers = ["#", "Jugador", "Puntaje", "Laberinto"]
        x_positions = [100, 180, 380, 500]

        for header, x in zip(headers, x_positions, strict=True):
            texto_header = self.font_data.render(
                header, False, PaletaColores.ACENTO_INFO
            )
            self.screen.blit(texto_header, (x, y_headers))

        # Línea separadora
        pygame.draw.line(
            self.screen,
            PaletaColores.ACENTO_PRINCIPAL,
            (80, y_headers + 20),
            (self.ancho - 80, y_headers + 20),
            2,
        )

        # Registros
        ultima_y = y_headers + 40
        for i, reg in enumerate(registros[:7]):
            y_pos = y_headers + 40 + i * 22
            pos_global = i + 4

            # Color degradado
            alpha = 255 - (i * 20)
            color = (max(150, alpha), max(150, alpha), max(180, alpha))

            datos = [
                f"{pos_global}.",
                reg["nombre_jugador"][:15],
                f"{reg['puntaje']} pts",
                reg["laberinto"][:18],
            ]

            for dato, x in zip(datos, x_positions, strict=True):
                texto_dato = self.font_info.render(dato, False, color)
                self.screen.blit(texto_dato, (x, y_pos))

            ultima_y = y_pos + 25

        return ultima_y

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
