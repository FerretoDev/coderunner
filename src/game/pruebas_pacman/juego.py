"""
Bucle principal del juego con Pygame.

Responsabilidades:
- Inicializar Pygame y crear la ventana.
- Gestionar eventos, actualizar estado del jugador y dibujar cada frame.
- Mantener un límite de FPS estable con un reloj.
"""
import sys  # Para salir limpiamente de la app al finalizar [web:61]
import pygame  # Motor de eventos, ventana y dibujo 2D [web:47]

from .constantes import BLACK, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE  # Configuración básica y colores [web:61]
from .sprites import Jugador  # Clase del jugador con métodos move, update y draw [web:61]


class Juego:
    """Contenedor del juego: maneja ventana, bucle y ciclo de vida."""

    def __init__(self):
        # Inicializar Pygame y sus módulos (ventana, fuentes, etc.)
        pygame.init()  # Debe llamarse antes de usar display o eventos [web:61]

        # Crear ventana con el tamaño definido en constantes
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Superficie principal de dibujo [web:61]
        pygame.display.set_caption("CodeRunner - Pruebas Pacman")  # Título de la ventana [web:61]

        # Reloj para limitar FPS y medir tiempo entre frames
        self.clock = pygame.time.Clock()  # Control de tiempo y FPS estables [web:61]

        # Bandera para mantener o salir del bucle principal
        self.running = True  # Cuando pase a False, termina el juego [web:61]

        # Crear el jugador (debe implementar move(dx, dy), update() y draw(screen))
        self.player = Jugador()  # Instancia del jugador con su propia lógica de sprite [web:61]

    def handle_events(self):
        """Lee la cola de eventos y aplica acciones básicas (cerrar ventana)."""
        for event in pygame.event.get():  # Obtiene todos los eventos pendientes [web:61]
            if event.type == pygame.QUIT:  # Cerrar la ventana (click en la X o similar) [web:61]
                self.running = False  # Señal para salir del bucle principal [web:61]

    def update(self):
        """Actualiza el estado del juego y del jugador."""
        keys = pygame.key.get_pressed()  # Mapa de teclas actualmente presionadas [web:61]

        # Movimiento simple con flechas: derecha/izquierda y abajo/arriba
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]  # 1, 0 o -1 según teclas pulsadas [web:61]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]  # 1, 0 o -1 para el eje vertical [web:61]

        self.player.move(dx, dy)  # Pasa el vector de dirección al jugador (la clase decide la velocidad real) [web:61]
        self.player.update()  # Permite animaciones, física o límites dentro del propio jugador [web:61]

    def draw(self):
        """Dibuja la escena del frame actual en pantalla."""
        self.screen.fill(BLACK)  # Limpia el frame con fondo negro para evitar arrastres de dibujo [web:61]
        self.player.draw(self.screen)  # Dibuja al jugador en su posición y estado actuales [web:61]
        pygame.display.flip()  # Intercambia buffers: muestra todo lo dibujado en este frame [web:61]

    def run(self):
        """Ejecuta el bucle principal del juego hasta que se cierre la ventana."""
        while self.running:  # Bucle de juego clásico: eventos → lógica → render [web:61]
            self.handle_events()  # Leer y manejar entradas del usuario y sistema [web:61]
            self.update()  # Actualizar posiciones, animaciones y lógica [web:61]
            self.draw()  # Dibujar la escena actual [web:61]
            self.clock.tick(60)  # Limitar a 60 FPS para estabilidad y consumo razonable [web:61]

        # Salida limpia al terminar el bucle
        pygame.quit()  # Libera recursos de Pygame (ventana, audio, etc.) [web:61]
        sys.exit()  # Termina el proceso de la app de forma explícita [web:61]
