import pygame

from .constantes import (
    ANIMATION_FRAMES,
    ANIMATION_SPEED,
    DOWN,
    LEFT,
    PLAYER_SIZE,
    PLAYER_SPEED,
    RIGHT,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    UP,
    load_image,
)


class Wall: ...


class Jugador:
    def __init__(self):
        # Posicion inicial del jugador (centro de la pantalla)
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2

        # Cargar sprite sheet de Minotauro
        self.sprite_sheet = load_image("PacMan.png")

        # Cargar todos los frames de animación
        self.animation_frames = []
        for i in range(ANIMATION_FRAMES):
            # Crear superficie para el frame
            frame = pygame.Surface((16, 16), pygame.SRCALPHA)
            # Copiar el frame desde el sprite sheet
            frame.blit(self.sprite_sheet, (0, 0), (i * 16, 0, 16, 16))
            # Escalar el frame al tamaño del jugador
            frame = pygame.transform.scale(frame, (PLAYER_SIZE, PLAYER_SIZE))
            self.animation_frames.append(frame)

        # Variable de animación
        self.current_frame = 0
        self.animation_timer = pygame.time.get_ticks()
        self.is_moving = False

        # Imagen actual del jugador
        self.original_image = self.animation_frames[0]
        self.image = self.original_image

        # Crear el rectángulo para colisiones y posicionamiento
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Dirección actual
        self.direction = RIGHT

        # deltas
        self.dx = 0
        self.dy = 0

        ## Util hasta que consiga los sprites correctos
        # Crear el rectángulo del jugador
        self.rect = pygame.Rect(
            self.x - PLAYER_SIZE // 2,  # Centrar el X
            self.y - PLAYER_SIZE // 2,  # Centrar el Y
            PLAYER_SIZE,
            PLAYER_SIZE,
        )

    def update_animation(self):
        """Actualizar la animación del jugador"""
        if not self.is_moving:
            self.current_frame = 0
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > ANIMATION_SPEED:
            self.current_frame = (self.current_frame + 1) % ANIMATION_FRAMES
            self.animation_timer = current_time

    def update_image(self):
        """Actualizar la imagen según la dirección y frame actual"""
        # Obtener el frame actual
        self.original_image = self.animation_frames[self.current_frame]

        # Actualizar la dirección basada en el movimiento horizontal
        if self.dx > 0:
            self.direction = RIGHT
            self.image = self.original_image
        elif self.dx < 0:
            self.direction = LEFT
            self.image = pygame.transform.flip(self.original_image, True, False)
        elif self.dy < 0:
            self.direction = UP
            self.image = pygame.transform.rotate(self.original_image, 90)
        elif self.dy > 0:
            self.direction = DOWN
            self.image = pygame.transform.rotate(self.original_image, -90)

    def move(self, dx, dy):
        """Mover el jugador según la entrada del usuario"""

        # Actualizar la posicion
        self.x += dx * PLAYER_SPEED
        self.y += dy * PLAYER_SPEED

        # Mantener al jugador dentro de los limites de la pantalla
        if self.x > SCREEN_WIDTH - PLAYER_SIZE:
            self.x = 0
        elif self.x < 0:
            self.x = SCREEN_WIDTH - PLAYER_SIZE

        if self.y > SCREEN_HEIGHT - PLAYER_SIZE:
            self.y = 0
        elif self.y < 0:
            self.y = SCREEN_HEIGHT - PLAYER_SIZE

        # Actualizar el rectángulo del jugador
        self.rect.center = (self.x, self.y)

        # Actualizar el rectángulo
        self.dx = dx
        self.dy = dy

        # Actualizar el estado de movimiento
        self.is_moving = self.dx != 0 or self.dy != 0

    def update(self):
        """Actualizar el estado del jugador"""
        self.update_animation()
        self.update_image()

    def draw(self, screen):
        """Dibujar el jugador en la pantalla"""
        pygame.draw.rect(screen, (255, 255, 0), self.rect)  # Dibujar en amarillo
        # screen.blit(self.image, self.rect)
