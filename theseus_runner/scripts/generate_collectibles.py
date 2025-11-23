"""
Generador de coleccionables (llaves, gemas, monedas, vida).
"""

import json
from pathlib import Path
from PIL import Image, ImageDraw
import sys

sys.path.append(str(Path(__file__).parent.parent))
from palette import get_palette


def draw_collectible_key(draw, x, y, size, palette, frame=0):
    """Dibuja llave con animación de brillo."""
    glow = frame % 2 == 0
    color = palette["ORO"] if not glow else palette["BLANCO"]

    # Cabeza
    draw.ellipse([x + 2, y + 2, x + size // 2, y + size // 2], fill=color)

    # Vástago
    draw.rectangle(
        [x + size // 4, y + size // 2, x + size // 2, y + size - 4], fill=color
    )

    # Dientes
    draw.point((x + size // 4, y + size - 4), fill=color)
    draw.point((x + size // 2, y + size - 6), fill=color)


def draw_collectible_gem(draw, x, y, size, palette, frame=0):
    """Dibuja gema con rotación."""
    center_x = x + size // 2
    center_y = y + size // 2

    colors = [palette["AZUL_CLARO"], palette["BLANCO"], palette["AZUL"]]
    color = colors[frame % 3]

    points = [
        (center_x, y + 2),
        (x + size - 2, center_y),
        (center_x, y + size - 2),
        (x + 2, center_y),
    ]

    draw.polygon(points, fill=color)
    draw.polygon(points, outline=palette["BLANCO"])


def draw_collectible_coin(draw, x, y, size, palette, frame=0):
    """Dibuja moneda con animación de giro."""
    width = size if frame % 4 < 2 else size // 2
    offset = (size - width) // 2

    draw.ellipse(
        [x + offset, y + 2, x + offset + width, y + size - 2], fill=palette["ORO"]
    )
    if width > size // 2:
        draw.ellipse(
            [x + offset + 2, y + 4, x + offset + width - 2, y + size - 4],
            outline=palette["BLANCO"],
        )


def draw_collectible_heart(draw, x, y, size, palette, frame=0):
    """Dibuja corazón (vida) con latido."""
    scale_factor = 1.1 if frame % 2 == 0 else 1.0
    center = size // 2

    # Corazón simple
    color = palette["ROJO_CLARO"]
    draw.ellipse([x + 2, y + 3, x + center, y + center + 2], fill=color)
    draw.ellipse([x + center, y + 3, x + size - 2, y + center + 2], fill=color)
    draw.polygon(
        [
            (x + center, y + center),
            (x + 2, y + center),
            (x + center, y + size - 2),
            (x + size - 2, y + center),
        ],
        fill=color,
    )


def generate_collectibles_spritesheet(
    scale=1, palette_name="default", output_dir="assets"
):
    """Genera spritesheet de coleccionables."""
    palette = get_palette(palette_name)

    size = 16
    items = ["key", "gem", "coin", "heart"]
    frames_per_item = 4

    sheet_w = size * frames_per_item * len(items)
    sheet_h = size

    img = Image.new("RGBA", (sheet_w, sheet_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    meta = {"collectibles": {}}

    x_offset = 0

    for item in items:
        frames_data = []

        for frame in range(frames_per_item):
            if item == "key":
                draw_collectible_key(draw, x_offset, 0, size, palette, frame)
            elif item == "gem":
                draw_collectible_gem(draw, x_offset, 0, size, palette, frame)
            elif item == "coin":
                draw_collectible_coin(draw, x_offset, 0, size, palette, frame)
            elif item == "heart":
                draw_collectible_heart(draw, x_offset, 0, size, palette, frame)

            frames_data.append(
                {"x": x_offset, "y": 0, "w": size, "h": size, "duration": 150}
            )

            x_offset += size

        meta["collectibles"][item] = {"frames": frames_data, "loop": True}

    if scale > 1:
        img = img.resize((sheet_w * scale, sheet_h * scale), Image.NEAREST)

    output_path = Path(output_dir)
    (output_path / "sprites").mkdir(parents=True, exist_ok=True)
    (output_path / "meta").mkdir(exist_ok=True)

    img.save(output_path / "sprites" / "collectibles_spritesheet.png")

    with open(output_path / "meta" / "collectibles.json", "w") as f:
        json.dump(meta, f, indent=2)

    print(f"✓ Collectibles generados: {len(items)} tipos")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, default=1)
    parser.add_argument("--palette", default="default")
    parser.add_argument("--out", default="assets")
    args = parser.parse_args()

    generate_collectibles_spritesheet(args.scale, args.palette, args.out)
