import pygame

class Jugador:
    def __init__(self, x, y, radio):
        self.radio = radio
        self.color = (255, 0, 0)
        self.velocidad = 4
        self.jugador_principal = pygame.Rect(x, y, radio*2, radio*2)

    def mover(self,teclas):
        if teclas[pygame.K_LEFT]:
            self.jugador_principal.x -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            self.jugador_principal.x += self.velocidad
        if teclas[pygame.K_UP]:
            self.jugador_principal.y -= self.velocidad
        if teclas[pygame.K_DOWN]:
            self.jugador_principal.y += self.velocidad
    
    def dibujar_jugador_principal(self, pantalla):
        centro = self.jugador_principal.center
        pygame.draw.circle(pantalla, self.color, centro, self.radio)
