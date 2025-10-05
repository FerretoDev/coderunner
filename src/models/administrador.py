from src.models.laberinto import Laberinto
from src.models.salon_fama import SalonFama


class Administrador:
    """
    Clase que representa al administrador del juego.
    """

    def __init__(self, clave: str):
        self._clave = clave

        def autenticar(self, clave: str) -> bool:
            """Autentica al administrador con la clave proporcionada."""
            return self._clave == clave

    def cargar_laberinto(self, ruta_archivo: str) -> Laberinto:
        """Carga un laberinto desde un archivo."""
        return Laberinto()

    def reiniciar_salon_fama(self, salon: SalonFama) -> None:
        """Reinicia el salón de la fama."""
        ...
