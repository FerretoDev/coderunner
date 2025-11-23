"""
Paleta de colores para Theseus Runner.
16 colores pixel art inspirados en el mito del Minotauro.
"""

# Paleta principal (16 colores)
PALETTE = {
    # Grises y neutros
    "NEGRO": (13, 13, 13),  # #0d0d0d
    "GRIS_OSCURO": (58, 58, 58),  # #3a3a3a
    "GRIS": (107, 107, 107),  # #6b6b6b
    "GRIS_CLARO": (160, 160, 160),  # #a0a0a0
    "BLANCO": (232, 232, 232),  # #e8e8e8
    # Piedras (laberinto)
    "PIEDRA_OSCURA": (74, 60, 46),  # #4a3c2e
    "PIEDRA": (107, 85, 68),  # #6b5544
    "PIEDRA_CLARA": (139, 115, 85),  # #8b7355
    # Rojos (Minotauro)
    "ROJO_OSCURO": (107, 32, 32),  # #6b2020
    "ROJO": (184, 50, 50),  # #b83232
    "ROJO_CLARO": (232, 80, 80),  # #e85050
    # Azules (Theseus)
    "AZUL_OSCURO": (42, 74, 107),  # #2a4a6b
    "AZUL": (64, 128, 192),  # #4080c0
    "AZUL_CLARO": (128, 176, 232),  # #80b0e8
    # Oro (objetos)
    "ORO": (212, 175, 55),  # #d4af37
}

# Paletas alternativas
PALETTE_NIGHT = {
    "NEGRO": (5, 5, 20),
    "GRIS_OSCURO": (20, 20, 40),
    "GRIS": (40, 40, 80),
    "GRIS_CLARO": (80, 80, 120),
    "BLANCO": (160, 160, 200),
    "PIEDRA_OSCURA": (30, 30, 50),
    "PIEDRA": (50, 50, 80),
    "PIEDRA_CLARA": (70, 70, 100),
    "ROJO_OSCURO": (80, 20, 40),
    "ROJO": (140, 40, 80),
    "ROJO_CLARO": (200, 80, 120),
    "AZUL_OSCURO": (20, 40, 80),
    "AZUL": (40, 80, 160),
    "AZUL_CLARO": (80, 120, 200),
    "ORO": (200, 180, 100),
}

PALETTE_LAVA = {
    "NEGRO": (20, 5, 5),
    "GRIS_OSCURO": (60, 30, 20),
    "GRIS": (100, 60, 40),
    "GRIS_CLARO": (140, 100, 80),
    "BLANCO": (255, 200, 180),
    "PIEDRA_OSCURA": (60, 30, 20),
    "PIEDRA": (100, 50, 30),
    "PIEDRA_CLARA": (140, 80, 50),
    "ROJO_OSCURO": (120, 40, 0),
    "ROJO": (200, 80, 20),
    "ROJO_CLARO": (255, 140, 60),
    "AZUL_OSCURO": (140, 60, 20),
    "AZUL": (200, 120, 60),
    "AZUL_CLARO": (255, 180, 120),
    "ORO": (255, 200, 60),
}

PALETTES = {
    "default": PALETTE,
    "night": PALETTE_NIGHT,
    "lava": PALETTE_LAVA,
}


def get_palette(name="default"):
    """Obtiene una paleta por nombre."""
    return PALETTES.get(name, PALETTE)
