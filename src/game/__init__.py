"""
Importa las pantallas de la interfaz gráfica.

Incluye:
- MenuPrincipal: pantalla inicial con opciones.
- PantallaAdministracion: gestión de datos/opciones de admin.
- PantallaMenuAdministrador: menú de opciones administrativas.
- PantallaCargaLaberinto: carga de archivos de laberinto.
- PantallaIniciarJuego: pantalla de inicio/selección para jugar.
- PantallaSalonFama: muestra puntajes o récords.
- MensajeModal: cuadro de diálogo para mensajes.
- ModalConfirmacion: cuadro de diálogo de confirmación.
"""

# Import relativo de las pantallas desde el paquete interfaz
from .interfaz import (
    MenuPrincipal,  # Menú de entrada a las demás pantallas
    MensajeModal,  # Cuadro de diálogo para mensajes
    ModalConfirmacion,  # Cuadro de diálogo de confirmación
    PantallaAdministracion,  # Opciones y administración del juego
    PantallaCargaLaberinto,  # Carga de archivos de laberinto
    PantallaIniciarJuego,  # Preparación y arranque del juego
    PantallaMenuAdministrador,  # Menú de opciones administrativas
    PantallaSalonFama,  # Tabla de puntuaciones destacadas
)
