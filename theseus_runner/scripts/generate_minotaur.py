"""
Generador de spritesheet para el Minotauro (enemigo/boss principal).

Animaciones:
- idle: 2 frames
- walk: 4 frames
- charge: 6 frames
- roar: 3 frames
- death: 4 frames

Tamaño base: 48x48 píxeles
"""

import argparse
from pathlib import Path
from PIL import Image, ImageDraw
import json
from palette import get_palette


def draw_pixel_rect(draw, x, y, w, h, color):
    """Dibuja un rectángulo de píxeles."""
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=color)


def draw_minotaur_head(draw, x, y, palette, angry=False):
    """Dibuja la cabeza del Minotauro."""
    # Cara/hocico
    draw_pixel_rect(draw, x + 16, y + 8, 16, 12, palette["ROJO_OSCURO"])

    # Ojos rojos
    eye_color = palette["ROJO_CLARO"] if angry else palette["ROJO"]
    draw.point((x + 19, y + 11), fill=eye_color)
    draw.point((x + 28, y + 11), fill=eye_color)

    # Hocico/nariz
    draw_pixel_rect(draw, x + 22, y + 16, 4, 3, palette["NEGRO"])

    # Cuernos
    draw_pixel_rect(draw, x + 12, y + 4, 4, 8, palette["BLANCO"])
    draw_pixel_rect(draw, x + 32, y + 4, 4, 8, palette["BLANCO"])
    # Puntas de cuernos
    draw_pixel_rect(draw, x + 10, y + 2, 2, 4, palette["GRIS"])
    draw_pixel_rect(draw, x + 36, y + 2, 2, 4, palette["GRIS"])


def draw_minotaur_idle(draw, x_offset, y_offset, frame, palette):
    """Dibuja frame idle del Minotauro."""
    # Cabeza
    draw_minotaur_head(draw, x_offset, y_offset, palette)

    # Torso masivo
    draw_pixel_rect(draw, x_offset + 12, y_offset + 20, 24, 16, palette["ROJO"])

    # Respiración (expandir/contraer ligeramente)
    if frame == 1:
        draw_pixel_rect(draw, x_offset + 10, y_offset + 22, 2, 12, palette["ROJO"])
        draw_pixel_rect(draw, x_offset + 36, y_offset + 22, 2, 12, palette["ROJO"])

    # Brazos musculosos
    draw_pixel_rect(draw, x_offset + 4, y_offset + 22, 8, 12, palette["ROJO_CLARO"])
    draw_pixel_rect(draw, x_offset + 36, y_offset + 22, 8, 12, palette["ROJO_CLARO"])

    # Manos/garras
    draw_pixel_rect(draw, x_offset + 2, y_offset + 32, 6, 4, palette["GRIS_OSCURO"])
    draw_pixel_rect(draw, x_offset + 40, y_offset + 32, 6, 4, palette["GRIS_OSCURO"])

    # Piernas
    draw_pixel_rect(draw, x_offset + 14, y_offset + 36, 8, 10, palette["ROJO_OSCURO"])
    draw_pixel_rect(draw, x_offset + 26, y_offset + 36, 8, 10, palette["ROJO_OSCURO"])

    # Pezuñas
    draw_pixel_rect(draw, x_offset + 14, y_offset + 44, 8, 4, palette["NEGRO"])
    draw_pixel_rect(draw, x_offset + 26, y_offset + 44, 8, 4, palette["NEGRO"])


def draw_minotaur_walk(draw, x_offset, y_offset, frame, palette):
    """Dibuja frame walk del Minotauro."""
    # Cabeza
    draw_minotaur_head(draw, x_offset, y_offset, palette)

    # Torso
    draw_pixel_rect(draw, x_offset + 12, y_offset + 20, 24, 16, palette["ROJO"])

    # Brazos balanceándose
    arm_swing = 2 if frame % 2 == 0 else -2
    draw_pixel_rect(
        draw, x_offset + 4, y_offset + 22 + arm_swing, 8, 12, palette["ROJO_CLARO"]
    )
    draw_pixel_rect(
        draw, x_offset + 36, y_offset + 22 - arm_swing, 8, 12, palette["ROJO_CLARO"]
    )

    # Manos
    draw_pixel_rect(
        draw, x_offset + 2, y_offset + 32 + arm_swing, 6, 4, palette["GRIS_OSCURO"]
    )
    draw_pixel_rect(
        draw, x_offset + 40, y_offset + 32 - arm_swing, 6, 4, palette["GRIS_OSCURO"]
    )

    # Piernas alternadas
    if frame < 2:
        draw_pixel_rect(
            draw, x_offset + 14, y_offset + 34, 8, 12, palette["ROJO_OSCURO"]
        )
        draw_pixel_rect(
            draw, x_offset + 26, y_offset + 38, 8, 8, palette["ROJO_OSCURO"]
        )
    else:
        draw_pixel_rect(
            draw, x_offset + 14, y_offset + 38, 8, 8, palette["ROJO_OSCURO"]
        )
        draw_pixel_rect(
            draw, x_offset + 26, y_offset + 34, 8, 12, palette["ROJO_OSCURO"]
        )

    # Pezuñas
    draw_pixel_rect(draw, x_offset + 14, y_offset + 44, 8, 4, palette["NEGRO"])
    draw_pixel_rect(draw, x_offset + 26, y_offset + 44, 8, 4, palette["NEGRO"])


