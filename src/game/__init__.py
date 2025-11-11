"""
Importa las pantallas de la interfaz gráfica.

Incluye:
- MenuPrincipal: pantalla inicial con opciones.
- PantallaAdministracion: gestión de datos/opciones de admin.
- PantallaIniciarJuego: pantalla de inicio/selección para jugar.
- PantallaSalonFama: muestra puntajes o récords.
"""

# Import relativo de las pantallas desde el paquete interfaz
from .interfaz import (
    MenuPrincipal,          # Menú de entrada a las demás pantallas
    PantallaAdministracion, # Opciones y administración del juego
    PantallaIniciarJuego,   # Preparación y arranque del juego
    PantallaSalonFama,      # Tabla de puntuaciones destacadas
)
