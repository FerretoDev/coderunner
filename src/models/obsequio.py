class Obsequio:
    def __init__(self, posicion: tuple[int, int], valor: int = 10):
        self._posicion = posicion
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, nuevo_valor: int) -> None:
        self._valor = nuevo_valor

    @property
    def activo(self) -> bool:
        return self._activo

    @activo.setter
    def activo(self, estado: bool) -> None:
        self._activo = estado

    @property
    def posicion(self):
        return self._posicion

    @posicion.setter
    def posicion(self, nueva_posicion):
        self._posicion = nueva_posicion

    def recolectar(self) -> int:
        """Retorna los puntos que aporta y desactiva el obsequio"""

        return 0
