import pygame
import sys
from laberinto import *
from jugador import *

ANCHO = 640
ALTO = 480
NEGRO = (0,0,0)

class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO,ALTO))
        self.bucle = True
        self.reloj = pygame.time.Clock()
        self.jugador_principal = Jugador(32, 32, 16)
        self.laberinto = Laberinto()
        self.muros = self.laberinto.obtener_rectangulos()

    def bucle_principal(self):
        while self.bucle:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.bucle = False
                    sys.exit()

            self.pantalla.fill(NEGRO)
            teclas = pygame.key.get_pressed()

            # Guardar posición anterior
            pos_x = self.jugador_principal.jugador_principal.x
            pos_y = self.jugador_principal.jugador_principal.y

            # Mover jugador
            self.jugador_principal.mover(teclas)

            # Colisiones con muros
            for muro in self.muros:
                if self.jugador_principal.jugador_principal.colliderect(muro):
                    self.jugador_principal.jugador_principal.x = pos_x
                    self.jugador_principal.jugador_principal.y = pos_y
                    break

            # Dibujar
            self.laberinto.dibujar_laberinto(self.pantalla)
            self.jugador_principal.dibujar_jugador_principal(self.pantalla)

            self.reloj.tick(60)
            pygame.display.flip()

juego = Juego()
juego.bucle_principal()