import sys

import pygame

from .componentes.input_texto import Boton, InputTexto


class MenuPrincipal:
    """Menú principal con botones horizontales"""

    def __init__(self, screen):
        self.screen = screen
        self.ancho = screen.get_width()
        self.alto = screen.get_height()

        # Colores
        self.COLORES = {
            "fondo": (20, 20, 30),
            "texto": (255, 255, 255),
            "acento": (0, 150, 255),
        }

        # Fuentes
        self.font_titulo = pygame.font.Font(None, 72)
        self.font_subtitulo = pygame.font.Font(None, 24)

        # Crear botones
        self._crear_botones()

    def _crear_botones(self):
        """Crea los botones del menú"""
        ancho_boton = 180
        alto_boton = 60
        espacio = 20

        num_botones = 4
        ancho_total = (ancho_boton * num_botones) + (espacio * (num_botones - 1))
        inicio_x = (self.ancho - ancho_total) // 2
        y = 350

        self.botones = []
        textos = ["Iniciar Juego", "Salón de la Fama", "Administración", "Salir"]

        for i, texto in enumerate(textos):
            x = inicio_x + (ancho_boton + espacio) * i
            self.botones.append(
                Boton(x, y, ancho_boton, alto_boton, texto, accion=i + 1)
            )

    def dibujar(self):
        """Dibuja el menú"""
        self.screen.fill(self.COLORES["fondo"])

        # Título
        titulo = self.font_titulo.render("CodeRunner", True, self.COLORES["texto"])
        sombra = self.font_titulo.render("CodeRunner", True, (10, 10, 20))

        sombra_rect = sombra.get_rect(center=(self.ancho // 2 + 3, 103))
        titulo_rect = titulo.get_rect(center=(self.ancho // 2, 100))

        self.screen.blit(sombra, sombra_rect)
        self.screen.blit(titulo, titulo_rect)

        # Línea decorativa
        pygame.draw.line(
            self.screen,
            self.COLORES["acento"],
            (self.ancho // 2 - 150, 150),
            (self.ancho // 2 + 150, 150),
            3,
        )

        # Subtítulo
        subtitulo = self.font_subtitulo.render(
            "Escapa del laberinto · Recolecta obsequios · Evita al enemigo",
            True,
            (150, 150, 150),
        )
        subtitulo_rect = subtitulo.get_rect(center=(self.ancho // 2, 180))
        self.screen.blit(subtitulo, subtitulo_rect)

        # Botones
        for boton in self.botones:
            boton.dibujar(self.screen)

        # Footer
        footer = self.font_subtitulo.render(
            "Usa el mouse para seleccionar", True, (100, 100, 120)
        )
        footer_rect = footer.get_rect(center=(self.ancho // 2, self.alto - 30))
        self.screen.blit(footer, footer_rect)

        pygame.display.flip()

    def ejecutar(self):
        """Loop del menú"""
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return 4

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return 4

                # Verificar clicks en botones
                for boton in self.botones:
                    if boton.manejar_evento(evento, mouse_pos):
                        return boton.accion

            self.dibujar()


class PantallaIniciarJuego:
    """Pantalla para ingresar nombre (TODO VISUAL)"""

    def __init__(self, screen):
        self.screen = screen
        self.ancho = screen.get_width()
        self.alto = screen.get_height()

        self.font_titulo = pygame.font.Font(None, 56)
        self.font_texto = pygame.font.Font(None, 32)

        # Input de nombre
        self.input_nombre = InputTexto(
            self.ancho // 2 - 200, 250, 400, 50, "Ingresa tu nombre"
        )

        # Botones
        self.btn_continuar = Boton(self.ancho // 2 - 100, 350, 200, 50, "Continuar")

        self.btn_volver = Boton(self.ancho // 2 - 100, 420, 200, 50, "Volver")

    def dibujar(self):
        """Dibuja la pantalla"""
        self.screen.fill((20, 20, 30))

        # Título
        titulo = self.font_titulo.render("Nuevo Juego", True, (255, 255, 255))
        titulo_rect = titulo.get_rect(center=(self.ancho // 2, 100))
        self.screen.blit(titulo, titulo_rect)

        # Instrucción
        instruccion = self.font_texto.render(
            "Ingresa tu nombre para comenzar:", True, (200, 200, 200)
        )
        instruccion_rect = instruccion.get_rect(center=(self.ancho // 2, 180))
        self.screen.blit(instruccion, instruccion_rect)

        # Input
        self.input_nombre.dibujar(self.screen)

        # Botones
        self.btn_continuar.dibujar(self.screen)
        self.btn_volver.dibujar(self.screen)

        pygame.display.flip()

    def ejecutar(self):
        """Loop de la pantalla"""
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return None

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return None

                # Input
                if self.input_nombre.manejar_evento(evento):
                    # Enter presionado
                    nombre = self.input_nombre.obtener_texto()
                    if nombre:
                        return nombre

                # Botones
                if self.btn_continuar.manejar_evento(evento, mouse_pos):
                    nombre = self.input_nombre.obtener_texto()
                    if nombre:
                        return nombre

                if self.btn_volver.manejar_evento(evento, mouse_pos):
                    return None

            self.dibujar()


class PantallaSalonFama:
    """Pantalla del salón de la fama"""

    def __init__(self, screen, salon_fama):
        self.screen = screen
        self.ancho = screen.get_width()
        self.alto = screen.get_height()
        self.salon_fama = salon_fama

        self.font_titulo = pygame.font.Font(None, 56)
        self.font_header = pygame.font.Font(None, 32)
        self.font_data = pygame.font.Font(None, 28)
        self.font_info = pygame.font.Font(None, 24)

        # Botón volver
        self.btn_volver = Boton(
            self.ancho // 2 - 100, self.alto - 80, 200, 50, "Volver"
        )

    def dibujar(self):
        """Dibuja la pantalla"""
        self.screen.fill((20, 20, 30))

        # Título
        titulo = self.font_titulo.render("🏆 Salón de la Fama", True, (255, 215, 0))
        titulo_rect = titulo.get_rect(center=(self.ancho // 2, 60))
        self.screen.blit(titulo, titulo_rect)

        # Obtener registros
        registros = self.salon_fama.mostrar_mejores()

        if not registros:
            texto = self.font_header.render(
                "No hay registros todavía", True, (150, 150, 150)
            )
            texto_rect = texto.get_rect(center=(self.ancho // 2, 300))
            self.screen.blit(texto, texto_rect)
        else:
            # Encabezados
            headers = ["#", "Jugador", "Puntaje", "Laberinto"]
            x_positions = [100, 200, 450, 600]

            for header, x in zip(headers, x_positions):
                texto = self.font_header.render(header, True, (150, 150, 150))
                self.screen.blit(texto, (x, 130))

            # Línea
            pygame.draw.line(self.screen, (100, 100, 120), (80, 160), (720, 160), 2)

            # Datos
            for i, reg in enumerate(registros[:10]):
                y_pos = 180 + i * 35
                color = (255, 215, 0) if i < 3 else (200, 200, 200)

                datos = [
                    f"{i + 1}",
                    reg["nombre_jugador"][:15],
                    str(reg["puntaje"]),
                    reg["laberinto"][:12],
                ]

                for dato, x in zip(datos, x_positions):
                    texto = self.font_data.render(dato, True, color)
                    self.screen.blit(texto, (x, y_pos))

        # Botón volver
        self.btn_volver.dibujar(self.screen)

        pygame.display.flip()

    def ejecutar(self):
        """Loop de la pantalla"""
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


class PantallaAdministracion:
    """Pantalla de administración"""

    def __init__(self, screen):
        self.screen = screen
        self.ancho = screen.get_width()
        self.alto = screen.get_height()
        self.autenticado = False

        self.font_titulo = pygame.font.Font(None, 56)
        self.font_texto = pygame.font.Font(None, 32)

        # Input de clave
        self.input_clave = InputTexto(
            self.ancho // 2 - 200, 250, 400, 50, "Ingresa la clave"
        )

        # Botones
        self.btn_ingresar = Boton(self.ancho // 2 - 100, 350, 200, 50, "Ingresar")

        self.btn_volver = Boton(self.ancho // 2 - 100, 420, 200, 50, "Volver")

    def dibujar(self):
        """Dibuja la pantalla"""
        self.screen.fill((20, 20, 30))

        # Título
        titulo = self.font_titulo.render("🔐 Administración", True, (255, 255, 255))
        titulo_rect = titulo.get_rect(center=(self.ancho // 2, 100))
        self.screen.blit(titulo, titulo_rect)

        # Instrucción
        instruccion = self.font_texto.render(
            "Ingresa la clave de administrador:", True, (200, 200, 200)
        )
        instruccion_rect = instruccion.get_rect(center=(self.ancho // 2, 180))
        self.screen.blit(instruccion, instruccion_rect)

        # Input
        self.input_clave.dibujar(self.screen)

        # Botones
        self.btn_ingresar.dibujar(self.screen)
        self.btn_volver.dibujar(self.screen)

        # Hint
        hint = pygame.font.Font(None, 20).render(
            "Clave por defecto: admin123", True, (100, 100, 120)
        )
        hint_rect = hint.get_rect(center=(self.ancho // 2, self.alto - 30))
        self.screen.blit(hint, hint_rect)

        pygame.display.flip()

    def ejecutar(self):
        """Loop de la pantalla"""
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return None

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return None

                # Input
                if self.input_clave.manejar_evento(evento):
                    clave = self.input_clave.obtener_texto()
                    return clave

                # Botones
                if self.btn_ingresar.manejar_evento(evento, mouse_pos):
                    clave = self.input_clave.obtener_texto()
                    return clave

                if self.btn_volver.manejar_evento(evento, mouse_pos):
                    return None

            self.dibujar()


class MensajeModal:
    """Modal para mostrar mensajes (como alert en web)"""

    def __init__(self, screen, titulo, mensaje, tipo="info"):
        self.screen = screen
        self.ancho = screen.get_width()
        self.alto = screen.get_height()
        self.titulo = titulo
        self.mensaje = mensaje
        self.tipo = tipo

        self.font_titulo = pygame.font.Font(None, 48)
        self.font_mensaje = pygame.font.Font(None, 32)

        # Botón OK
        self.btn_ok = Boton(self.ancho // 2 - 75, self.alto // 2 + 60, 150, 50, "OK")

        # Colores según tipo
        colores = {
            "info": (0, 150, 255),
            "success": (0, 200, 100),
            "error": (255, 50, 50),
            "warning": (255, 200, 0),
        }
        self.color_acento = colores.get(tipo, colores["info"])

    def dibujar(self):
        """Dibuja el modal"""
        # Fondo semitransparente
        overlay = pygame.Surface((self.ancho, self.alto))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Caja del modal
        modal_rect = pygame.Rect(self.ancho // 2 - 250, self.alto // 2 - 100, 500, 200)
        pygame.draw.rect(self.screen, (40, 40, 60), modal_rect, border_radius=15)
        pygame.draw.rect(
            self.screen, self.color_acento, modal_rect, 3, border_radius=15
        )

        # Título
        titulo_surface = self.font_titulo.render(self.titulo, True, self.color_acento)
        titulo_rect = titulo_surface.get_rect(
            center=(self.ancho // 2, self.alto // 2 - 50)
        )
        self.screen.blit(titulo_surface, titulo_rect)

        # Mensaje
        mensaje_surface = self.font_mensaje.render(self.mensaje, True, (255, 255, 255))
        mensaje_rect = mensaje_surface.get_rect(
            center=(self.ancho // 2, self.alto // 2)
        )
        self.screen.blit(mensaje_surface, mensaje_rect)

        # Botón
        self.btn_ok.dibujar(self.screen)

        pygame.display.flip()

    def ejecutar(self):
        """Loop del modal"""
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return

                if evento.type == pygame.KEYDOWN:
                    if evento.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                        return

                if self.btn_ok.manejar_evento(evento, mouse_pos):
                    return

            self.dibujar()