def draw_minotaur_charge(draw, x_offset, y_offset, frame, palette):
    """Dibuja frame charge/attack del Minotauro."""
    # Cabeza inclinada (embestida)
    head_forward = min(frame * 2, 8)
    draw_minotaur_head(draw, x_offset + head_forward, y_offset + 4, palette, angry=True)

    # Torso inclinado hacia adelante
    draw_pixel_rect(
        draw, x_offset + 14 + head_forward // 2, y_offset + 22, 20, 14, palette["ROJO"]
    )

    # Brazos hacia atrás (preparando embestida)
    draw_pixel_rect(draw, x_offset + 6, y_offset + 26, 8, 10, palette["ROJO_CLARO"])
    draw_pixel_rect(draw, x_offset + 34, y_offset + 26, 8, 10, palette["ROJO_CLARO"])

    # Piernas en posición de carrera
    if frame < 3:
        draw_pixel_rect(
            draw, x_offset + 12, y_offset + 36, 8, 10, palette["ROJO_OSCURO"]
        )
        draw_pixel_rect(
            draw, x_offset + 28, y_offset + 38, 8, 8, palette["ROJO_OSCURO"]
        )
    else:
        draw_pixel_rect(
            draw, x_offset + 12, y_offset + 38, 8, 8, palette["ROJO_OSCURO"]
        )
        draw_pixel_rect(
            draw, x_offset + 28, y_offset + 36, 8, 10, palette["ROJO_OSCURO"]
        )

    # Partículas de polvo
    if frame > 2:
        for i in range(3):
            draw.point((x_offset + 8 - i * 4, y_offset + 44), fill=palette["GRIS"])


def draw_minotaur_roar(draw, x_offset, y_offset, frame, palette):
    """Dibuja frame roar del Minotauro."""
    # Cabeza hacia atrás
    draw_minotaur_head(draw, x_offset, y_offset - 2, palette, angry=True)

    # Boca abierta
    draw_pixel_rect(draw, x_offset + 22, y_offset + 16, 4, 4, palette["ROJO_CLARO"])

    # Torso expandido
    draw_pixel_rect(draw, x_offset + 10, y_offset + 20, 28, 16, palette["ROJO"])

    # Brazos arriba (rugiendo)
    draw_pixel_rect(draw, x_offset + 2, y_offset + 16, 8, 12, palette["ROJO_CLARO"])
    draw_pixel_rect(draw, x_offset + 38, y_offset + 16, 8, 12, palette["ROJO_CLARO"])

    # Ondas de sonido (frame 2)
    if frame == 2:
        for offset in [(4, 10), (42, 10), (8, 14), (38, 14)]:
            draw.point(
                (x_offset + offset[0], y_offset + offset[1]), fill=palette["BLANCO"]
            )

    # Piernas firmes
    draw_pixel_rect(draw, x_offset + 14, y_offset + 36, 8, 12, palette["ROJO_OSCURO"])
    draw_pixel_rect(draw, x_offset + 26, y_offset + 36, 8, 12, palette["ROJO_OSCURO"])


