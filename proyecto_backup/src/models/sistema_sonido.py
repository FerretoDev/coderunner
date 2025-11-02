class SistemaSonido:
    """Sistema básico de sonido para el juego"""

    def __init__(self):
        """Inicializa el sistema de sonido"""
        self.sonidos_activos = True

    def reproducir_movimiento(self):
        """Reproduce sonido de movimiento"""
        if self.sonidos_activos:
            print("🔊 Movimiento", end="\r")

    def reproducir_captura(self):
        """Reproduce sonido de captura"""
        if self.sonidos_activos:
            print("🔊 Captura")

    def desactivar_sonidos(self):
        """Desactiva todos los sonidos"""
        self.sonidos_activos = False
