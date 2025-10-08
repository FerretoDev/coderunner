import os
import sys

import pygame

# Agregar el directorio src al path para las importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.salon_fama import SalonFama
from models.sistema_sonido import SistemaSonido


class Juego:
    """
    Clase que maneja la lógica principal del juego.
    """

    def __init__(self):
        self._jugador = None
        self._enemigo = None
        self._laberinto = None
        self._sonido = SistemaSonido()
        self._salon_fama = SalonFama()
        self._estado = "en curso"

        # Pygame
        self.screen = None
        self.clock = pygame.time.Clock()

    def iniciar(self, nombre: str):
        """Arranca el juego con un jugador, crea los objetos iniciales"""
        print(f"🎮 Iniciando juego para: {nombre}")

        # Inicializar pygame
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("CodeRunner")

        # Crear jugador básico
        self._jugador = {"nombre": nombre, "puntaje": 0, "vidas": 3}

        # Loop principal del juego
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # Limpiar pantalla
            self.screen.fill((0, 0, 0))

            # Mostrar información básica
            font = pygame.font.Font(None, 36)
            texto = font.render(f"Jugador: {nombre}", True, (255, 255, 255))
            self.screen.blit(texto, (10, 10))

            texto2 = font.render("Presiona ESC para salir", True, (255, 255, 255))
            self.screen.blit(texto2, (10, 50))

            pygame.display.flip()
            self.clock.tick(60)

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
