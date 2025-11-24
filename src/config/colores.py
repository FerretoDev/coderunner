"""
Paleta de colores centralizada del juego - Estilo Pixel Art Retro.

Define todos los colores usados en la interfaz para facilitar
cambios de tema y mantener consistencia visual.
Inspirada en paletas retro de 8-bit y 16-bit.
"""


class PaletaColores:
    """Paleta de colores del juego - Estética Pixel Art."""

    # Colores de fondo - Tonos oscuros pero vibrantes
    FONDO_PRINCIPAL = (15, 15, 35)
    FONDO_SECUNDARIO = (25, 25, 45)
    FONDO_MODAL = (30, 30, 60)
    FONDO_OVERLAY = (0, 0, 0)

    # Colores de texto - Alta saturación
    TEXTO_PRINCIPAL = (255, 255, 255)
    TEXTO_SECUNDARIO = (200, 220, 255)
    TEXTO_DESACTIVADO = (120, 140, 180)
    TEXTO_PLACEHOLDER = (100, 120, 160)
    TEXTO_SOMBRA = (0, 0, 20)

    # Colores de acento - Vibrantes estilo retro
    ACENTO_PRINCIPAL = (0, 200, 255)  # Cyan brillante
    ACENTO_SUCCESS = (50, 255, 100)  # Verde neón
    ACENTO_ERROR = (255, 60, 60)  # Rojo brillante
    ACENTO_WARNING = (255, 220, 0)  # Amarillo dorado
    ACENTO_INFO = (120, 180, 255)  # Azul cielo

    # Colores especiales - Metálicos pixel
    ORO = (255, 220, 60)
    PLATA = (220, 220, 240)
    BRONCE = (220, 140, 60)

    # Colores de UI - Estilo arcade
    BORDE_NORMAL = (80, 100, 160)
    BORDE_ACTIVO = (0, 200, 255)
    BORDE_HOVER = (100, 220, 255)

    # Colores de botones - Gradientes simulados
    BOTON_NORMAL = (50, 60, 100)
    BOTON_HOVER = (70, 90, 140)
    BOTON_PRESIONADO = (30, 40, 70)

    # Colores de input
    INPUT_INACTIVO = (40, 50, 80)
    INPUT_ACTIVO = (60, 80, 120)

    # Colores adicionales pixel art
    PIXEL_SOMBRA = (10, 10, 25)
    PIXEL_LUZ = (180, 200, 255)
    PIXEL_GRID = (40, 40, 70)

    @classmethod
    def obtener_color_tipo(cls, tipo):
        """
        Obtiene color según el tipo de mensaje.

        Args:
            tipo: 'info', 'success', 'error', 'warning'

        Returns:
            Color RGB correspondiente
        """
        colores = {
            "info": cls.ACENTO_INFO,
            "success": cls.ACENTO_SUCCESS,
            "error": cls.ACENTO_ERROR,
            "warning": cls.ACENTO_WARNING,
        }
        return colores.get(tipo, cls.ACENTO_PRINCIPAL)
