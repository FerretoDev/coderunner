from game.juego import Juego


def main():
    juego = Juego()
    juego.iniciar()


if __name__ == "__main__":
    main()


datos: list[int] = [1, 2, 3]


def agregar(lista: list):
    lista.append(99)


agregar(datos)


aj: int = "e"
b: bool = "True"


def hola():
    print("hola")
