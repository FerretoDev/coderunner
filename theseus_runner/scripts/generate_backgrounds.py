"""
Generador de fondos parallax (3 capas).
"""

import json
from pathlib import Path
from PIL import Image, ImageDraw
import random
import sys

sys.path.append(str(Path(__file__).parent.parent))
from palette import get_palette


def generate_parallax_backgrounds(scale=1, palette_name="default", output_dir="assets"):
    """Genera 3 capas de parallax para fondos."""
    palette = get_palette(palette_name)

    width, height = 320, 180

    # Capa 1: Cielo/Fondo lejano
    layer1 = Image.new("RGBA", (width, height), palette["AZUL_OSCURO"])
    draw = ImageDraw.Draw(layer1)

    # Estrellas/puntos de luz
    random.seed(42)
    for _ in range(30):
        x = random.randint(0, width - 1)
        y = random.randint(0, height // 2)
        draw.point((x, y), fill=palette["BLANCO"])

    # Capa 2: Estalactitas
    layer2 = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer2)

    for i in range(0, width, 40):
        x = i + random.randint(-10, 10)
        length = random.randint(20, 50)
        draw.polygon(
            [(x, 0), (x - 4, 0), (x - 2, length), (x + 2, length)], fill=palette["GRIS"]
        )

    # Capa 3: Detalles de caverna
    layer3 = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer3)

    # Formaciones rocosas
    for i in range(0, width, 60):
        x = i + random.randint(-15, 15)
        y = height - random.randint(30, 60)
        w = random.randint(20, 40)
        h = random.randint(20, 50)
        draw.ellipse([x, y, x + w, y + h], fill=palette["PIEDRA_OSCURA"])

    # Escalar si es necesario
    if scale > 1:
        layer1 = layer1.resize((width * scale, height * scale), Image.NEAREST)
        layer2 = layer2.resize((width * scale, height * scale), Image.NEAREST)
        layer3 = layer3.resize((width * scale, height * scale), Image.NEAREST)

    # Guardar
    output_path = Path(output_dir)
    (output_path / "backgrounds").mkdir(parents=True, exist_ok=True)
    (output_path / "meta").mkdir(exist_ok=True)

    layer1.save(output_path / "backgrounds" / "bg_layer1.png")
    layer2.save(output_path / "backgrounds" / "bg_layer2.png")
    layer3.save(output_path / "backgrounds" / "bg_layer3.png")

    meta = {
        "layers": [
            {"file": "bg_layer1.png", "speed": 0.2},
            {"file": "bg_layer2.png", "speed": 0.5},
            {"file": "bg_layer3.png", "speed": 0.8},
        ]
    }

    with open(output_path / "meta" / "backgrounds.json", "w") as f:
        json.dump(meta, f, indent=2)

    print("✓ Fondos parallax generados (3 capas)")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, default=1)
    parser.add_argument("--palette", default="default")
    parser.add_argument("--out", default="assets")
    args = parser.parse_args()

    generate_parallax_backgrounds(args.scale, args.palette, args.out)
