#!/usr/bin/env python3
"""
Script para descargar e instalar la fuente Press Start 2P para CodeRunner.

Esta fuente pixel art de Google Fonts es perfecta para juegos retro.
"""

import os
import urllib.request
from pathlib import Path


def descargar_fuente_press_start_2p():
    """Descarga la fuente Press Start 2P de Google Fonts."""

    # URL directa del archivo TTF de Google Fonts
    url = "https://github.com/google/fonts/raw/main/ofl/pressstart2p/PressStart2P-Regular.ttf"

    # Crear directorio de fuentes si no existe
    fonts_dir = Path("src/assets/fonts")
    fonts_dir.mkdir(parents=True, exist_ok=True)

    # Ruta de destino
    font_path = fonts_dir / "PressStart2P-Regular.ttf"

    if font_path.exists():
        print(f"✓ Fuente ya existe en: {font_path}")
        return str(font_path)

    print("Descargando fuente Press Start 2P...")
    try:
        urllib.request.urlretrieve(url, font_path)
        print(f"✓ Fuente descargada exitosamente en: {font_path}")
        print(f"  Tamaño: {font_path.stat().st_size / 1024:.1f} KB")
        return str(font_path)
    except Exception as e:
        print(f"✗ Error al descargar la fuente: {e}")
        print("\nAlternativa manual:")
        print(f"1. Descarga desde: {url}")
        print(f"2. Guárdala en: {font_path}")
        return None


def verificar_fuente():
    """Verifica que la fuente se pueda cargar con pygame."""
    try:
        import pygame

        pygame.init()

        font_path = Path("src/assets/fonts/PressStart2P-Regular.ttf")
        if font_path.exists():
            font = pygame.font.Font(str(font_path), 16)
            print(f"\n✓ Fuente verificada con pygame")
            return True
        else:
            print(f"\n✗ Archivo de fuente no encontrado")
            return False
    except Exception as e:
        print(f"\n✗ Error al verificar la fuente: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("  INSTALADOR DE FUENTE PIXEL ART - CODERUNNER")
    print("=" * 60)
    print()

    font_path = descargar_fuente_press_start_2p()

    if font_path:
        print()
        if verificar_fuente():
            print()
            print("=" * 60)
            print("  ✓ INSTALACIÓN COMPLETA")
            print("=" * 60)
            print()
            print("La fuente Press Start 2P está lista para usar.")
            print("El juego la usará automáticamente.")
        else:
            print("\nAdvertencia: La fuente se descargó pero no se pudo verificar.")
    else:
        print("\nNo se pudo completar la instalación automática.")
