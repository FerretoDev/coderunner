# from game.pruebas_pacman.juego import Juego
from game.juego import Juego
from game.pantalla_juego import PantallaJuego

# from Prototipo3.juego import Juego


def main():
    juego = Juego()
    juego.iniciar()

    # ------
    # from game.pantalla_juego import PantallaJuego

    # ----
    # Test (please no tocar)

    """
    try:
        ## Iniciar Pygame
        pygame.init()

        # crear y correr juego
        game = Juego()
        game.run()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        pygame.quit()
        sys.exit()"""


if __name__ == "__main__":
    main()
