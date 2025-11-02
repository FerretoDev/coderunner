import pygame  # Librería para gráficos, eventos y tiempo en juegos 2D [web:47]

from .constantes import (
    ANIMATION_FRAMES,  # Total de frames en la animación del sprite [web:61]
    ANIMATION_SPEED,   # Milisegundos entre cambios de frame [web:58]
    DOWN,              # Constante para dirección abajo [web:61]
    LEFT,              # Constante para dirección izquierda [web:61]
    PLAYER_SIZE,       # Tamaño en píxeles del jugador en pantalla [web:61]
    PLAYER_SPEED,      # Velocidad base de movimiento del jugador [web:61]
    RIGHT,             # Constante para dirección derecha [web:61]
    SCREEN_HEIGHT,     # Alto de la ventana para limitar posición [web:61]
    SCREEN_WIDTH,      # Ancho de la ventana para limitar posición [web:61]
    UP,                # Constante para dirección arriba [web:61]
    load_image,        # Utilidad para cargar imágenes con alpha [web:47]
)  # Importa constantes y la función de carga de imágenes desde el módulo de utilidades [web:61]


class Wall:
    """Placeholder para futuras paredes/colisiones (no implementado aún)."""  # Docstring breve para indicar estado actual [web:61]
    ...
    # Cuando se implementen paredes, aquí irán su rect y lógica de colisiones [web:61]


