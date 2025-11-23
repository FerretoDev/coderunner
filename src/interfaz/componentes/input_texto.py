"""
Componentes UI con Pygame: campo de texto y botón.

Incluye:
- InputTexto: campo para escribir con placeholder y cursor que parpadea.
- Boton: botón con estados hover y presionado.

Requisitos:
- Llamar a pygame.init() antes de usar.
- Usar un loop de eventos y un loop de dibujo en cada frame.
"""

import pygame  # Librería para gráficos, ventana y eventos en juegos y apps [web:21]
from interfaz.gestor_fuentes import GestorFuentes


class InputTexto:
    """Campo de texto simple al estilo input de HTML.

    Permite activar con click, escribir cuando está activo y mostrar un cursor parpadeante.

    Args:
        x (int): Posición horizontal del input en pantalla. [web:21]
        y (int): Posición vertical del input en pantalla. [web:21]
        ancho (int): Ancho del rectángulo del input. [web:21]
        alto (int): Alto del rectángulo del input. [web:21]
        placeholder (str): Texto de guía cuando está vacío. [web:42]

    Returns:
        manejar_evento: True cuando presionas Enter estando activo, para que el llamador lo detecte. [web:21]
    """

    def __init__(self, x, y, ancho, alto, placeholder=""):
        self.rect = pygame.Rect(
            x, y, ancho, alto
        )  # Área del input para dibujar y detectar clicks [web:21]
        self.texto = ""  # Lo que el usuario ha escrito hasta ahora [web:21]
        self.placeholder = (
            placeholder  # Texto de guía cuando no hay entrada del usuario [web:42]
        )
        self.activo = False  # Indica si acepta teclado (tiene foco) [web:21]
        self.cursor_visible = (
            True  # Estado del cursor (se alterna para parpadear) [web:21]
        )
        self.cursor_timer = (
            0  # Contador para controlar el parpadeo del cursor por frames [web:21]
        )

        # Colores de estados y texto - Estilo pixel art vibrante
        self.COLOR_INACTIVO = (40, 50, 80)  # Fondo cuando no está activo [web:42]
        self.COLOR_ACTIVO = (60, 80, 120)  # Fondo cuando está activo [web:42]
        self.COLOR_TEXTO = (255, 255, 255)  # Color del texto y cursor [web:21]
        self.COLOR_PLACEHOLDER = (
            100,
            120,
            160,
        )  # Color del placeholder (más tenue) [web:42]
        self.COLOR_BORDE = (80, 100, 160)  # Color del borde normal [web:42]
        self.COLOR_BORDE_ACTIVO = (
            0,
            200,
            255,
        )  # Borde resaltado cyan brillante cuando está activo [web:42]

        fuentes = GestorFuentes()
        self.font = fuentes.texto_normal  # Fuente pixel art para el input [web:21]

    def manejar_evento(self, evento):
        """Procesa clicks y teclado del usuario.

        - Click dentro del rectángulo: activa el input. Fuera: lo desactiva.
        - Si está activo y presionas Enter: devuelve True (confirmación).
        - Si está activo y presionas Backspace: borra el último carácter.
        - Si está activo y escribes otra tecla: agrega el carácter (máx. 20).
        """
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # Activa si haces click dentro; desactiva si haces click fuera
            self.activo = self.rect.collidepoint(
                evento.pos
            )  # Fácil de entender y mantener [web:21]

        if evento.type == pygame.KEYDOWN and self.activo:
            if evento.key == pygame.K_RETURN:
                return True  # Señal de “listo” para que el código externo lo use (ej. enviar) [web:21]
            elif evento.key == pygame.K_BACKSPACE:
                self.texto = self.texto[
                    :-1
                ]  # Borra el último carácter de forma segura [web:21]
            else:
                # Límite simple para que el texto no se salga visualmente del input
                if (
                    len(self.texto) < 20
                ):  # Evita desbordes sin cálculos complejos [web:21]
                    self.texto += (
                        evento.unicode
                    )  # Agrega el carácter según el teclado del sistema [web:21]

        return False  # No hubo Enter o no estaba activo al presionar tecla [web:21]

    def dibujar(self, screen):
        """Dibuja el input: fondo, borde, texto/placeholder y cursor si está activo."""
        # Fondo y borde cambian si está activo (feedback visual claro)
        color_fondo = self.COLOR_ACTIVO if self.activo else self.COLOR_INACTIVO
        color_borde = self.COLOR_BORDE_ACTIVO if self.activo else self.COLOR_BORDE

        # Rectángulo del input estilo pixel art (sin border_radius)
        pygame.draw.rect(screen, color_fondo, self.rect)
        pygame.draw.rect(screen, color_borde, self.rect, 2)

        # Si hay texto, lo dibujamos; si no, mostramos el placeholder
        if self.texto:
            texto_surface = self.font.render(self.texto, False, self.COLOR_TEXTO)
        else:
            texto_surface = self.font.render(
                self.placeholder, False, self.COLOR_PLACEHOLDER
            )  # Guía cuando está vacío [web:42]

        # Posición: centrado vertical y con un pequeño margen a la izquierda
        texto_rect = texto_surface.get_rect(
            midleft=(self.rect.x + 10, self.rect.centery)
        )  # Alineación simple y clara [web:21]
        screen.blit(
            texto_surface, texto_rect
        )  # Dibuja el texto en la pantalla [web:21]

        # Cursor que parpadea cuando está activo (controlado por frames)
        if self.activo:
            self.cursor_timer += (
                1  # Incrementa cada frame para alternar visibilidad [web:21]
            )
            if (
                self.cursor_timer > 30
            ):  # Umbral del parpadeo (aprox. 0.5s a 60 FPS) [web:21]
                self.cursor_visible = (
                    not self.cursor_visible
                )  # Cambia entre visible/oculto [web:21]
                self.cursor_timer = 0  # Reinicia el contador [web:21]

            if self.cursor_visible:
                cursor_x = (
                    texto_rect.right + 2
                )  # Justo al lado del texto dibujado [web:21]
                cursor_y = (
                    self.rect.centery - 12
                )  # Altura coherente con la fuente usada [web:21]
                pygame.draw.line(
                    screen,
                    self.COLOR_TEXTO,
                    (cursor_x, cursor_y),
                    (cursor_x, cursor_y + 24),
                    2,
                )  # Línea vertical que simula el cursor [web:21]

    def obtener_texto(self):
        """Devuelve el texto escrito sin espacios al inicio o final."""
        return (
            self.texto.strip()
        )  # Útil para validar entradas sin espacios sobrantes [web:21]


