import sys

import pygame

from .constantes import BLACK, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE
from .sprites import Jugador


class Juego:
    def __init__(self):
        # Inicializar Pygame
        pygame.init()

        # Crear ventana
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("CodeRunner - Pruebas Pacman")  #

        # Reloj para controlar la velocidad del juego
        self.clock = pygame.time.Clock()

        # Variable para controlar el bucle del juego
        self.running = True

        # Crear el jugador
        self.player = Jugador()

    def handle_events(self):
        """Manejar eventos de Pygame"""
        for event in pygame.event.get():
            # Si el usuario cierra la ventana
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        """Actualizar el estado del juego"""
        # Obtener las teclas presionadas
        keys = pygame.key.get_pressed()

        # Calcular el movimiento basado en las teclas presionadas
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]

        # Mover el jugador
        self.player.move(dx, dy)

        # Actualizar el jugador
        self.player.update()

    def draw(self):
        """Dibujar en la pantalla"""
        # Llenar la pantalla con color negro
        self.screen.fill(BLACK)

        # Dibujar el jugador
        self.player.draw(self.screen)

        # Actualizar la pantalla
        pygame.display.flip()

    def run(self):
        """Bucle principal del juego"""
        while self.running:
            self.handle_events()  # Procesar eventos
            self.update()  # Actualizar estado
            self.draw()  # Dibujar en pantalla
            self.clock.tick(60)  # Limitar a 60 FPS

        # Cierra Pygame al terminar el bucle
        pygame.quit()
        sys.exit()