class Jugador:
    """Controla posición, animación y dibujo del jugador.

    - Usa un sprite sheet de 16x16 por frame y lo escala a PLAYER_SIZE. [web:49]
    - Anima en función del tiempo con pygame.time.get_ticks y ANIMATION_SPEED. [web:47]
    - Cambia la imagen según la dirección usando flip/rotate para reutilizar frames. [web:47]
    """

    def __init__(self):
        # Posición inicial en el centro de la pantalla para empezar visible
        self.x = SCREEN_WIDTH // 2  # Mitad del ancho de la ventana [web:61]
        self.y = SCREEN_HEIGHT // 2  # Mitad del alto de la ventana [web:61]

        # Cargar sprite sheet (debe existir en assets); usa convert_alpha internamente
        self.sprite_sheet = load_image("PacMan.png")  # Superficie con todos los frames en fila [web:47]

        # Extraer todos los frames del sprite sheet y escalarlos al tamaño deseado
        self.animation_frames = []  # Lista donde guardaremos cada frame ya escalado [web:49]
        for i in range(ANIMATION_FRAMES):  # Recorre cada índice de frame disponible [web:58]
            frame = pygame.Surface((16, 16), pygame.SRCALPHA)  # Superficie con alpha para recorte limpio [web:51]
            frame.blit(self.sprite_sheet, (0, 0), (i * 16, 0, 16, 16))  # Copia un trozo del sheet según i [web:47]
            frame = pygame.transform.scale(frame, (PLAYER_SIZE, PLAYER_SIZE))  # Escala al tamaño en pantalla [web:47]
            self.animation_frames.append(frame)  # Agrega el frame listo para usar en animación [web:49]

        # Control de animación basado en tiempo
        self.current_frame = 0  # Índice del frame actual que se mostrará [web:58]
        self.animation_timer = pygame.time.get_ticks()  # Marca de tiempo del último cambio de frame [web:47]
        self.is_moving = False  # Si el jugador se está moviendo, avanza la animación [web:61]

        # Imagen actual a partir del primer frame; se irá cambiando en update_image
        self.original_image = self.animation_frames[0]  # Guarda el frame base sin rotar/flip [web:47]
        self.image = self.original_image  # Imagen mostrada tras aplicar dirección [web:47]

        # Rect para posicionar y detectar colisiones; centrado en (x, y)
        self.rect = self.image.get_rect(center=(self.x, self.y))  # Facilita blit/draw centrado [web:47]

        # Dirección actual por defecto hacia la derecha
        self.direction = RIGHT  # Se actualizará según dx/dy en cada movimiento [web:61]

        # Último vector de movimiento aplicado (se usa para decidir dirección y animación)
        self.dx = 0  # Desplazamiento horizontal del último update [web:61]
        self.dy = 0  # Desplazamiento vertical del último update [web:61]

        # Rect centrado con tamaño fijo, útil si aún no se usan las imágenes reales del sprite
        self.rect = pygame.Rect(  # Rect manual para dibujar un placeholder amarillo coherente con tamaño [web:47]
            self.x - PLAYER_SIZE // 2,  # Ajuste para centrar en X según tamaño [web:61]
            self.y - PLAYER_SIZE // 2,  # Ajuste para centrar en Y según tamaño [web:61]
            PLAYER_SIZE,  # Ancho del jugador en píxeles [web:61]
            PLAYER_SIZE,  # Alto del jugador en píxeles [web:61]
        )  # Se mantiene para que el rect de colisión coincida con el cuadrado amarillo actual [web:61]

    def update_animation(self):
        """Avanza o reinicia la animación según si hay movimiento y el tiempo transcurrido."""  # Explica la condición de animar [web:58]
        if not self.is_moving:  # Si no se mueve, mostrar el primer frame (idle simple) [web:61]
            self.current_frame = 0  # Vuelve al frame base para “quieto” [web:58]
            return  # Sale sin cambiar el timer para no consumir lógica extra [web:61]

        current_time = pygame.time.get_ticks()  # Tiempo actual en ms desde que inició Pygame [web:47]
        if current_time - self.animation_timer > ANIMATION_SPEED:  # ¿Pasó el intervalo para cambiar frame? [web:58]
            self.current_frame = (self.current_frame + 1) % ANIMATION_FRAMES  # Avanza y cicla la animación [web:58]
            self.animation_timer = current_time  # Actualiza la marca de tiempo del último cambio [web:47]

    def update_image(self):
        """Actualiza la imagen visible según el frame y la dirección actual."""  # Describe cómo se elige la imagen [web:47]
        self.original_image = self.animation_frames[self.current_frame]  # Toma el frame base sin transformaciones [web:47]

        # Decide la orientación a partir del último movimiento: derecha/izquierda con flip, arriba/abajo con rotación
        if self.dx > 0:  # Movimiento hacia la derecha [web:61]
            self.direction = RIGHT  # Guarda la dirección para otras lógicas si hiciera falta [web:61]
            self.image = self.original_image  # Derecha no requiere transformar el frame base [web:47]
        elif self.dx < 0:  # Movimiento hacia la izquierda [web:61]
            self.direction = LEFT  # Actualiza dirección actual [web:61]
            self.image = pygame.transform.flip(self.original_image, True, False)  # Espeja horizontalmente [web:47]
        elif self.dy < 0:  # Movimiento hacia arriba [web:61]
            self.direction = UP  # Actualiza dirección actual [web:61]
            self.image = pygame.transform.rotate(self.original_image, 90)  # Rota 90° para apuntar hacia arriba [web:47]
        elif self.dy > 0:  # Movimiento hacia abajo [web:61]
            self.direction = DOWN  # Actualiza dirección actual [web:61]
            self.image = pygame.transform.rotate(self.original_image, -90)  # Rota -90° para apuntar hacia abajo [web:47]

    def move(self, dx, dy):
        """Aplica el movimiento según la entrada y limita en pantalla con wrap sencillo."""  # Explica la mecánica de movimiento [web:61]
        # Cambia la posición sumando velocidad por dirección; dx/dy suelen ser -1, 0 o 1
        self.x += dx * PLAYER_SPEED  # Desplaza en X en función de la velocidad base [web:61]
        self.y += dy * PLAYER_SPEED  # Desplaza en Y en función de la velocidad base [web:61]

        # Teletransporte en bordes: si sale por un lado, entra por el opuesto (efecto túnel)
        if self.x > SCREEN_WIDTH - PLAYER_SIZE:  # Se pasó del límite derecho [web:61]
            self.x = 0  # Aparece en el borde izquierdo [web:61]
        elif self.x < 0:  # Se pasó del límite izquierdo [web:61]
            self.x = SCREEN_WIDTH - PLAYER_SIZE  # Aparece en el borde derecho [web:61]

        if self.y > SCREEN_HEIGHT - PLAYER_SIZE:  # Se pasó del límite inferior [web:61]
            self.y = 0  # Aparece arriba [web:61]
        elif self.y < 0:  # Se pasó del límite superior [web:61]
            self.y = SCREEN_HEIGHT - PLAYER_SIZE  # Aparece abajo [web:61]

        # Actualiza el rect para que coincida con la nueva posición al centro
        self.rect.center = (self.x, self.y)  # Mantiene colisiones y dibujo coherentes con la posición [web:47]

        # Guarda los últimos deltas para orientar el sprite y decidir si anima
        self.dx = dx  # Último delta horizontal aplicado [web:61]
        self.dy = dy  # Último delta vertical aplicado [web:61]
        self.is_moving = self.dx != 0 or self.dy != 0  # Verdadero si hay movimiento en cualquier eje [web:61]

    def update(self):
        """Actualiza animación e imagen en cada frame del juego."""  # Resume el ciclo de actualización del jugador [web:61]
        self.update_animation()  # Avanza la animación si corresponde según el tiempo y movimiento [web:58]
        self.update_image()  # Ajusta la imagen y orientación para este frame [web:47]

    def draw(self, screen):
        """Dibuja al jugador: actualmente un rectángulo amarillo como placeholder."""  # Indica el estado temporal del render [web:61]
        pygame.draw.rect(screen, (255, 255, 0), self.rect)  # Visual simple para ver posición y tamaño [web:61]
        # Si ya quieres usar el sprite animado, descomenta la línea de abajo y comenta el rectángulo. [web:47]
        # screen.blit(self.image, self.rect)  # Dibuja el frame actual orientado según la dirección [web:47]
