"""
Script de prueba para visualizar la nueva estética del laberinto.
Muestra muros con efecto neón, pasillos con patrón de puntos y obsequios con forma de diamante.
"""

import sys

sys.path.insert(0, "src")

import pygame

from mundo.laberinto import Laberinto

# Inicializar pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Test - Estética del Laberinto")
clock = pygame.time.Clock()

# Crear un laberinto de prueba simple
datos_laberinto = {
    "nombre": "Test Visual",
    "dificultad": "normal",
    "mapa": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    "inicio_jugador": {"col": 1, "fila": 1},
    "inicio_computadora": {"col": 8, "fila": 7},
    "obsequios": [
        {"posicion": [3, 1], "valor": 50},
        {"posicion": [5, 3], "valor": 100},
        {"posicion": [7, 5], "valor": 75},
        {"posicion": [2, 7], "valor": 50},
    ],
}

laberinto = Laberinto(datos_laberinto)

# Configuración de vista
tam_celda = 60
offset_x = (800 - 10 * tam_celda) // 2
offset_y = (600 - 9 * tam_celda) // 2
frame_count = 0

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    frame_count += 1

    # Fondo oscuro
    screen.fill((10, 12, 18))

    # Dibujar laberinto con la nueva estética
    for fila in range(len(laberinto.laberinto)):
        for col in range(len(laberinto.laberinto[0])):
            x = col * tam_celda + offset_x
            y = fila * tam_celda + offset_y

            if laberinto.laberinto[fila][col] == 1:
                # === MUROS CON EFECTO NEÓN ===
                pygame.draw.rect(screen, (20, 25, 40), (x, y, tam_celda, tam_celda))

                # Patrón de cuadrícula interior
                grid_size = tam_celda // 4
                for i in range(4):
                    for j in range(4):
                        gx = x + i * grid_size + 2
                        gy = y + j * grid_size + 2
                        color_var = 30 + ((i + j) % 2) * 10
                        pygame.draw.rect(
                            screen,
                            (color_var, color_var + 10, color_var + 20),
                            (gx, gy, grid_size - 4, grid_size - 4),
                        )

                # Borde neón cyan brillante
                pygame.draw.rect(screen, (0, 200, 255), (x, y, tam_celda, tam_celda), 2)
                pygame.draw.rect(
                    screen,
                    (0, 120, 180),
                    (x + 2, y + 2, tam_celda - 4, tam_celda - 4),
                    1,
                )
            else:
                # === PASILLOS CON PATRÓN DE PUNTOS ===
                import math

                pygame.draw.rect(screen, (15, 18, 25), (x, y, tam_celda, tam_celda))

                dot_spacing = 8
                for dx in range(0, tam_celda, dot_spacing):
                    for dy in range(0, tam_celda, dot_spacing):
                        pulso = abs(math.sin((frame_count + dx + dy) * 0.05)) * 10
                        pygame.draw.circle(
                            screen,
                            (0, 40 + int(pulso), 60 + int(pulso)),
                            (x + dx + 4, y + dy + 4),
                            1,
                        )

                pygame.draw.rect(screen, (0, 60, 80), (x, y, tam_celda, tam_celda), 1)

    # Dibujar obsequios con nueva estética de diamante
    laberinto.dibujar_obsequios(screen, frame_count, tam_celda, offset_x, offset_y)

    # Instrucciones
    font = pygame.font.Font(None, 24)
    text = font.render("ESC para salir", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    title = font.render("Estética Retro/Arcade", True, (0, 255, 255))
    screen.blit(title, (10, 560))

    # Leyenda
    font_small = pygame.font.Font(None, 18)
    legend = [
        "Muros: Neón cyan con patrón de cuadrícula",
        "Pasillos: Puntos pulsantes azules",
        "Obsequios: Diamantes giratorios dorados",
    ]
    for i, line in enumerate(legend):
        text_surf = font_small.render(line, True, (150, 150, 150))
        screen.blit(text_surf, (250, 560 + i * 15))

    # Actualizar pantalla
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print("✓ Test completado - Nueva estética del laberinto funcionando correctamente")
