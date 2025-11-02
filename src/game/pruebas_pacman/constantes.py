"""
Constantes y utilidades básicas para Pygame.

Incluye:
- Tamaño de ventana y colores comunes.
- Parámetros del jugador (tamaño, velocidad y animación).
- Función para cargar imágenes desde la carpeta de assets.
"""
import os  # Manejo de rutas y archivos del sistema operativo [web:60]
import pygame  # Librería de juegos para cargar imágenes y dibujar en pantalla [web:47]

# Configuración de la ventana
SCREEN_WIDTH = 800  # Ancho de la ventana principal en píxeles [web:61]
SCREEN_HEIGHT = 600  # Alto de la ventana principal en píxeles [web:61]

# Configuración del jugador
PLAYER_SIZE = 30  # Tamaño del cuadrado del jugador en píxeles [web:61]
PLAYER_SPEED = 5  # Cuántos píxeles se mueve por actualización (velocidad base) [web:61]
ANIMATION_SPEED = 100  # Milisegundos entre frames de la animación del jugador [web:58]
ANIMATION_FRAMES = 8  # Cuántos frames tiene el ciclo de animación del jugador [web:55]

# Direcciones (útiles para lógica de movimiento/animación)
RIGHT = 0  # Derecha [web:61]
LEFT = 1  # Izquierda [web:61]
UP = 2  # Arriba [web:61]
DOWN = 3  # Abajo [web:61]

# Colores en formato RGB
BLACK = (0, 0, 0)  # Negro para fondos o texto [web:61]
WHITE = (255, 255, 255)  # Blanco para fondos o texto [web:61]
YELLOW = (255, 255, 0)  # Amarillo, por ejemplo para el jugador [web:61]

def load_image(name):
    """Carga una imagen desde src/assets/imagenes y la prepara con alpha.

    Usa os.path.join para crear la ruta de forma compatible en Windows, macOS y Linux.
    Convierte la imagen con convert_alpha() para habilitar transparencias y optimizar
    el formato de píxeles según la pantalla.

    Args:
        name (str): Nombre del archivo de imagen, por ejemplo 'jugador.png'. [web:58]

    Returns:
        pygame.Surface: Superficie lista para dibujar con canal alpha. [web:47]

    Nota:
        convert_alpha() requiere que la pantalla principal exista (pygame.display.set_mode)
        para convertir al formato correcto; haz esa llamada antes de cargar imágenes. [web:48]
    """
    ruta = os.path.join("src", "assets", "imagenes", name)  # Construye la ruta sin problemas de separadores [web:60]
    imagen = pygame.image.load(ruta)  # Carga la imagen como una Surface desde disco [web:47]
    return imagen.convert_alpha()  # Convierte para transparencia y mejor rendimiento al dibujar [web:53]
