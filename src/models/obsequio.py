class Obsequio:
    """
    Representa un item coleccionable en el laberinto.

    Los obsequios son elementos que el jugador puede recolectar para sumar puntos.
    Cada obsequio tiene:
    - Una posición fija en el grid del laberinto
    - Un valor en puntos (por defecto 10)
    - Un estado activo/inactivo

    Los obsequios se renderizan como círculos dorados con efecto pulsante
    y tienen un tiempo de vida limitado (10 segundos) antes de reposicionarse.
    """

    def __init__(self, posicion: tuple[int, int], valor: int = 10):
        """
        Crea un nuevo obsequio.

        Args:
            posicion: Tupla (columna, fila) indicando la celda del laberinto
            valor: Puntos que otorga al ser recolectado (default: 10)
        """
        self._posicion = posicion  # Celda (col, fila) donde está ubicado
        self._valor = valor  # Puntos que otorga
        self._activo = True  # Si está disponible para recolectar

    @property
    def valor(self):
        """Obtiene el valor en puntos del obsequio."""
        return self._valor

    @valor.setter
    def valor(self, nuevo_valor: int) -> None:
        """Establece un nuevo valor en puntos para el obsequio."""
        self._valor = nuevo_valor

    @property
    def activo(self) -> bool:
        """Indica si el obsequio está disponible para ser recolectado."""
        return self._activo

    @activo.setter
    def activo(self, estado: bool) -> None:
        """Activa o desactiva el obsequio."""
        self._activo = estado

    @property
    def posicion(self):
        """Obtiene la posición (columna, fila) del obsequio en el grid."""
        return self._posicion

    @posicion.setter
    def posicion(self, nueva_posicion):
        """Cambia la posición del obsequio a una nueva celda."""
        self._posicion = nueva_posicion

    def recolectar(self) -> int:
        """Retorna los puntos que aporta y desactiva el obsequio"""
        if self._activo:
            self._activo = False
            return self._valor
        return 0