def draw_minotaur_death(draw, x_offset, y_offset, frame, palette):
    """Dibuja frame death del Minotauro."""
    if frame < 2:
        # Tambaleándose
        tilt = frame * 4
        draw_minotaur_head(draw, x_offset + tilt, y_offset + frame * 2, palette)
        draw_pixel_rect(
            draw,
            x_offset + 12 + tilt,
            y_offset + 20 + frame * 2,
            24,
            16,
            palette["ROJO"],
        )
        draw_pixel_rect(
            draw,
            x_offset + 14,
            y_offset + 36,
            8,
            12 - frame * 4,
            palette["ROJO_OSCURO"],
        )
        draw_pixel_rect(
            draw,
            x_offset + 26,
            y_offset + 36,
            8,
            12 - frame * 4,
            palette["ROJO_OSCURO"],
        )
    else:
        # Caído en el suelo
        y = y_offset + 32
        draw_pixel_rect(draw, x_offset + 4, y, 40, 12, palette["ROJO"])
        draw_pixel_rect(draw, x_offset + 8, y - 6, 16, 6, palette["ROJO_OSCURO"])

        # Cuernos en el suelo
        draw_pixel_rect(draw, x_offset + 2, y - 2, 4, 4, palette["GRIS"])


def generate_minotaur_spritesheet(scale=1, palette_name="default", output_dir="assets"):
    """Genera el spritesheet completo del Minotauro."""
    palette = get_palette(palette_name)

    sprite_w, sprite_h = 48, 48
    animations = {
        "idle": 2,
        "walk": 4,
        "charge": 6,
        "roar": 3,
        "death": 4,
    }

    total_frames = sum(animations.values())
    sheet_width = sprite_w * total_frames
    sheet_height = sprite_h

    img = Image.new("RGBA", (sheet_width, sheet_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    meta = {
        "name": "minotaur",
        "sprite_width": sprite_w,
        "sprite_height": sprite_h,
        "animations": {},
    }

    frame_x = 0

    # Idle
    frames_data = []
    for i in range(animations["idle"]):
        draw_minotaur_idle(draw, frame_x, 0, i, palette)
        frames_data.append(
            {"x": frame_x, "y": 0, "w": sprite_w, "h": sprite_h, "duration": 600}
        )
        frame_x += sprite_w
    meta["animations"]["idle"] = {"frames": frames_data, "loop": True}

    # Walk
    frames_data = []
    for i in range(animations["walk"]):
        draw_minotaur_walk(draw, frame_x, 0, i, palette)
        frames_data.append(
            {"x": frame_x, "y": 0, "w": sprite_w, "h": sprite_h, "duration": 150}
        )
        frame_x += sprite_w
    meta["animations"]["walk"] = {"frames": frames_data, "loop": True}

    # Charge
    frames_data = []
    for i in range(animations["charge"]):
        draw_minotaur_charge(draw, frame_x, 0, i, palette)
        frames_data.append(
            {"x": frame_x, "y": 0, "w": sprite_w, "h": sprite_h, "duration": 80}
        )
        frame_x += sprite_w
    meta["animations"]["charge"] = {"frames": frames_data, "loop": False}

    # Roar
    frames_data = []
    for i in range(animations["roar"]):
        draw_minotaur_roar(draw, frame_x, 0, i, palette)
        frames_data.append(
            {"x": frame_x, "y": 0, "w": sprite_w, "h": sprite_h, "duration": 300}
        )
        frame_x += sprite_w
    meta["animations"]["roar"] = {"frames": frames_data, "loop": False}

    # Death
    frames_data = []
    for i in range(animations["death"]):
        draw_minotaur_death(draw, frame_x, 0, i, palette)
        frames_data.append(
            {"x": frame_x, "y": 0, "w": sprite_w, "h": sprite_h, "duration": 250}
        )
        frame_x += sprite_w
    meta["animations"]["death"] = {"frames": frames_data, "loop": False}

    if scale > 1:
        new_size = (sheet_width * scale, sheet_height * scale)
        img = img.resize(new_size, Image.NEAREST)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    (output_path / "sprites").mkdir(exist_ok=True)
    (output_path / "meta").mkdir(exist_ok=True)

    img.save(output_path / "sprites" / "minotaur_spritesheet.png")

    with open(output_path / "meta" / "minotaur.json", "w") as f:
        json.dump(meta, f, indent=2)

    print(f"✓ Minotaur spritesheet generado: {total_frames} frames")
    print(f"  - {output_path / 'sprites' / 'minotaur_spritesheet.png'}")
    print(f"  - {output_path / 'meta' / 'minotaur.json'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Genera spritesheet del Minotauro")
    parser.add_argument("--scale", type=int, default=1)
    parser.add_argument("--palette", default="default")
    parser.add_argument("--out", default="assets")

    args = parser.parse_args()
    generate_minotaur_spritesheet(args.scale, args.palette, args.out)
