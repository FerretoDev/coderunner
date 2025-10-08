import pygame


class InputTexto:
    """Input de texto visual (como <input> en HTML)"""

    def __init__(self, x, y, ancho, alto, placeholder=""):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = ""
        self.placeholder = placeholder
        self.activo = False
        self.cursor_visible = True
        self.cursor_timer = 0

        # Colores
        self.COLOR_INACTIVO = (70, 70, 90)
        self.COLOR_ACTIVO = (100, 100, 130)
        self.COLOR_TEXTO = (255, 255, 255)
        self.COLOR_PLACEHOLDER = (150, 150, 150)
        self.COLOR_BORDE = (100, 100, 120)
        self.COLOR_BORDE_ACTIVO = (0, 150, 255)

        self.font = pygame.font.Font(None, 32)

    def manejar_evento(self, evento):
        """Maneja eventos del input"""
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # Activar/desactivar si se hace click
            self.activo = self.rect.collidepoint(evento.pos)

        if evento.type == pygame.KEYDOWN and self.activo:
            if evento.key == pygame.K_RETURN:
                return True  # Enter presionado
            elif evento.key == pygame.K_BACKSPACE:
                self.texto = self.texto[:-1]
            else:
                # Agregar carácter (límite de 20 caracteres)
                if len(self.texto) < 20:
                    self.texto += evento.unicode

        return False

    def dibujar(self, screen):
        """Dibuja el input"""
        # Color según estado
        color_fondo = self.COLOR_ACTIVO if self.activo else self.COLOR_INACTIVO
        color_borde = self.COLOR_BORDE_ACTIVO if self.activo else self.COLOR_BORDE

        # Fondo del input
        pygame.draw.rect(screen, color_fondo, self.rect, border_radius=8)
        pygame.draw.rect(screen, color_borde, self.rect, 2, border_radius=8)

        # Texto o placeholder
        if self.texto:
            texto_surface = self.font.render(self.texto, True, self.COLOR_TEXTO)
        else:
            texto_surface = self.font.render(self.placeholder, True, self.COLOR_PLACEHOLDER)

        # Posicionar texto
        texto_rect = texto_surface.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        screen.blit(texto_surface, texto_rect)

        # Cursor parpadeante
        if self.activo:
            self.cursor_timer += 1
            if self.cursor_timer > 30:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0

            if self.cursor_visible:
                cursor_x = texto_rect.right + 2
                cursor_y = self.rect.centery - 12
                pygame.draw.line(screen, self.COLOR_TEXTO,
                                 (cursor_x, cursor_y),
                                 (cursor_x, cursor_y + 24), 2)

    def obtener_texto(self):
        """Retorna el texto ingresado"""
        return self.texto.strip()


class Boton:
    """Botón reutilizable"""

    def __init__(self, x, y, ancho, alto, texto, accion=None):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.accion = accion
        self.hover = False
        self.presionado = False

        # Colores
        self.COLOR_NORMAL = (70, 70, 90)
        self.COLOR_HOVER = (100, 100, 130)
        self.COLOR_PRESIONADO = (120, 120, 160)
        self.COLOR_TEXTO = (255, 255, 255)
        self.COLOR_TEXTO_HOVER = (255, 255, 100)
        self.COLOR_BORDE = (100, 100, 120)
        self.COLOR_BORDE_HOVER = (0, 150, 255)

        self.font = pygame.font.Font(None, 36)

    def manejar_evento(self, evento, mouse_pos):
        """Maneja eventos del botón"""
        self.hover = self.rect.collidepoint(mouse_pos)

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.hover:
                self.presionado = True
                return True

        if evento.type == pygame.MOUSEBUTTONUP:
            self.presionado = False

        return False

    def dibujar(self, screen):
        """Dibuja el botón"""
        # Determinar color
        if self.presionado:
            color_fondo = self.COLOR_PRESIONADO
        elif self.hover:
            color_fondo = self.COLOR_HOVER
        else:
            color_fondo = self.COLOR_NORMAL

        color_borde = self.COLOR_BORDE_HOVER if self.hover else self.COLOR_BORDE
        color_texto = self.COLOR_TEXTO_HOVER if self.hover else self.COLOR_TEXTO

        # Dibujar fondo
        pygame.draw.rect(screen, color_fondo, self.rect, border_radius=10)
        pygame.draw.rect(screen, color_borde, self.rect, 2, border_radius=10)

        # Texto
        texto_surface = self.font.render(self.texto, True, color_texto)
        texto_rect = texto_surface.get_rect(center=self.rect.center)
        screen.blit(texto_surface, texto_rect)