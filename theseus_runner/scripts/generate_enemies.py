"""
Generador de enemigos secundarios (ratas, estatuas).
"""

import json
from pathlib import Path
from PIL import Image, ImageDraw
import sys

sys.path.append(str(Path(__file__).parent.parent))
from palette import get_palette


def draw_rat_run(draw, x, y, frame, palette):
    """Dibuja rata corriendo (16x16)."""
    # Cuerpo
    draw.rectangle([x + 4, y + 8, x + 12, y + 14], fill=palette["GRIS_OSCURO"])

    # Cabeza
    draw.rectangle([x + 2, y + 8, x + 6, y + 12], fill=palette["GRIS_OSCURO"])

    # Ojo
    draw.point((x + 3, y + 9), fill=palette["ROJO"])

    # Cola
    tail_y = y + 10 + (1 if frame % 2 == 0 else -1)
    draw.line([x + 12, y + 12, x + 14, tail_y], fill=palette["GRIS"])

    # Patas (alternadas)
    if frame % 2 == 0:
        draw.point((x + 6, y + 14), fill=palette["GRIS"])
        draw.point((x + 10, y + 14), fill=palette["GRIS"])
    else:
        draw.point((x + 7, y + 14), fill=palette["GRIS"])
        draw.point((x + 11, y + 14), fill=palette["GRIS"])


def draw_statue_idle(draw, x, y, frame, palette):
    """Dibuja estatua de guerrero (32x32)."""
    # Base/pedestal
    draw.rectangle([x + 8, y + 26, x + 24, y + 30], fill=palette["PIEDRA_OSCURA"])

    # Cuerpo
    draw.rectangle([x + 12, y + 12, x + 20, y + 26], fill=palette["PIEDRA"])

    # Cabeza
    draw.rectangle([x + 13, y + 6, x + 19, y + 12], fill=palette["PIEDRA"])

    # Brazos
    draw.rectangle([x + 8, y + 14, x + 12, y + 22], fill=palette["PIEDRA"])
    draw.rectangle([x + 20, y + 14, x + 24, y + 22], fill=palette["PIEDRA"])

    # Ojos brillantes (parpadeo)
    if frame % 4 != 3:
        draw.point((x + 14, y + 8), fill=palette["ROJO"])
        draw.point((x + 18, y + 8), fill=palette["ROJO"])


def draw_statue_attack(draw, x, y, palette):
    """Dibuja estatua atacando."""
    draw_statue_idle(draw, x, y, 0, palette)

    # Brazo extendido
    draw.rectangle([x + 24, y + 14, x + 30, y + 18], fill=palette["PIEDRA"])

    # Efecto de golpe
    draw.point((x + 30, y + 16), fill=palette["BLANCO"])


def generate_enemies_spritesheet(scale=1, palette_name="default", output_dir="assets"):
    """Genera spritesheet de enemigos."""
    palette = get_palette(palette_name)

    # Rata: 4 frames run
    rat_frames = 4
    rat_size = 16

    # Estatua: 4 frames idle + 2 frames attack
    statue_frames = 6
    statue_size = 32

    # Sheet layout: [ratas] [estatuas]
    sheet_w = (rat_frames * rat_size) + (statue_frames * statue_size)
    sheet_h = statue_size

    img = Image.new("RGBA", (sheet_w, sheet_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    meta = {"enemies": {}}

    # Ratas
    x_offset = 0
    rat_data = []
    for i in range(rat_frames):
        draw_rat_run(draw, x_offset, (sheet_h - rat_size) // 2, i, palette)
        rat_data.append(
            {
                "x": x_offset,
                "y": (sheet_h - rat_size) // 2,
                "w": rat_size,
                "h": rat_size,
                "duration": 100,
            }
        )
        x_offset += rat_size

    meta["enemies"]["rat"] = {
        "size": rat_size,
        "animations": {"run": {"frames": rat_data, "loop": True}},
    }

    # Estatuas
    statue_data_idle = []
    for i in range(4):
        draw_statue_idle(draw, x_offset, 0, i, palette)
        statue_data_idle.append(
            {"x": x_offset, "y": 0, "w": statue_size, "h": statue_size, "duration": 200}
        )
        x_offset += statue_size

    statue_data_attack = []
    for i in range(2):
        draw_statue_attack(draw, x_offset, 0, palette)
        statue_data_attack.append(
            {"x": x_offset, "y": 0, "w": statue_size, "h": statue_size, "duration": 150}
        )
        x_offset += statue_size

    meta["enemies"]["statue"] = {
        "size": statue_size,
        "animations": {
            "idle": {"frames": statue_data_idle, "loop": True},
            "attack": {"frames": statue_data_attack, "loop": False},
        },
    }

    if scale > 1:
        img = img.resize((sheet_w * scale, sheet_h * scale), Image.NEAREST)

    output_path = Path(output_dir)
    (output_path / "sprites").mkdir(parents=True, exist_ok=True)
    (output_path / "meta").mkdir(exist_ok=True)

    img.save(output_path / "sprites" / "enemies_spritesheet.png")

    with open(output_path / "meta" / "enemies.json", "w") as f:
        json.dump(meta, f, indent=2)

    print("✓ Enemigos generados: rata, estatua")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, default=1)
    parser.add_argument("--palette", default="default")
    parser.add_argument("--out", default="assets")
    args = parser.parse_args()

    generate_enemies_spritesheet(args.scale, args.palette, args.out)
