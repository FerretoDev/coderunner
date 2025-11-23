"""
Generador de efectos de partículas (polvo, chispas, sangre).
"""

import json
from pathlib import Path
from PIL import Image, ImageDraw
import random
import sys

sys.path.append(str(Path(__file__).parent.parent))
from palette import get_palette


def generate_particle_effects(scale=1, palette_name="default", output_dir="assets"):
    """Genera texturas de partículas."""
    palette = get_palette(palette_name)

    particle_size = 8
    effects = {
        "dust": {"color": palette["GRIS"], "count": 8},
        "sparks": {"color": palette["ORO"], "count": 6},
        "blood": {"color": palette["ROJO"], "count": 6},
        "glow": {"color": palette["AZUL_CLARO"], "count": 4},
    }

    total_particles = sum(e["count"] for e in effects.values())
    sheet_w = particle_size * total_particles
    sheet_h = particle_size

    img = Image.new("RGBA", (sheet_w, sheet_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    meta = {"particles": {}}
    x_offset = 0

    random.seed(123)

    for effect_name, effect_data in effects.items():
        frames = []

        for i in range(effect_data["count"]):
            # Dibujar partícula con tamaño y opacidad variables
            size = random.randint(1, 3)
            center_x = x_offset + particle_size // 2
            center_y = particle_size // 2

            color = effect_data["color"]

            if effect_name == "sparks":
                # Chispas como líneas
                angle = random.randint(0, 3)
                if angle == 0:
                    draw.line(
                        [center_x, center_y, center_x + size, center_y], fill=color
                    )
                elif angle == 1:
                    draw.line(
                        [center_x, center_y, center_x, center_y + size], fill=color
                    )
                elif angle == 2:
                    draw.line(
                        [center_x, center_y, center_x + size, center_y + size],
                        fill=color,
                    )
                else:
                    draw.line(
                        [center_x, center_y, center_x - size, center_y + size],
                        fill=color,
                    )
            else:
                # Puntos circulares
                draw.ellipse(
                    [
                        center_x - size,
                        center_y - size,
                        center_x + size,
                        center_y + size,
                    ],
                    fill=color,
                )

            frames.append(
                {"x": x_offset, "y": 0, "w": particle_size, "h": particle_size}
            )

            x_offset += particle_size

        meta["particles"][effect_name] = {
            "frames": frames,
            "color": effect_data["color"],
        }

    if scale > 1:
        img = img.resize((sheet_w * scale, sheet_h * scale), Image.NEAREST)

    output_path = Path(output_dir)
    (output_path / "particles").mkdir(parents=True, exist_ok=True)
    (output_path / "meta").mkdir(exist_ok=True)

    img.save(output_path / "particles" / "particles.png")

    with open(output_path / "meta" / "particles.json", "w") as f:
        json.dump(meta, f, indent=2)

    print(f"✓ Partículas generadas: {len(effects)} tipos")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, default=1)
    parser.add_argument("--palette", default="default")
    parser.add_argument("--out", default="assets")
    args = parser.parse_args()

    generate_particle_effects(args.scale, args.palette, args.out)
