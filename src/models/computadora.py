from .jugador import Jugador
from .laberinto import Laberinto
from .personaje import Personaje


class Computadora(Personaje):
    """Computadora enemiga que persigue al jugador.

    Implementación simple que mueve la computadora en píxeles hacia la
    posición del jugador. Usa `laberinto.es_paso_valido` con coordenadas de
    celda (x // TAM_CELDA, y // TAM_CELDA) para validar movimientos.
    """

    def __init__(self, x: int, y: int, radio: int = 10, velocidad: float = 1.1):
        super().__init__(x, y, radio, velocidad)

    def perseguir(self, jugador: Jugador, laberinto: Laberinto) -> None:
        """Mueve la computadora hacia el `jugador`.

        La estrategia es muy básica:
        - Calcular la diferencia en X e Y.
        - Intentar mover en el eje con mayor diferencia.
        - Validar la celda destino con `laberinto.es_paso_valido`.
        - Si está bloqueado, intentar el otro eje.
        - Si ambos ejes bloqueados, no moverse.
        """
        # Soporte a objetos Jugador que expongan jugador_principal (pygame.Rect)
        try:
            objetivo_x = jugador.jugador_principal.x
            objetivo_y = jugador.jugador_principal.y
        except Exception:
            # También soportar objetos con atributos x,y directamente
            objetivo_x = getattr(jugador, "x", None)
            objetivo_y = getattr(jugador, "y", None)

        if objetivo_x is None or objetivo_y is None:
            return

        dx = objetivo_x - self.x
        dy = objetivo_y - self.y

        # Priorizar el eje con mayor distancia
        ejes = ("x", "y") if abs(dx) >= abs(dy) else ("y", "x")

        # velocidad en píxeles (entero >=1)
        paso = max(1, int(round(self.velocidad)))

        try:
            tam = laberinto.TAM_CELDA
        except Exception:
            tam = 32

        for eje in ejes:
            if eje == "x" and dx != 0:
                nuevo_x = self.x + (paso if dx > 0 else -paso)
                nuevo_y = self.y
            elif eje == "y" and dy != 0:
                nuevo_x = self.x
                nuevo_y = self.y + (paso if dy > 0 else -paso)
            else:
                continue

            celda = (nuevo_x // tam, nuevo_y // tam)
            if laberinto.es_paso_valido(celda):
                self.x = nuevo_x
                self.y = nuevo_y
                return

        # Si llegó aquí, no se pudo mover en ninguno de los ejes

    def mover(self, direccion: str) -> None:
        """Mueve a la computadora en una dirección simple.

        Direcciones: 'arriba','abajo','izquierda','derecha'.
        No valida colisiones (usar `perseguir` para movimiento validado).
        """
        paso = max(1, int(round(self.velocidad)))
        if direccion == "arriba":
            self.y -= paso
        elif direccion == "abajo":
            self.y += paso
        elif direccion == "izquierda":
            self.x -= paso
        elif direccion == "derecha":
            self.x += paso
        # direcciones desconocidas: no hacer nada
