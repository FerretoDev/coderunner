"""
Módulo de componentes de interfaz.

Componentes reutilizables para la interfaz de usuario
(botones, inputs de texto, overlays, paneles, etc.).
"""

from .input_texto import InputTexto
from .input_texto import Boton as BotonLegacy  # Mantener compatibilidad
from .overlay import Overlay
from .overlay import Panel as PanelLegacy  # Mantener compatibilidad

# Nuevos componentes pixel art
from .boton import Boton
from .panel import Panel
from .barra_vida import BarraVida
from .hud import HUD

__all__ = [
    # Legacy
    "BotonLegacy",
    "InputTexto",
    "Overlay",
    "PanelLegacy",
    # Nuevos componentes
    "Boton",
    "Panel",
    "BarraVida",
    "HUD",
]
