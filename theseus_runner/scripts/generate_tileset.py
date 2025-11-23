"""
Generador de tileset modular para el laberinto.
Crea tiles de 16x16 y 32x32 píxeles con variaciones.
"""

import json
from pathlib import Path
from PIL import Image, ImageDraw
import sys

sys.path.append(str(Path(__file__).parent.parent))
from palette import get_palette


def draw_tile_floor(draw, x, y, size, palette, variant=0):
    """Dibuja tile de piso con variaciones."""
    base = palette["PIEDRA"]
    dark = palette["PIEDRA_OSCURA"]

    draw.rectangle([x, y, x + size - 1, y + size - 1], fill=base)

    # Grietas/detalles
    if variant == 0:
        for i in range(0, size, 4):
            draw.point((x + i, y + size // 2), fill=dark)
    elif variant == 1:
        draw.line([x + 2, y + 2, x + size - 3, y + size - 3], fill=dark)
    elif variant == 2:
        draw.rectangle(
            [x + size // 4, y + size // 4, x + size // 2, y + size // 2], fill=dark
        )


def draw_tile_wall(draw, x, y, size, palette):
    """Dibuja tile de muro."""
    draw.rectangle([x, y, x + size - 1, y + size - 1], fill=palette["GRIS_OSCURO"])

    # Bloques de piedra
    for i in range(0, size, size // 4):
        for j in range(0, size, size // 4):
            if (i + j) % 8 == 0:
                draw.point((x + i, y + j), fill=palette["GRIS"])


def draw_tile_door(draw, x, y, size, palette, open_state=False):
    """Dibuja tile de puerta."""
    if open_state:
        draw.rectangle([x, y, x + size - 1, y + size - 1], fill=(0, 0, 0, 0))
    else:
        draw.rectangle(
            [x, y, x + size - 1, y + size - 1], fill=palette["PIEDRA_OSCURA"]
        )
        # Marco
        draw.rectangle([x + 2, y + 2, x + size - 3, y + size - 3], fill=palette["ORO"])


def draw_tile_trap(draw, x, y, size, palette, active=False):
    """Dibuja tile de trampa."""
    base = palette["PIEDRA"] if not active else palette["ROJO_OSCURO"]
    draw.rectangle([x, y, x + size - 1, y + size - 1], fill=base)

    # Patrón de peligro
    if active:
        for i in range(0, size, 4):
            draw.line([x + i, y, x + i, y + size - 1], fill=palette["ROJO"])


def draw_tile_torch(draw, x, y, size, palette, lit=True):
    """Dibuja tile de antorcha."""
    draw.rectangle([x, y, x + size - 1, y + size - 1], fill=(0, 0, 0, 0))

    # Soporte
    center_x = x + size // 2
    draw.rectangle(
        [center_x - 1, y + size // 2, center_x + 1, y + size - 4],
        fill=palette["GRIS_OSCURO"],
    )

    # Llama
    if lit:
        flame_y = y + size // 4
        draw.rectangle(
            [center_x - 2, flame_y, center_x + 2, flame_y + 4], fill=palette["ORO"]
        )
        draw.point((center_x, flame_y - 1), fill=palette["ROJO_CLARO"])


def generate_tileset(scale=1, palette_name="default", output_dir="assets"):
    """Genera tileset completo."""
    palette = get_palette(palette_name)

    tile_sizes = [16, 32]
    tiles_meta = {}

    for size in tile_sizes:
        # 8 tiles por fila
        tiles_per_row = 8
        tile_types = [
            ("floor", 3),  # 3 variantes
            ("wall", 1),
            ("door", 2),  # cerrada/abierta
            ("trap", 2),  # inactiva/activa
            ("torch", 2),  # apagada/encendida
        ]

        total_tiles = sum(count for _, count in tile_types)
        rows = (total_tiles + tiles_per_row - 1) // tiles_per_row

        sheet_w = size * tiles_per_row
        sheet_h = size * rows

        img = Image.new("RGBA", (sheet_w, sheet_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        tile_index = 0
        tiles_info = []

        for tile_type, count in tile_types:
            for variant in range(count):
                row = tile_index // tiles_per_row
                col = tile_index % tiles_per_row

                tx = col * size
                ty = row * size

                if tile_type == "floor":
                    draw_tile_floor(draw, tx, ty, size, palette, variant)
                elif tile_type == "wall":
                    draw_tile_wall(draw, tx, ty, size, palette)
                elif tile_type == "door":
                    draw_tile_door(draw, tx, ty, size, palette, variant == 1)
                elif tile_type == "trap":
                    draw_tile_trap(draw, tx, ty, size, palette, variant == 1)
                elif tile_type == "torch":
                    draw_tile_torch(draw, tx, ty, size, palette, variant == 1)

                tiles_info.append(
                    {
                        "id": f"{tile_type}_{variant}" if count > 1 else tile_type,
                        "x": tx,
                        "y": ty,
                        "w": size,
                        "h": size,
                    }
                )

                tile_index += 1

        if scale > 1:
            img = img.resize((sheet_w * scale, sheet_h * scale), Image.NEAREST)

        output_path = Path(output_dir)
        (output_path / "tiles").mkdir(parents=True, exist_ok=True)
        (output_path / "meta").mkdir(exist_ok=True)

        filename = f"tileset_{size}x{size}.png"
        img.save(output_path / "tiles" / filename)

        tiles_meta[f"{size}x{size}"] = {"tile_size": size, "tiles": tiles_info}

        print(f"✓ Tileset {size}x{size} generado: {total_tiles} tiles")

    with open(output_path / "meta" / "tilesets.json", "w") as f:
        json.dump(tiles_meta, f, indent=2)

    print(f"  - {output_path / 'meta' / 'tilesets.json'}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, default=1)
    parser.add_argument("--palette", default="default")
    parser.add_argument("--out", default="assets")
    args = parser.parse_args()

    generate_tileset(args.scale, args.palette, args.out)
