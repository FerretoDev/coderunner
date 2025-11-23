#!/usr/bin/env python3
"""
Script de prueba rápida del sistema UI pixel art.

Ejecuta directamente la pantalla de demostración sin pasar por el menú principal.
"""

import os
import sys

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import pygame
from interfaz.pantallas.pantalla_demo_ui import PantallaDemoUI


def main():
    """Ejecuta la demo UI directamente."""
    # Inicializar Pygame
    pygame.init()

    # Crear ventana
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("CodeRunner - Demo UI Pixel Art")

    # Crear pantalla de demo
    pantalla_demo = PantallaDemoUI(screen)

    print("=== DEMO UI PIXEL ART ===")
    print("Controles:")
    print("  ↑↓ : Cambiar vida")
    print("  ←→ : Cambiar llaves")
    print("  Click: Interactuar con botones")
    print("  ESC: Salir")
    print()

    # Ejecutar usando el loop de PantallaBase
    resultado = pantalla_demo.ejecutar()

    # Cerrar
    pygame.quit()
    print(f"Demo finalizada: {resultado}")


if __name__ == "__main__":
    main()
