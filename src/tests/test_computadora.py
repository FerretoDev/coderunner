from models.computadora import Computadora


class StubJugador:
    def __init__(self, x, y):
        # Simular atributo jugador_principal de pygame.Rect
        class R:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        self.jugador_principal = R(x, y)


class StubLaberinto:
    def __init__(self, pasillos):
        # pasillos es un set de celdas válidas (tuplas)
        self.pasillos = set(pasillos)
        self.TAM_CELDA = 32

    def es_paso_valido(self, celda):
        return celda in self.pasillos


def test_computadora_se_aproxima_al_jugador():
    lab = StubLaberinto(pasillos={(0, 0), (1, 0), (2, 0)})
    comp = Computadora(x=0, y=0, radio=5, velocidad=2)
    jugador = StubJugador(x=64, y=0)  # a 2 celdas a la derecha (32px cada una)

    comp.perseguir(jugador, lab)

    # Con velocidad 2 -> paso = 2 píxeles, como la celda (0,0) sigue siendo válida,
    # se espera que comp.x aumente en 2
    assert comp.x == 2


def test_computadora_no_pasa_por_muro():
    # laberinto con bloqueos en la dirección del jugador
    lab = StubLaberinto(pasillos={(0, 0)})
    comp = Computadora(x=0, y=0, radio=5, velocidad=40)  # velocidad grande -> intenta salir de celda
    jugador = StubJugador(x=100, y=0)

    comp.perseguir(jugador, lab)

    # No debe moverse a una celda inválida
    assert (comp.x // lab.TAM_CELDA, comp.y // lab.TAM_CELDA) == (0, 0)
