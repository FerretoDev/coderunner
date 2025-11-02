import os
import sys

import pygame

# Agregar el directorio src al path para las importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.interfaz import (
    MensajeModal,
    MenuPrincipal,
    PantallaAdministracion,
    PantallaIniciarJuego,
    PantallaSalonFama,
)
from models.administrador import Administrador
from models.salon_fama import SalonFama
from models.sistema_sonido import SistemaSonido


class Juego:
    """
    Clase que maneja la lógica principal del juego.
    """

    def __init__(self):
        self._jugador = None
        self._computadora = None
        self._laberinto = None
        self.sonido = SistemaSonido()
        self.salon_fama = SalonFama()
        self._estado = "en curso"

        # Pygame
        self.screen = None
        self.clock = pygame.time.Clock()

    def iniciar(self):
        # Inicializar Pygame
        pygame.init()

        # Crear ventana
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("CodeRunner")

        # Instancias
        salon_fama = SalonFama()
        admin = Administrador("casa")

        # Loop principal
        ejecutando = True

        while ejecutando:
            # Mostrar menú principal
            menu = MenuPrincipal(screen)
            opcion = menu.ejecutar()

            if opcion == 1:  # Iniciar Juego
                pantalla_inicio = PantallaIniciarJuego(screen)
                nombre = pantalla_inicio.ejecutar()

                if nombre:
                    # TODO: Iniciar el juego
                    # modal = MensajeModal(
                    #    screen,
                    #    "Próximamente",
                    #    "El juego se implementará pronto",
                    #    "info",
                    # )
                    # modal.ejecutar()
                    from .laberinto_uno import Juego

                    juego = Juego()
                    juego.bucle_principal()

            elif opcion == 2:  # Salón de la Fama
                pantalla_salon = PantallaSalonFama(screen, salon_fama)
                pantalla_salon.ejecutar()

            elif opcion == 3:  # Administración
                pantalla_admin = PantallaAdministracion(screen)
                clave = pantalla_admin.ejecutar()

                if clave and admin.autenticar(clave):
                    modal = MensajeModal(
                        screen,
                        "✅ Acceso Concedido",
                        "Bienvenido Administrador",
                        "success",
                    )
                    modal.ejecutar()
                    # TODO: Panel de admin
                elif clave:
                    modal = MensajeModal(
                        screen, "❌ Error", "Clave incorrecta", "error"
                    )
                    modal.ejecutar()

            elif opcion == 4:  # Salir
                ejecutando = False

        pygame.quit()
        sys.exit()

        self.terminar()

    def actualizar(self):
        """Cada ciclo: mover enemigo, detectar colisiones, actualizar puntaje"""
        pass

    def mostrar_estado(self):
        """Muestra cuántos puntos y vidas tiene el jugador"""
        if self._jugador:
            print(f"Jugador: {self._jugador['nombre']}")
            print(f"Puntaje: {self._jugador['puntaje']}")
            print(f"Vidas: {self._jugador['vidas']}")

    def terminar(self):
        """Cierra el juego y guarda en el Salón de la Fama"""
        print("🎮 Juego terminado")
        if self._jugador:
            print(f"Puntaje final: {self._jugador['puntaje']}")
        pygame.quit()

    def salir(self):
        """Maneja la confirmación y cierre ordenado de la aplicación"""
        self.terminar()
