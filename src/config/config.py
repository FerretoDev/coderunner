"""
Configuración centralizada del juego.

Todas las constantes del juego en un solo lugar para fácil ajuste y mantenimiento.
"""


class ConfigJuego:
    """Configuración general del juego"""

    # === VENTANA ===
    # None = se adapta al tamaño del monitor automáticamente
    ANCHO_VENTANA = None  # Se calcula dinámicamente
    ALTO_VENTANA = None  # Se calcula dinámicamente
    FPS = 60
    TITULO = "Theseus Runner"
    FULLSCREEN = False  # True para pantalla completa, False para ventana

    # === LABERINTO ===
    TAM_CELDA = 32  # Tamaño de cada celda en píxeles

    # === TIEMPO Y DURACIÓN ===
    SEGUNDOS_ESPERA_GAME_OVER = 5  # Segundos antes de poder salir del game over
    SEGUNDOS_VIDA_OBSEQUIO = 10  # Segundos antes de que un obsequio desaparezca
    FRAMES_COOLDOWN_MOVIMIENTO = 8  # Frames de espera entre movimientos por celda

    # === DIFICULTAD PROGRESIVA ===
    VELOCIDAD_INICIAL_ENEMIGO = 1.5
    INCREMENTO_VELOCIDAD = 0.2
    SEGUNDOS_INCREMENTO_VELOCIDAD = 10

    # === JUGADOR ===
    VIDAS_INICIALES = 3
    VELOCIDAD_JUGADOR = 4
    RADIO_JUGADOR = 12

    # === ENEMIGO ===
    RADIO_ENEMIGO = 12
    FRAMES_RECALCULO_BFS = 6  # Cada cuántos frames recalcular pathfinding
    MARGEN_CAPTURA = 5  # Píxeles de holgura para capturar

    # === OBSEQUIOS ===
    VALOR_OBSEQUIO_DEFAULT = 10
    RADIO_OBSEQUIO_BASE = 8

    # === FÍSICA Y COLISIONES ===
    # Factor de ajuste del rect de colisión respecto al radio visual
    # Un valor de 1.8 hace que el rect sea 90% del diámetro visual (más preciso)
    FACTOR_RECT_COLISION = 1.8

    # Factores para movimientos alternativos en pathfinding legacy
    FACTOR_DIAGONAL = 0.7  # Para movimientos diagonales (sqrt(2)/2 ≈ 0.707)

    # === CONVERSIÓN TIEMPO ===
    @staticmethod
    def segundos_a_frames(segundos: int) -> int:
        """Convierte segundos a frames a 60 FPS"""
        return segundos * 60

    @staticmethod
    def frames_a_segundos(frames: int) -> int:
        """Convierte frames a segundos"""
        return frames // 60


class Colores:
    """Paleta de colores del juego - Estilo Pixel Art Vibrante"""

    # === FONDO Y BASE ===
    FONDO = (15, 15, 35)
    HUD_FONDO = (25, 30, 55)

    # === LABERINTO ===
    PARED = (70, 85, 120)
    PISO = (35, 40, 60)
    BORDE_CELDA = (120, 140, 180)

    # === PERSONAJES ===
    JUGADOR = (50, 200, 255)  # Cyan brillante
    ENEMIGO = (255, 60, 80)  # Rojo neón

    # === UI Y TEXTO ===
    TEXTO = (255, 255, 255)
    TEXTO_SECUNDARIO = (180, 200, 255)
    ACENTO = (0, 200, 255)  # Cyan eléctrico

    # === ESTADOS ===
    VIDAS = (255, 80, 120)  # Rosa neón
    PUNTAJE = (255, 220, 60)  # Dorado brillante

    # === OBSEQUIOS ===
    OBSEQUIO_EXTERIOR = (255, 240, 100)
    OBSEQUIO_PRINCIPAL = (255, 215, 0)
    OBSEQUIO_BRILLO = (255, 255, 150)
    OBSEQUIO_DESTELLO = (255, 255, 255)

    # === OVERLAYS ===
    OVERLAY_OSCURO = (0, 0, 0)
    BLANCO = (255, 255, 255)


class Direcciones:
    """Mapeo de direcciones y sus deltas"""

    ARRIBA = "arriba"
    ABAJO = "abajo"
    IZQUIERDA = "izquierda"
    DERECHA = "derecha"

    # Delta de movimiento (dx, dy) para cada dirección
    DELTAS: dict[str, tuple[int, int]] = {
        ARRIBA: (0, -1),
        ABAJO: (0, 1),
        IZQUIERDA: (-1, 0),
        DERECHA: (1, 0),
    }

    @classmethod
    def obtener_delta(cls, direccion: str) -> tuple[int, int]:
        """Retorna el delta (dx, dy) para una dirección"""
        return cls.DELTAS.get(direccion, (0, 0))
