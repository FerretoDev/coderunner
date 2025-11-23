"""
Generador de fuente bitmap pixel art.
Crea fuentes de 8px y 16px con caracteres ASCII básicos.
"""

import json
from pathlib import Path
from PIL import Image, ImageDraw
import sys

sys.path.append(str(Path(__file__).parent.parent))
from palette import get_palette


# Definición de caracteres en formato 5x7 (matriz de bits)
FONT_5X7 = {
    "A": ["  X  ", " X X ", "X   X", "XXXXX", "X   X", "X   X", "X   X"],
    "B": ["XXXX ", "X   X", "X   X", "XXXX ", "X   X", "X   X", "XXXX "],
    "C": [" XXX ", "X   X", "X    ", "X    ", "X    ", "X   X", " XXX "],
    "E": ["XXXXX", "X    ", "X    ", "XXXX ", "X    ", "X    ", "XXXXX"],
    "G": [" XXX ", "X   X", "X    ", "X  XX", "X   X", "X   X", " XXX "],
    "M": ["X   X", "XX XX", "X X X", "X   X", "X   X", "X   X", "X   X"],
    "O": [" XXX ", "X   X", "X   X", "X   X", "X   X", "X   X", " XXX "],
    "S": [" XXX ", "X   X", "X    ", " XXX ", "    X", "X   X", " XXX "],
    "T": ["XXXXX", "  X  ", "  X  ", "  X  ", "  X  ", "  X  ", "  X  "],
    "U": ["X   X", "X   X", "X   X", "X   X", "X   X", "X   X", " XXX "],
    "0": [" XXX ", "X   X", "X  XX", "X X X", "XX  X", "X   X", " XXX "],
    "1": ["  X  ", " XX  ", "  X  ", "  X  ", "  X  ", "  X  ", "XXXXX"],
    "2": [" XXX ", "X   X", "    X", "   X ", "  X  ", " X   ", "XXXXX"],
    "3": ["XXXXX", "    X", "   X ", "  XX ", "    X", "X   X", " XXX "],
    ":": ["     ", "  X  ", "  X  ", "     ", "  X  ", "  X  ", "     "],
    "!": ["  X  ", "  X  ", "  X  ", "  X  ", "  X  ", "     ", "  X  "],
    " ": ["     ", "     ", "     ", "     ", "     ", "     ", "     "],
}


def draw_char(draw, x, y, char, palette, size=8):
    """Dibuja un carácter usando la matriz de bits."""
    if char.upper() not in FONT_5X7:
        return

    pattern = FONT_5X7[char.upper()]
    pixel_size = size // 8

    for row_idx, row in enumerate(pattern):
        for col_idx, pixel in enumerate(row):
            if pixel == "X":
                px = x + col_idx * pixel_size
                py = y + row_idx * pixel_size
                draw.rectangle(
                    [px, py, px + pixel_size - 1, py + pixel_size - 1],
                    fill=palette["BLANCO"],
                )


def generate_pixel_font(scale=1, palette_name="default", output_dir="assets"):
    """Genera fuentes bitmap de 8px y 16px."""
    palette = get_palette(palette_name)

    chars = list(FONT_5X7.keys())
    char_count = len(chars)

    sizes = [8, 16]

    for size in sizes:
        chars_per_row = 16
        rows = (char_count + chars_per_row - 1) // chars_per_row

        sheet_w = size * chars_per_row
        sheet_h = size * rows

        img = Image.new("RGBA", (sheet_w, sheet_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        char_map = {}

        for idx, char in enumerate(chars):
            row = idx // chars_per_row
            col = idx % chars_per_row

            x = col * size
            y = row * size

            draw_char(draw, x, y, char, palette, size)

            char_map[char] = {"x": x, "y": y, "width": size, "height": size}

        if scale > 1:
            img = img.resize((sheet_w * scale, sheet_h * scale), Image.NEAREST)

        output_path = Path(output_dir)
        (output_path / "fonts").mkdir(parents=True, exist_ok=True)
        (output_path / "meta").mkdir(exist_ok=True)

        filename = f"font_{size}px.png"
        img.save(output_path / "fonts" / filename)

        meta = {"size": size, "characters": char_map, "spacing": 1}

        with open(output_path / "meta" / f"font_{size}px.json", "w") as f:
            json.dump(meta, f, indent=2)

        print(f"✓ Font {size}px generada: {char_count} caracteres")

    print(f"  - {output_path / 'fonts' / 'font_8px.png'}")
    print(f"  - {output_path / 'fonts' / 'font_16px.png'}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, default=1)
    parser.add_argument("--palette", default="default")
    parser.add_argument("--out", default="assets")
    args = parser.parse_args()

    generate_pixel_font(args.scale, args.palette, args.out)
