"""
Paleta de colores UI basada en juegos retro clásicos.
Referencias: Zelda Minish Cap, Castlevania, Shovel Knight, Hyper Light Drifter.
"""

# Colores base oscuros/claros
UI_DARK = (26, 28, 44)  # #1a1c2c - Fondo oscuro estilo Dead Cells
UI_GRAY = (93, 93, 129)  # #5d5d81 - Sombras estilo Zelda GBA
UI_LIGHT = (196, 196, 212)  # #c4c4d4 - Bordes claros estilo Shovel Knight
UI_WHITE = (244, 244, 244)  # #f4f4f4 - Highlights universal retro

# Dorado (Castlevania)
UI_GOLD = (255, 215, 0)  # #ffd700 - Marcos dorados
UI_GOLD_DARK = (184, 134, 11)  # #b8860b - Sombras doradas

# Azul (Hyper Light Drifter)
UI_BLUE = (59, 93, 201)  # #3b5dc9 - Azul primario
UI_BLUE_LIGHT = (65, 166, 246)  # #41a6f6 - Azul claro iconos activos

# Rojo (vida/peligro)
UI_RED = (204, 51, 51)  # #cc3333 - Vida baja universal
UI_RED_DARK = (139, 37, 40)  # #8b2528 - Sombras rojas

# Verde (vida/salud)
UI_GREEN = (56, 183, 100)  # #38b764 - Vida completa estilo Zelda
UI_GREEN_DARK = (37, 113, 121)  # #257179 - Sombras verdes

# Transparencia
TRANSPARENT = (0, 0, 0, 0)


class PaletaUI:
    """Clase contenedora de la paleta UI para fácil acceso."""

    # Colores base
    DARK = UI_DARK
    GRAY = UI_GRAY
    LIGHT = UI_LIGHT
    WHITE = UI_WHITE

    # Dorado
    GOLD = UI_GOLD
    GOLD_DARK = UI_GOLD_DARK

    # Azul
    BLUE = UI_BLUE
    BLUE_LIGHT = UI_BLUE_LIGHT

    # Rojo
    RED = UI_RED
    RED_DARK = UI_RED_DARK

    # Verde
    GREEN = UI_GREEN
    GREEN_DARK = UI_GREEN_DARK

    # Estados de botones
    BUTTON_NORMAL = UI_BLUE
    BUTTON_HOVER = UI_BLUE_LIGHT
    BUTTON_PRESSED = UI_DARK
    BUTTON_DISABLED = UI_GRAY

    # Estados de vida
    HEALTH_FULL = UI_GREEN
    HEALTH_MEDIUM = UI_GOLD
    HEALTH_LOW = UI_RED

    @classmethod
    def obtener_color_vida(cls, porcentaje):
        """
        Retorna el color apropiado según el porcentaje de vida.

        Args:
            porcentaje: float entre 0.0 y 1.0

        Returns:
            tuple: Color RGB
        """
        if porcentaje > 0.5:
            return cls.HEALTH_FULL
        elif porcentaje > 0.25:
            return cls.HEALTH_MEDIUM
        else:
            return cls.HEALTH_LOW
