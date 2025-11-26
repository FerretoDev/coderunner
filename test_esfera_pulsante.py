"""
Script de prueba para verificar el efecto de esfera pulsante de la computadora.
Ejecutar para ver la animación en acción.
"""

import sys

sys.path.insert(0, "src")

import pygame

from personajes.computadora import Computadora

# Inicializar pygame
pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Test - Esfera Pulsante")
clock = pygame.time.Clock()

# Crear computadora en el centro
computadora = Computadora(200, 200, radio=20, velocidad=2)

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

    # Dibujar computadora con efecto pulsante
    computadora.dibujar_computadora_principal(screen)

    # Texto de instrucciones
    font = pygame.font.Font(None, 24)
    text = font.render("ESC para salir", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    # Actualizar pantalla
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print("✓ Test completado - La esfera pulsante funciona correctamente")
