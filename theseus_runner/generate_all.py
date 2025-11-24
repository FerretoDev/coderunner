"""
Script principal para generar todos los assets de Theseus Runner.
Ejecuta todos los sub-scripts en orden y crea la carpeta assets/ completa.
"""

import argparse
import sys
from pathlib import Path

# Importar generadores
sys.path.insert(0, str(Path(__file__).parent))
from scripts.generate_theseus import generate_theseus_spritesheet
from scripts.generate_minotaur import generate_minotaur_spritesheet
from scripts.generate_tileset import generate_tileset
from scripts.generate_ui import generate_ui_assets
from scripts.generate_fonts import generate_pixel_font
from scripts.generate_backgrounds import generate_parallax_backgrounds
from scripts.generate_collectibles import generate_collectibles_spritesheet
from scripts.generate_enemies import generate_enemies_spritesheet
from scripts.generate_particles import generate_particle_effects
from scripts.generate_audio import generate_audio_assets


def main():
    parser = argparse.ArgumentParser(
        description="Genera todos los assets de Theseus Runner"
    )
    parser.add_argument(
        "--scale",
        type=int,
        default=2,
        choices=[1, 2, 3, 4],
        help="Escala de los sprites (default: 2)",
    )
    parser.add_argument(
        "--palette",
        default="default",
        choices=["default", "night", "lava"],
        help="Paleta de colores (default: default)",
    )
    parser.add_argument(
        "--out", default="assets", help="Directorio de salida (default: assets/)"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("THESEUS RUNNER - Generador de Assets Pixel Art")
    print("=" * 60)
    print(f"\nConfiguración:")
    print(f"  Escala: {args.scale}x")
    print(f"  Paleta: {args.palette}")
    print(f"  Salida: {args.out}/")
    print("\n" + "=" * 60)

    # Crear directorio de salida
    output_path = Path(args.out)
    output_path.mkdir(parents=True, exist_ok=True)

    try:
        # 1. Personajes
        print("\n[1/10] Generando Theseus...")
        generate_theseus_spritesheet(args.scale, args.palette, args.out)

        print("\n[2/10] Generando Minotauro...")
        generate_minotaur_spritesheet(args.scale, args.palette, args.out)

        print("\n[3/10] Generando enemigos...")
        generate_enemies_spritesheet(args.scale, args.palette, args.out)

        # 2. Mundo
        print("\n[4/10] Generando tilesets...")
        generate_tileset(args.scale, args.palette, args.out)

        print("\n[5/10] Generando fondos parallax...")
        generate_parallax_backgrounds(args.scale, args.palette, args.out)

        # 3. Objetos
        print("\n[6/10] Generando coleccionables...")
        generate_collectibles_spritesheet(args.scale, args.palette, args.out)

        print("\n[7/10] Generando partículas...")
        generate_particle_effects(args.scale, args.palette, args.out)

        # 4. UI
        print("\n[8/10] Generando interfaz de usuario...")
        generate_ui_assets(args.scale, args.palette, args.out)

        print("\n[9/10] Generando fuente pixel...")
        generate_pixel_font(args.scale, args.palette, args.out)

        # 5. Audio
        print("\n[10/10] Generando assets de audio...")
        generate_audio_assets(args.out)

        print("\n" + "=" * 60)
        print("✓ ¡Todos los assets generados exitosamente!")
        print("=" * 60)
        print(f"\nRevisa la carpeta: {output_path.absolute()}/")
        print("\nContenido generado:")
        print("  - sprites/      (personajes y animaciones)")
        print("  - tiles/        (tileset del laberinto)")
        print("  - ui/           (interfaz y HUD)")
        print("  - fonts/        (fuente pixel)")
        print("  - bg/           (fondos parallax)")
        print("  - audio/        (música y SFX)")
        print("  - meta/         (archivos JSON con metadata)")
        print("\nPara probar: python demo.py")

    except Exception as e:
        print(f"\n✗ Error durante la generación: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
