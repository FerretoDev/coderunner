"""
Paleta de colores centralizada del juego.

Define todos los colores usados en la interfaz para facilitar
cambios de tema y mantener consistencia visual.
"""


class PaletaColores:
    """Paleta de colores del juego."""

    # Colores de fondo
    FONDO_PRINCIPAL = (20, 20, 30)
    FONDO_SECUNDARIO = (30, 30, 40)
    FONDO_MODAL = (40, 40, 60)
    FONDO_OVERLAY = (0, 0, 0)

    # Colores de texto
    TEXTO_PRINCIPAL = (255, 255, 255)
    TEXTO_SECUNDARIO = (200, 200, 200)
    TEXTO_DESACTIVADO = (150, 150, 150)
    TEXTO_PLACEHOLDER = (120, 120, 140)
    TEXTO_SOMBRA = (10, 10, 20)

    # Colores de acento
    ACENTO_PRINCIPAL = (0, 150, 255)  # Azul
    ACENTO_SUCCESS = (0, 200, 100)  # Verde
    ACENTO_ERROR = (255, 50, 50)  # Rojo
    ACENTO_WARNING = (255, 200, 0)  # Amarillo
    ACENTO_INFO = (100, 150, 255)  # Azul claro

    # Colores especiales
    ORO = (255, 215, 0)
    PLATA = (192, 192, 192)
    BRONCE = (205, 127, 50)

    # Colores de UI
    BORDE_NORMAL = (100, 100, 120)
    BORDE_ACTIVO = (0, 150, 255)
    BORDE_HOVER = (120, 170, 255)

    # Colores de botones
    BOTON_NORMAL = (70, 70, 90)
    BOTON_HOVER = (90, 90, 110)
    BOTON_PRESIONADO = (50, 50, 70)

    # Colores de input
    INPUT_INACTIVO = (70, 70, 90)
    INPUT_ACTIVO = (100, 100, 130)

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
