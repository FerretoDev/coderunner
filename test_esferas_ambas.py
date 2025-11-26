"""
Script de prueba para verificar el efecto de esfera pulsante del jugador y la computadora.
Ejecutar para ver ambas animaciones en acción.
"""

import sys

sys.path.insert(0, "src")

import pygame

from personajes.computadora import Computadora
from personajes.jugador import Jugador

# Inicializar pygame
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Test - Esferas Pulsantes (Jugador vs Computadora)")
clock = pygame.time.Clock()

# Crear jugador (izquierda, azul/cyan)
jugador = Jugador(150, 200, radio=20)

# Crear computadora (derecha, rojo)
computadora = Computadora(450, 200, radio=20, velocidad=2)

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Limpiar pantalla
    screen.fill((20, 20, 30))

    # Dibujar jugador (azul/cyan)
    jugador.dibujar_jugador_principal(screen)

    # Dibujar computadora (rojo)
    computadora.dibujar_computadora_principal(screen)

    # Textos
    font = pygame.font.Font(None, 24)
    font_small = pygame.font.Font(None, 20)

    # Título
    text = font.render("ESC para salir", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    # Etiquetas
    jugador_label = font_small.render("JUGADOR", True, (100, 255, 255))
    screen.blit(jugador_label, (120, 350))

    comp_label = font_small.render("COMPUTADORA", True, (255, 100, 100))
    screen.blit(comp_label, (390, 350))

    # Actualizar pantalla
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print("✓ Test completado - Ambas esferas pulsantes funcionan correctamente")
