import pygame

AZUL = (0, 0, 255)

class Laberinto:
    TAM_CELDA = 32

    laberinto = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,0,1,1,0,0,1,1,1,1,1,1,1,1,1,0,0,1],
        [1,0,1,0,0,1,0,0,0,0,0,0,1,0,0,0,1,1,0,1],
        [1,0,1,1,1,1,0,1,0,0,1,0,1,0,1,0,1,0,0,1],
        [1,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,0,0,0,1],
        [1,1,1,0,0,0,1,1,0,0,1,0,0,0,1,1,1,1,0,1],
        [1,0,1,0,1,0,1,1,1,0,1,0,1,1,1,0,0,0,0,1],
        [1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,1,1,0,1],
        [1,0,1,0,1,0,1,0,1,1,0,0,1,1,1,0,0,1,0,1],
        [1,0,1,0,1,0,1,0,0,1,1,0,1,0,1,1,0,1,0,1],
        [1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ]

    def obtener_rectangulos(self):
        rectangulos = []
        for fila in range(len(self.laberinto)):
            for col in range(len(self.laberinto[0])):
                if self.laberinto[fila][col] == 1:
                    x = col * self.TAM_CELDA
                    y = fila * self.TAM_CELDA
                    rect = pygame.Rect(x, y, self.TAM_CELDA, self.TAM_CELDA)
                    rectangulos.append(rect)
        return rectangulos

    def dibujar_laberinto(self, pantalla):
        for fila in range(len(self.laberinto)):
            for col in range(len(self.laberinto[0])):
                if self.laberinto[fila][col] == 1:
                    x = col * self.TAM_CELDA
                    y = fila * self.TAM_CELDA
                    pygame.draw.rect(pantalla, AZUL, (x, y, self.TAM_CELDA, self.TAM_CELDA))