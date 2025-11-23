"""
Módulo de pantallas de la interfaz del juego.

Exporta todas las pantallas y modales para facilitar los imports.
"""

from .menu_principal import MenuPrincipal
from .mensaje_modal import MensajeModal
from .modal_confirmacion import ModalConfirmacion
from .pantalla_administracion import PantallaAdministracion
from .pantalla_carga_laberinto import PantallaCargaLaberinto
from .pantalla_iniciar_juego import PantallaIniciarJuego
from .pantalla_menu_administrador import PantallaMenuAdministrador
from .pantalla_salon_fama import PantallaSalonFama

__all__ = [
    "MenuPrincipal",
    "PantallaIniciarJuego",
    "PantallaSalonFama",
    "PantallaAdministracion",
    "MensajeModal",
    "PantallaMenuAdministrador",
    "PantallaCargaLaberinto",
    "ModalConfirmacion",
]