class Boton:
    """Botón simple con hover y estado presionado.

    Cambia de color cuando pasas el mouse o lo presionas. No ejecuta la acción
    automáticamente; el código externo decide qué hacer cuando manejar_evento devuelve True.
    """

    def __init__(self, x, y, ancho, alto, texto, accion=None):
        self.rect = pygame.Rect(
            x, y, ancho, alto
        )  # Área del botón para colisiones y dibujo [web:21]
        self.texto = texto  # Etiqueta que se mostrará en el centro del botón [web:21]
        self.accion = accion  # Callback opcional (no se usa aquí directamente) [web:42]
        self.hover = False  # True si el mouse está encima del botón [web:21]
        self.presionado = False  # True mientras el mouse se mantiene presionando sobre el botón [web:21]

        # Colores por estado - Estilo arcade vibrante
        self.COLOR_NORMAL = (50, 60, 100)  # Estado sin interacción [web:42]
        self.COLOR_HOVER = (70, 90, 140)  # Cuando el mouse pasa por encima [web:42]
        self.COLOR_PRESIONADO = (
            30,
            40,
            70,
        )  # Mientras el botón del mouse está abajo [web:42]
        self.COLOR_TEXTO = (255, 255, 255)  # Texto normal [web:21]
        self.COLOR_TEXTO_HOVER = (255, 220, 60)  # Texto dorado en hover [web:42]
        self.COLOR_BORDE = (80, 100, 160)  # Borde base [web:42]
        self.COLOR_BORDE_HOVER = (0, 200, 255)  # Borde cyan brillante en hover [web:42]

        fuentes = GestorFuentes()
        self.font = (
            fuentes.texto_pequeño
        )  # Fuente pixel art para el botón (más pequeña) [web:21]

    def manejar_evento(self, evento, mouse_pos):
        """Actualiza estados con el mouse y detecta clics.

        - hover: se actualiza con la posición del mouse.
        - MOUSEBUTTONDOWN dentro del botón: marca presionado y devuelve True (para que actúes).
        - MOUSEBUTTONUP: suelta el estado presionado.
        """
        self.hover = self.rect.collidepoint(
            mouse_pos
        )  # Detecta si el mouse está encima del botón [web:21]

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.hover:
                self.presionado = (
                    True  # Entra en estado “presionado” hasta que sueltes [web:21]
                )
                return True  # Señal para que el llamador ejecute la acción deseada [web:21]

        if evento.type == pygame.MOUSEBUTTONUP:
            self.presionado = False  # Libera el estado “presionado” al soltar [web:21]

        return False  # No hubo click de interés en esta llamada [web:21]

    def dibujar(self, screen):
        """Dibuja el botón con su color según estado y el texto centrado."""
        # Elige el color de fondo según prioridad: presionado > hover > normal
        if self.presionado:
            color_fondo = self.COLOR_PRESIONADO  # Visual de click sostenido [web:42]
        elif self.hover:
            color_fondo = self.COLOR_HOVER  # Visual al pasar el mouse [web:42]
        else:
            color_fondo = self.COLOR_NORMAL  # Visual base [web:42]

        color_borde = self.COLOR_BORDE_HOVER if self.hover else self.COLOR_BORDE
        color_texto = self.COLOR_TEXTO_HOVER if self.hover else self.COLOR_TEXTO

        # Rectángulo estilo pixel art (sin bordes redondeados)
        pygame.draw.rect(screen, color_fondo, self.rect)
        pygame.draw.rect(screen, color_borde, self.rect, 2)

        # Efecto 3D pixel art
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
            color_sombra = tuple(max(0, c - 40) for c in color_fondo)
            pygame.draw.line(
                screen,
                color_sombra,
                (self.rect.left, self.rect.bottom - 1),
                (self.rect.right, self.rect.bottom - 1),
                2,
            )
            pygame.draw.line(
                screen,
                color_sombra,
                (self.rect.right - 1, self.rect.top),
                (self.rect.right - 1, self.rect.bottom),
                2,
            )

        # Texto centrado (sin antialiasing para efecto pixel)
        texto_surface = self.font.render(self.texto, False, color_texto)
        texto_rect = texto_surface.get_rect(center=self.rect.center)
        screen.blit(texto_surface, texto_rect)
