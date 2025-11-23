#!/usr/bin/env python3
"""
Script para verificar que Press Start 2P está siendo usada en todo el juego.
"""

import sys
import pygame

# Inicializar pygame
pygame.init()

# Importar el gestor de fuentes
sys.path.insert(0, "src")
from interfaz.gestor_fuentes import GestorFuentes


def verificar_fuentes():
    """Verifica que todas las fuentes usen Press Start 2P."""
    print("=" * 60)
    print("  VERIFICACIÓN DE FUENTES - CODERUNNER")
    print("=" * 60)

    fuentes = GestorFuentes()

    print(f"\n✓ Fuente activa: {fuentes.fuente_pixel_nombre}")

    if "Press Start 2P" in fuentes.fuente_pixel_nombre:
        print("✓ Press Start 2P cargada correctamente desde TTF")
        print("\nFuentes disponibles:")
        print(f"  - Títulos: {fuentes.titulo_grande.get_height()}px (grande)")
        print(f"  - Títulos: {fuentes.titulo_normal.get_height()}px (normal)")
        print(f"  - Títulos: {fuentes.titulo_mediano.get_height()}px (mediano)")
        print(f"  - Títulos: {fuentes.titulo_pequeño.get_height()}px (pequeño)")
        print(f"  - Títulos: {fuentes.titulo_mini.get_height()}px (mini)")
        print(f"  - Texto: {fuentes.texto_grande.get_height()}px (grande)")
        print(f"  - Texto: {fuentes.texto_normal.get_height()}px (normal)")
        print(f"  - Texto: {fuentes.texto_pequeño.get_height()}px (pequeño)")
        print(f"  - HUD: {fuentes.hud_titulo.get_height()}px (título)")
        print(f"  - HUD: {fuentes.hud_normal.get_height()}px (normal)")
        print(f"  - HUD: {fuentes.hud_pequeño.get_height()}px (pequeño)")

        # Renderizar un ejemplo
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Verificación de Fuente")

        screen.fill((20, 20, 30))

        # Título grande
        titulo = fuentes.titulo_grande.render("CODERUNNER", True, (0, 255, 128))
        titulo_rect = titulo.get_rect(center=(400, 100))
        screen.blit(titulo, titulo_rect)

        # Subtítulo
        subtitulo = fuentes.titulo_pequeño.render(
            "Press Start 2P Font", True, (200, 200, 200)
        )
        subtitulo_rect = subtitulo.get_rect(center=(400, 180))
        screen.blit(subtitulo, subtitulo_rect)

        # Texto normal
        texto1 = fuentes.texto_grande.render(
            "Laberinto del Minotauro", True, (255, 255, 255)
        )
        texto1_rect = texto1.get_rect(center=(400, 280))
        screen.blit(texto1, texto1_rect)

        # Texto pequeño
        texto2 = fuentes.texto_normal.render(
            "Fuente pixel art retro", True, (150, 150, 255)
        )
        texto2_rect = texto2.get_rect(center=(400, 350))
        screen.blit(texto2, texto2_rect)

        # HUD
        hud = fuentes.hud_normal.render("VIDAS: 3  PUNTOS: 100", True, (255, 200, 0))
        hud_rect = hud.get_rect(center=(400, 450))
        screen.blit(hud, hud_rect)

        # Info
        info = fuentes.texto_info.render(
            "Presiona cualquier tecla para salir", True, (100, 100, 120)
        )
        info_rect = info.get_rect(center=(400, 550))
        screen.blit(info, info_rect)

        pygame.display.flip()

        print("\n✓ Ventana de ejemplo generada")
        print("  Presiona cualquier tecla para cerrar...")

        # Esperar a que se cierre
        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    esperando = False
                elif evento.type == pygame.KEYDOWN:
                    esperando = False

        pygame.quit()

        print("\n" + "=" * 60)
        print("  ✓ VERIFICACIÓN COMPLETA - TODO CORRECTO")
        print("=" * 60)

    else:
        print("⚠ Usando fuente de respaldo:", fuentes.fuente_pixel_nombre)
        print("  La fuente Press Start 2P no está disponible.")
        print("  Ejecuta: python descargar_fuente.py")


if __name__ == "__main__":
    verificar_fuentes()
