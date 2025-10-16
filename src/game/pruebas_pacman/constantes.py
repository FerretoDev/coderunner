import os

import pygame

# Configuración de la ventana
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Configuración del jugador
PLAYER_SIZE = 30  # Tamaño del cuadrado del jugador
PLAYER_SPEED = 5  # Velocidad de movimiento del jugador
ANIMATION_SPEED = 100  # Velocidad de la animación del jugador
ANIMATION_FRAMES = 8  # Número de frames en la animación del jugador

# Direcciones
RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)  # Color del jugador


# Funcion para cargar imágenes
def load_image(name):
    """Cargar una imagen desde la carpeta de assets"""
    return pygame.image.load(
        os.path.join("src", "assets", "imagenes", name)
    ).convert_alpha()
