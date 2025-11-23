"""
Módulo de componentes de interfaz.

Componentes reutilizables para la interfaz de usuario
(botones, inputs de texto, overlays, paneles, etc.).
"""

from .input_texto import Boton, InputTexto
from .overlay import Overlay, Panel

__all__ = ["Boton", "InputTexto", "Overlay", "Panel"]
