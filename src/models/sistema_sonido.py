class SistemaSonido:
    """Sistema básico de sonido para el juego"""

    def __init__(self):
        # Este método se llama al crear el sistema de sonido.
        # Por defecto, los sonidos están activados.
        self.sonidos_activos = True

    def reproducir_movimiento(self):
        # Si los sonidos están activados, muestra un mensaje de movimiento.
        if self.sonidos_activos:
            print("Movimiento", end="\r")

    def reproducir_captura(self):
        # Si los sonidos están activados, muestra un mensaje de captura.
        if self.sonidos_activos:
            print("Captura")

    def desactivar_sonidos(self):
        # Desactiva todos los sonidos del sistema.
        self.sonidos_activos = False
