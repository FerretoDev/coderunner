import sys  # Permite salir de la app y manejar argumentos si hiciera falta

import pygame  # Motor para eventos, fuentes, dibujo y tiempo del loop

from .componentes.input_texto import (  # Componentes reutilizables de UI (botón e input)
    Boton,
    InputTexto,
)
from .config import (
    ConfigJuego,  # Configuración global del juego (tamaños, colores, etc.)
)


class MenuPrincipal:
    """Menú principal con botones horizontales.

    Muestra el título y cuatro botones: Iniciar, Salón de la Fama, Administración y Salir.
    Devuelve un número según la opción elegida para que el llamador actúe.
    """

    def __init__(self, screen):
        self.screen = screen  # Superficie principal donde se dibuja el menú [web:47]
        self.ancho = (
            screen.get_width()
        )  # Ancho actual de la ventana (útil para centrar) [web:47]
        self.alto = screen.get_height()  # Alto actual de la ventana [web:47]

        # Paleta de colores del menú
        self.COLORES = {
            "fondo": (20, 20, 30),  # Fondo oscuro para resaltar texto [web:21]
            "texto": (255, 255, 255),  # Texto principal en blanco [web:47]
            "acento": (0, 150, 255),  # Color de acento para líneas y detalles [web:21]
        }

        # Fuentes para título y subtítulos
        self.font_titulo = pygame.font.Font(
            None, 72
        )  # Tamaño grande para el título [web:47]
        self.font_subtitulo = pygame.font.Font(
            None, 24
        )  # Tamaño pequeño para mensajes [web:47]

        # Crear los botones alineados de forma horizontal
        self._crear_botones()  # Delega la creación para mantener __init__ limpio [web:21]

    def _crear_botones(self):
        """Calcula posiciones y crea los botones del menú."""
        ancho_boton = 180  # Ancho uniforme para consistencia visual [web:21]
        alto_boton = 60  # Alto cómodo para hacer click [web:21]
        espacio = 20  # Separación entre botones [web:21]

        num_botones = 4  # Iniciar, Salón, Admin, Salir [web:21]
        ancho_total = (ancho_boton * num_botones) + (
            espacio * (num_botones - 1)
        )  # Total para centrar [web:47]
        inicio_x = (
            self.ancho - ancho_total
        ) // 2  # Punto de inicio para que el grupo quede centrado [web:47]
        y = 350  # Altura a la que se dibujan los botones [web:21]

        self.botones = []  # Lista de instancias de Boton para iterar y dibujar [web:21]
        textos = [
            "Iniciar Juego",
            "Salón de la Fama",
            "Administración",
            "Salir",
        ]  # Etiquetas de cada botón [web:21]

        for i, texto in enumerate(textos):  # Recorre cada botón con su índice [web:21]
            x = (
                inicio_x + (ancho_boton + espacio) * i
            )  # Posiciona cada botón uno al lado del otro [web:47]
            self.botones.append(
                Boton(
                    x, y, ancho_boton, alto_boton, texto, accion=i + 1
                )  # acción=i+1 para devolver 1..4 [web:21]
            )  # Se usa acción para identificar qué opción eligió el usuario [web:21]

    def dibujar(self):
        """Pinta el fondo, título, línea decorativa, subtítulo, botones y footer."""
        self.screen.fill(
            self.COLORES["fondo"]
        )  # Limpia el frame con fondo oscuro [web:47]

        # Título con pequeña sombra para contraste
        titulo = self.font_titulo.render(
            ConfigJuego.TITULO, True, self.COLORES["texto"]
        )  # Texto principal [web:47]
        sombra = self.font_titulo.render(
            ConfigJuego.TITULO, True, (10, 10, 20)
        )  # Sombra tenue [web:47]

        sombra_rect = sombra.get_rect(
            center=(self.ancho // 2 + 3, 103)
        )  # Desfase leve para efecto sombra [web:47]
        titulo_rect = titulo.get_rect(
            center=(self.ancho // 2, 100)
        )  # Centrado horizontal [web:47]

        self.screen.blit(sombra, sombra_rect)  # Dibuja sombra primero [web:47]
        self.screen.blit(titulo, titulo_rect)  # Luego el título encima [web:47]

        # Línea decorativa bajo el título para separar visualmente
        pygame.draw.line(
            self.screen,
            self.COLORES["acento"],
            (self.ancho // 2 - 150, 150),
            (self.ancho // 2 + 150, 150),
            3,
        )  # Línea central de acento para estética [web:47]

        # Subtítulo con instrucciones del juego
        subtitulo = self.font_subtitulo.render(
            "Escapa del laberinto · Recolecta obsequios · Evita al enemigo",
            True,
            (150, 150, 150),
        )  # Texto aclaratorio y motivacional [web:21]
        subtitulo_rect = subtitulo.get_rect(
            center=(self.ancho // 2, 180)
        )  # Centrado bajo la línea [web:47]
        self.screen.blit(subtitulo, subtitulo_rect)  # Dibuja subtítulo [web:47]

        # Botones del menú
        for boton in self.botones:  # Recorre y dibuja cada botón [web:21]
            boton.dibujar(
                self.screen
            )  # Cada botón decide su color según hover/presionado [web:47]

        # Footer con indicación de uso del mouse
        footer = self.font_subtitulo.render(
            "Usa el mouse para seleccionar", True, (100, 100, 120)
        )  # Ayuda contextual [web:21]
        footer_rect = footer.get_rect(
            center=(self.ancho // 2, self.alto - 30)
        )  # Ubicado al fondo [web:47]
        self.screen.blit(footer, footer_rect)  # Dibuja el footer [web:47]

        pygame.display.flip()  # Actualiza la ventana con todo lo dibujado en este frame [web:47]

    def ejecutar(self):
        """Loop del menú: procesa eventos y devuelve la opción elegida."""
        clock = pygame.time.Clock()  # Controla los FPS del menú para fluidez [web:47]

        while True:  # Permanece hasta que el usuario elija o cierre [web:47]
            clock.tick(60)  # Limita a 60 FPS para no consumir CPU de más [web:47]
            mouse_pos = (
                pygame.mouse.get_pos()
            )  # Posición del mouse para hover/clics [web:47]

            for (
                evento
            ) in pygame.event.get():  # Lee eventos del sistema y usuario [web:47]
                if evento.type == pygame.QUIT:  # Cerrar ventana [web:47]
                    return 4  # Equivalente a “Salir” para el llamador [web:21]

                if evento.type == pygame.KEYDOWN:  # Alguna tecla presionada [web:47]
                    if (
                        evento.key == pygame.K_ESCAPE
                    ):  # Escape como atajo para salir [web:47]
                        return 4  # Devuelve “Salir” [web:21]

                # Verifica si algún botón recibió un click válido
                for boton in self.botones:  # Itera todos los botones [web:21]
                    if boton.manejar_evento(
                        evento, mouse_pos
                    ):  # Detecta click down sobre el botón [web:47]
                        return (
                            boton.accion
                        )  # Devuelve 1..4 según el botón elegido [web:21]

            self.dibujar()  # Redibuja cada frame para feedback visual (hover, etc.) [web:47]


class PantallaIniciarJuego:
    """Pantalla para ingresar nombre del jugador y continuar o volver."""

    def __init__(self, screen):
        self.screen = screen  # Superficie de dibujo [web:47]
        self.ancho = screen.get_width()  # Ancho de ventana [web:47]
        self.alto = screen.get_height()  # Alto de ventana [web:47]

        self.font_titulo = pygame.font.Font(
            None, 56
        )  # Fuente grande para título [web:47]
        self.font_texto = pygame.font.Font(
            None, 32
        )  # Fuente media para textos [web:47]

        # Campo de texto para el nombre con placeholder
        self.input_nombre = InputTexto(
            self.ancho // 2 - 200, 250, 400, 50, "Ingresa tu nombre"
        )  # Input centrado con ancho cómodo [web:21]

        # Botones de acción
        self.btn_continuar = Boton(
            self.ancho // 2 - 100, 350, 200, 50, "Continuar"
        )  # Continúa si hay nombre [web:21]
        self.btn_volver = Boton(
            self.ancho // 2 - 100, 420, 200, 50, "Volver"
        )  # Regresa al menú principal [web:21]

    def dibujar(self):
        """Dibuja fondo, textos, input y botones."""
        self.screen.fill((20, 20, 30))  # Fondo oscuro [web:47]

        # Título
        titulo = self.font_titulo.render(
            "Nuevo Juego", True, (255, 255, 255)
        )  # Título claro [web:47]
        titulo_rect = titulo.get_rect(
            center=(self.ancho // 2, 100)
        )  # Centrado arriba [web:47]
        self.screen.blit(titulo, titulo_rect)  # Dibuja el título [web:47]

        # Instrucción
        instruccion = self.font_texto.render(
            "Ingresa tu nombre para comenzar:", True, (200, 200, 200)
        )  # Indicación simple [web:21]
        instruccion_rect = instruccion.get_rect(
            center=(self.ancho // 2, 180)
        )  # Bajo el título [web:47]
        self.screen.blit(instruccion, instruccion_rect)  # Dibuja instrucción [web:47]

        # Input de nombre
        self.input_nombre.dibujar(
            self.screen
        )  # Renderiza input con su estado y cursor [web:47]

        # Botones
        self.btn_continuar.dibujar(self.screen)  # Botón principal [web:47]
        self.btn_volver.dibujar(self.screen)  # Botón para volver [web:47]

        pygame.display.flip()  # Actualiza pantalla [web:47]

    def ejecutar(self):
        """Loop: recoge nombre por Enter o botón, o vuelve con Escape/Volver."""
        clock = pygame.time.Clock()  # Control de FPS [web:47]

        while True:  # Permanece hasta confirmar o volver [web:47]
            clock.tick(60)  # Suavidad y bajo consumo [web:47]
            mouse_pos = pygame.mouse.get_pos()  # Para hover y clics en botones [web:47]

            for evento in pygame.event.get():  # Manejo de eventos [web:47]
                if evento.type == pygame.QUIT:  # Cerrar ventana [web:47]
                    return None  # Señal al llamador de que se abortó [web:21]

                if evento.type == pygame.KEYDOWN:  # Tecla presionada [web:47]
                    if evento.key == pygame.K_ESCAPE:  # Atajo para volver [web:47]
                        return None  # Sale sin nombre [web:21]

                # Input: si manejar_evento devuelve True, se presionó Enter
                if self.input_nombre.manejar_evento(
                    evento
                ):  # Procesa teclas y clicks del input [web:47]
                    nombre = (
                        self.input_nombre.obtener_texto()
                    )  # Lee el texto limpio [web:21]
                    if nombre:  # Solo acepta si no está vacío [web:21]
                        return nombre  # Confirma el nombre [web:21]

                # Botón Continuar: intenta confirmar el nombre
                if self.btn_continuar.manejar_evento(
                    evento, mouse_pos
                ):  # Click en Continuar [web:47]
                    nombre = self.input_nombre.obtener_texto()  # Lee el texto [web:21]
                    if nombre:  # Valida no vacío [web:21]
                        return nombre  # Devuelve el nombre [web:21]

                # Botón Volver: regresa sin nombre
                if self.btn_volver.manejar_evento(
                    evento, mouse_pos
                ):  # Click en Volver [web:47]
                    return None  # Señal de cancelar [web:21]

            self.dibujar()  # Redibuja cada frame [web:47]


class PantallaSalonFama:
    """Muestra los mejores puntajes con un listado sencillo."""

    def __init__(self, screen, salon_fama):
        self.screen = screen  # Superficie de dibujo [web:47]
        self.ancho = screen.get_width()  # Ancho ventana [web:47]
        self.alto = screen.get_height()  # Alto ventana [web:47]
        self.salon_fama = salon_fama  # Fuente de datos de récords [web:21]

        # Fuentes
        self.font_titulo = pygame.font.Font(None, 56)  # Título [web:47]
        self.font_header = pygame.font.Font(None, 28)  # Encabezados de tabla [web:47]
        self.font_data = pygame.font.Font(None, 24)  # Filas de datos [web:47]
        self.font_info = pygame.font.Font(None, 20)  # Mensajes informativos [web:47]
        self.font_stats = pygame.font.Font(None, 22)  # Estadísticas [web:47]

        # Botones
        self.btn_volver = Boton(
            self.ancho // 2 - 220, self.alto - 80, 200, 50, "Volver"
        )  # Permite regresar al menú principal [web:21]
        self.btn_reiniciar = Boton(
            self.ancho // 2 + 20, self.alto - 80, 200, 50, "Reiniciar"
        )  # Reinicia el salón de la fama [web:21]

    def dibujar(self):
        """Dibuja título, encabezados, registros si hay, y el botón volver."""
        self.screen.fill((20, 20, 30))  # Fondo [web:47]

        # Título con emoji de trofeo
        titulo = self.font_titulo.render(
            "🏆 Salón de la Fama", True, (255, 215, 0)
        )  # Color dorado [web:21]
        titulo_rect = titulo.get_rect(
            center=(self.ancho // 2, 40)
        )  # Centrado arriba [web:47]
        self.screen.blit(titulo, titulo_rect)  # Dibuja [web:47]

        # Obtener registros y estadísticas
        registros = self.salon_fama.mostrar_mejores()  # Lista de registros [web:21]
        stats = (
            self.salon_fama.obtener_estadisticas()
        )  # Estadísticas generales [web:21]

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
                stat_surface = self.font_stats.render(
                    texto, True, (180, 180, 200)
                )  # Color gris claro [web:21]
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
        )  # Línea azul [web:47]

        if not registros:  # Si no hay datos [web:21]
            texto = self.font_header.render(
                "No hay registros todavía", True, (150, 150, 150)
            )  # Mensaje gris [web:21]
            texto_rect = texto.get_rect(
                center=(self.ancho // 2, 300)
            )  # Centrado [web:47]
            self.screen.blit(texto, texto_rect)  # Dibuja [web:47]

            # Mensaje de ayuda
            ayuda = self.font_info.render(
                "¡Juega una partida para empezar a competir!", True, (120, 120, 140)
            )
            ayuda_rect = ayuda.get_rect(center=(self.ancho // 2, 340))
            self.screen.blit(ayuda, ayuda_rect)
        else:
            # Encabezados de la tabla
            headers = [
                "#",
                "Jugador",
                "Puntaje",
                "Laberinto",
                "Fecha",
            ]  # Columnas con fecha
            x_positions = [
                80,
                140,
                320,
                430,
                600,
            ]  # Posiciones ajustadas para 5 columnas

            for header, x in zip(
                headers, x_positions, strict=True
            ):  # Dibuja cada título de columna
                texto = self.font_header.render(
                    header, True, (150, 150, 150)
                )  # Gris [web:21]
                self.screen.blit(texto, (x, 200))  # Posición de encabezados ajustada

            # Línea separadora
            pygame.draw.line(
                self.screen, (100, 100, 120), (60, 225), (740, 225), 2
            )  # Separador ajustado

            # Mostrar hasta 10 registros
            for i, reg in enumerate(registros[:10]):  # Top 10 [web:21]
                y_pos = 240 + i * 30  # Espaciado entre filas

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
                    color = (200, 200, 200)  # Blanco grisáceo
                    emoji = f"{i + 1}"

                # Formatear fecha (solo mostrar fecha, no hora completa)
                fecha_str = reg.get("fecha", "N/A")
                if fecha_str != "N/A" and len(fecha_str) > 10:
                    fecha_str = fecha_str[:10]  # Solo YYYY-MM-DD

                datos = [
                    emoji,  # Posición con emoji para top 3
                    reg["nombre_jugador"][:12],  # Nombre truncado
                    str(reg["puntaje"]),  # Puntaje
                    reg["laberinto"][:15],  # Laberinto truncado
                    fecha_str,  # Fecha
                ]

                for dato, x in zip(datos, x_positions, strict=True):
                    texto = self.font_data.render(dato, True, color)
                    self.screen.blit(texto, (x, y_pos))

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
        self.btn_reiniciar.dibujar(self.screen)

        pygame.display.flip()  # Actualiza pantalla [web:47]

    def ejecutar(self):
        """Loop de lectura: cierra con Volver, Escape o al cerrar ventana."""
        clock = pygame.time.Clock()  # Control FPS [web:47]

        while True:  # Permanece hasta acción de salida [web:47]
            clock.tick(60)  # Suave y eficiente [web:47]
            mouse_pos = pygame.mouse.get_pos()  # Para hover y clicks [web:47]

            for evento in pygame.event.get():  # Manejo de eventos [web:47]
                if evento.type == pygame.QUIT:  # Cerrar ventana [web:47]
                    return  # Sale al llamador (menú) [web:21]

                if evento.type == pygame.KEYDOWN:  # Teclas [web:47]
                    if evento.key == pygame.K_ESCAPE:  # Atajo de salida [web:47]
                        return  # Vuelve al menú [web:21]

                if self.btn_volver.manejar_evento(
                    evento, mouse_pos
                ):  # Click en Volver [web:47]
                    return  # Sale [web:21]

                if self.btn_reiniciar.manejar_evento(
                    evento, mouse_pos
                ):  # Click en Reiniciar [web:47]
                    # Reiniciar el salón de la fama
                    self.salon_fama.reiniciar()

            self.dibujar()  # Redibuja [web:47]


class PantallaAdministracion:
    """Solicita la clave de administrador y la devuelve para validarla afuera."""

    def __init__(self, screen):
        self.screen = screen  # Superficie de dibujo [web:47]
        self.ancho = screen.get_width()  # Ancho de la ventana [web:47]
        self.alto = screen.get_height()  # Alto de la ventana [web:47]
        self.autenticado = False  # Bandera local por si se usa en el futuro [web:21]

        self.font_titulo = pygame.font.Font(None, 56)  # Título [web:47]
        self.font_texto = pygame.font.Font(None, 32)  # Texto [web:47]

        # Input de clave con placeholder
        self.input_clave = InputTexto(
            self.ancho // 2 - 200, 250, 400, 50, "Ingresa la clave"
        )  # Centrado y tamaño cómodo [web:21]

        # Botones
        self.btn_ingresar = Boton(
            self.ancho // 2 - 100, 350, 200, 50, "Ingresar"
        )  # Aceptar [web:21]
        self.btn_volver = Boton(
            self.ancho // 2 - 100, 420, 200, 50, "Volver"
        )  # Cancelar [web:21]

    def dibujar(self):
        """Dibuja la pantalla de autenticación con input, botones y un hint."""
        self.screen.fill((20, 20, 30))  # Fondo [web:47]

        # Título
        titulo = self.font_titulo.render(
            "🔐 Administración", True, (255, 255, 255)
        )  # Título claro [web:47]
        titulo_rect = titulo.get_rect(
            center=(self.ancho // 2, 100)
        )  # Centrado [web:47]
        self.screen.blit(titulo, titulo_rect)  # Dibuja [web:47]

        # Instrucción
        instruccion = self.font_texto.render(
            "Ingresa la clave de administrador:", True, (200, 200, 200)
        )  # Texto guía [web:21]
        instruccion_rect = instruccion.get_rect(
            center=(self.ancho // 2, 180)
        )  # Ubicación [web:47]
        self.screen.blit(instruccion, instruccion_rect)  # Dibuja [web:47]

        # Input y botones
        self.input_clave.dibujar(self.screen)  # Campo de texto [web:47]
        self.btn_ingresar.dibujar(self.screen)  # Botón aceptar [web:47]
        self.btn_volver.dibujar(self.screen)  # Botón volver [web:47]

        # Hint visible al pie de pantalla
        hint = pygame.font.Font(None, 20).render(
            "Clave por defecto: admin123", True, (100, 100, 120)
        )  # Mensaje de ayuda [web:21]
        hint_rect = hint.get_rect(
            center=(self.ancho // 2, self.alto - 30)
        )  # Posición [web:47]
        self.screen.blit(hint, hint_rect)  # Dibuja [web:47]

        pygame.display.flip()  # Actualiza [web:47]

    def ejecutar(self):
        """Loop: devuelve la clave con Enter o Ingresar, o None al volver/salir."""
        clock = pygame.time.Clock()  # Control FPS [web:47]

        while True:  # Espera interacción del usuario [web:47]
            clock.tick(60)  # Suaviza y limita consumo [web:47]
            mouse_pos = pygame.mouse.get_pos()  # Posición del mouse [web:47]

            for evento in pygame.event.get():  # Procesa eventos [web:47]
                if evento.type == pygame.QUIT:  # Cerrar ventana [web:47]
                    return None  # Señal de cancelar [web:21]

                if evento.type == pygame.KEYDOWN:  # Teclas [web:47]
                    if evento.key == pygame.K_ESCAPE:  # Atajo de cancelar [web:47]
                        return None  # Sale [web:21]

                # Input: Enter devuelve inmediatamente la clave
                if self.input_clave.manejar_evento(
                    evento
                ):  # Procesa tecla/Click [web:47]
                    clave = (
                        self.input_clave.obtener_texto()
                    )  # Lee la clave ingresada [web:21]
                    return clave  # Devuelve para que el llamador la valide [web:21]

                # Botón Ingresar: también devuelve la clave
                if self.btn_ingresar.manejar_evento(
                    evento, mouse_pos
                ):  # Click en Ingresar [web:47]
                    clave = self.input_clave.obtener_texto()  # Lee la clave [web:21]
                    return clave  # Devuelve para validar [web:21]

                # Botón Volver
                if self.btn_volver.manejar_evento(
                    evento, mouse_pos
                ):  # Click en Volver [web:47]
                    return None  # Cancela [web:21]

            self.dibujar()  # Redibuja [web:47]


class MensajeModal:
    """Cuadro de diálogo simple para mostrar mensajes y confirmar con OK."""

    def __init__(self, screen, titulo, mensaje, tipo="info"):
        self.screen = screen  # Superficie de dibujo [web:47]
        self.ancho = screen.get_width()  # Ancho de ventana [web:47]
        self.alto = screen.get_height()  # Alto de ventana [web:47]
        self.titulo = titulo  # Título del modal (ej. “Acceso Concedido”) [web:21]
        self.mensaje = mensaje  # Mensaje principal [web:21]
        self.tipo = tipo  # info, success, error o warning para cambiar color [web:21]

        self.font_titulo = pygame.font.Font(None, 48)  # Fuente para título [web:47]
        self.font_mensaje = pygame.font.Font(None, 32)  # Fuente para texto [web:47]

        # Botón OK centrado bajo el mensaje
        self.btn_ok = Boton(
            self.ancho // 2 - 75, self.alto // 2 + 60, 150, 50, "OK"
        )  # Cierra el modal [web:21]

        # Colores de acento según el tipo de mensaje
        colores = {
            "info": (0, 150, 255),  # Azul informativo [web:21]
            "success": (0, 200, 100),  # Verde de éxito [web:21]
            "error": (255, 50, 50),  # Rojo de error [web:21]
            "warning": (255, 200, 0),  # Amarillo de advertencia [web:21]
        }  # Mapa simple para estilo visual del modal [web:21]
        self.color_acento = colores.get(
            tipo, colores["info"]
        )  # Por defecto “info” [web:21]

    def dibujar(self):
        """Dibuja fondo translúcido, caja con borde, textos y el botón OK."""
        # Fondo semitransparente para centrar la atención
        overlay = pygame.Surface(
            (self.ancho, self.alto)
        )  # Capa del tamaño de la ventana [web:47]
        overlay.set_alpha(200)  # Opacidad para oscurecer el fondo [web:47]
        overlay.fill((0, 0, 0))  # Negro [web:47]
        self.screen.blit(overlay, (0, 0))  # Dibuja la capa [web:47]

        # Caja central del modal
        modal_rect = pygame.Rect(
            self.ancho // 2 - 250, self.alto // 2 - 100, 500, 200
        )  # Caja de 500x200 [web:47]
        pygame.draw.rect(
            self.screen, (40, 40, 60), modal_rect, border_radius=15
        )  # Fondo de la caja [web:47]
        pygame.draw.rect(
            self.screen, self.color_acento, modal_rect, 3, border_radius=15
        )  # Borde con color de acento [web:47]

        # Título centrado
        titulo_surface = self.font_titulo.render(
            self.titulo, True, self.color_acento
        )  # Texto del título [web:47]
        titulo_rect = titulo_surface.get_rect(
            center=(self.ancho // 2, self.alto // 2 - 50)
        )  # Posición superior de la caja [web:47]
        self.screen.blit(titulo_surface, titulo_rect)  # Dibuja título [web:47]

        # Mensaje principal
        mensaje_surface = self.font_mensaje.render(
            self.mensaje, True, (255, 255, 255)
        )  # Texto blanco [web:47]
        mensaje_rect = mensaje_surface.get_rect(
            center=(self.ancho // 2, self.alto // 2)
        )  # Centro de la caja [web:47]
        self.screen.blit(mensaje_surface, mensaje_rect)  # Dibuja mensaje [web:47]

        # Botón OK
        self.btn_ok.dibujar(self.screen)  # Dibuja el botón [web:47]

        pygame.display.flip()  # Actualiza pantalla [web:47]

    def ejecutar(self):
        """Loop del modal: se cierra con OK, Enter/Escape o al cerrar la ventana."""
        clock = pygame.time.Clock()  # Control de FPS para fluidez [web:47]

        while True:  # Espera una acción de cierre [web:47]
            clock.tick(60)  # Establece 60 FPS [web:47]
            mouse_pos = pygame.mouse.get_pos()  # Para hover/click en OK [web:47]

            for evento in pygame.event.get():  # Revisa eventos [web:47]
                if evento.type == pygame.QUIT:  # Cerrar ventana [web:47]
                    return  # Sale al llamador [web:21]

                if evento.type == pygame.KEYDOWN:  # Teclas [web:47]
                    if evento.key in [
                        pygame.K_RETURN,
                        pygame.K_ESCAPE,
                    ]:  # Enter/Escape [web:47]
                        return  # Cierra el modal [web:21]

                if self.btn_ok.manejar_evento(
                    evento, mouse_pos
                ):  # Click en OK [web:47]
                    return  # Cierra [web:21]

            self.dibujar()  # Sigue dibujando hasta cerrar [web:47]


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


class PantallaCargaLaberinto:
    """
    Pantalla para seleccionar y cargar un archivo de laberinto.
    Utiliza tkinter.filedialog para explorador de archivos.
    """

    def __init__(self, screen, admin):
        self.screen = screen
        self.ancho = screen.get_width()
        self.alto = screen.get_height()
        self.admin = admin  # Instancia del Administrador

        self.COLORES = {
            "fondo": (20, 20, 30),
            "texto": (255, 255, 255),
            "acento": (0, 150, 255),
        }

        self.font_titulo = pygame.font.Font(None, 52)
        self.font_texto = pygame.font.Font(None, 28)
        self.font_info = pygame.font.Font(None, 22)

        # Botones
        self.btn_explorar = Boton(
            self.ancho // 2 - 200, 250, 400, 60, "📂 Seleccionar Archivo"
        )
        self.btn_cargar = Boton(
            self.ancho // 2 - 200, 340, 190, 50, "✓ Cargar", activo=False
        )
        self.btn_volver = Boton(self.ancho // 2 + 10, 340, 190, 50, "✗ Cancelar")

        self.archivo_seleccionado = None
        self.nombre_archivo = ""

    def dibujar(self):
        """Dibuja la pantalla de carga de laberinto."""
        self.screen.fill(self.COLORES["fondo"])

        # Título
        titulo = self.font_titulo.render(
            "Cargar Laberinto", True, self.COLORES["acento"]
        )
        titulo_rect = titulo.get_rect(center=(self.ancho // 2, 100))
        self.screen.blit(titulo, titulo_rect)

        # Instrucción
        instruccion = self.font_texto.render(
            "Selecciona un archivo .json o .txt:", True, (200, 200, 200)
        )
        instruccion_rect = instruccion.get_rect(center=(self.ancho // 2, 170))
        self.screen.blit(instruccion, instruccion_rect)

        # Mostrar archivo seleccionado
        if self.archivo_seleccionado:
            archivo_texto = self.font_info.render(
                f"Archivo: {self.nombre_archivo}", True, (100, 255, 100)
            )
            archivo_rect = archivo_texto.get_rect(center=(self.ancho // 2, 430))
            self.screen.blit(archivo_texto, archivo_rect)
        else:
            archivo_texto = self.font_info.render(
                "Ningún archivo seleccionado", True, (150, 150, 150)
            )
            archivo_rect = archivo_texto.get_rect(center=(self.ancho // 2, 430))
            self.screen.blit(archivo_texto, archivo_rect)

        # Botones
        self.btn_explorar.dibujar(self.screen)
        self.btn_cargar.dibujar(self.screen)
        self.btn_volver.dibujar(self.screen)

        # Información adicional
        info = self.font_info.render(
            "Formatos aceptados: .json, .txt", True, (120, 120, 140)
        )
        info_rect = info.get_rect(center=(self.ancho // 2, self.alto - 50))
        self.screen.blit(info, info_rect)

        pygame.display.flip()

    def seleccionar_archivo(self):
        """Abre el diálogo de selección de archivo usando tkinter."""
        try:
            import tkinter as tk
            from tkinter import filedialog

            # Crear ventana temporal de tkinter (oculta)
            root = tk.Tk()
            root.withdraw()  # Ocultar la ventana principal
            root.attributes("-topmost", True)  # Mantener al frente

            # Abrir diálogo de selección
            archivo = filedialog.askopenfilename(
                title="Seleccionar archivo de laberinto",
                filetypes=[
                    ("Archivos JSON", "*.json"),
                    ("Archivos de texto", "*.txt"),
                    ("Todos los archivos", "*.*"),
                ],
            )

            root.destroy()  # Cerrar ventana temporal

            if archivo:
                self.archivo_seleccionado = archivo
                self.nombre_archivo = archivo.split("/")[-1].split("\\")[-1]
                return True

            return False

        except Exception as e:
            print(f"Error al abrir selector de archivo: {e}")
            return False

    def ejecutar(self):
        """
        Loop de la pantalla de carga.

        Returns:
            tuple: (laberinto, mensaje) si se cargó exitosamente, (None, None) si se canceló
        """
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return None, None

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return None, None

                # Botón Explorar
                if self.btn_explorar.manejar_evento(evento, mouse_pos):
                    self.seleccionar_archivo()

                # Botón Cargar
                if self.btn_cargar.manejar_evento(evento, mouse_pos):
                    if self.archivo_seleccionado:
                        laberinto, mensaje = self.admin.cargar_laberinto(
                            self.archivo_seleccionado
                        )
                        return laberinto, mensaje

                # Botón Volver
                if self.btn_volver.manejar_evento(evento, mouse_pos):
                    return None, None

            self.dibujar()


class ModalConfirmacion:
    """
    Modal de confirmación con botones Sí/No.
    Se usa para confirmar acciones críticas como salir o reiniciar datos.
    """

    def __init__(self, screen, titulo, mensaje):
        self.screen = screen
        self.ancho = screen.get_width()
        self.alto = screen.get_height()
        self.titulo = titulo
        self.mensaje = mensaje

        self.font_titulo = pygame.font.Font(None, 44)
        self.font_mensaje = pygame.font.Font(None, 28)

        # Botones
        self.btn_si = Boton(self.ancho // 2 - 160, self.alto // 2 + 50, 140, 50, "✓ Sí")
        self.btn_no = Boton(self.ancho // 2 + 20, self.alto // 2 + 50, 140, 50, "✗ No")

    def dibujar(self):
        """Dibuja el modal de confirmación."""
        # Fondo semitransparente
        overlay = pygame.Surface((self.ancho, self.alto))
        overlay.set_alpha(220)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Caja del modal
        modal_rect = pygame.Rect(self.ancho // 2 - 300, self.alto // 2 - 120, 600, 240)
        pygame.draw.rect(self.screen, (40, 40, 60), modal_rect, border_radius=15)
        pygame.draw.rect(self.screen, (255, 200, 0), modal_rect, 3, border_radius=15)

        # Título
        titulo_surface = self.font_titulo.render(self.titulo, True, (255, 200, 0))
        titulo_rect = titulo_surface.get_rect(
            center=(self.ancho // 2, self.alto // 2 - 70)
        )
        self.screen.blit(titulo_surface, titulo_rect)

        # Mensaje (puede tener múltiples líneas)
        lineas = self.mensaje.split("\n")
        y_offset = -20
        for linea in lineas:
            mensaje_surface = self.font_mensaje.render(linea, True, (255, 255, 255))
            mensaje_rect = mensaje_surface.get_rect(
                center=(self.ancho // 2, self.alto // 2 + y_offset)
            )
            self.screen.blit(mensaje_surface, mensaje_rect)
            y_offset += 35

        # Botones
        self.btn_si.dibujar(self.screen)
        self.btn_no.dibujar(self.screen)

        pygame.display.flip()

    def ejecutar(self):
        """
        Loop del modal de confirmación.

        Returns:
            bool: True si confirmó (Sí), False si canceló (No)
        """
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return False
                    if evento.key == pygame.K_RETURN:
                        return True

                # Botones
                if self.btn_si.manejar_evento(evento, mouse_pos):
                    return True
                if self.btn_no.manejar_evento(evento, mouse_pos):
                    return False

            self.dibujar()
