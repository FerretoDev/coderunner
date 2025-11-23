"""
Generador de spritesheet para Theseus (personaje principal).

Animaciones:
- idle: 2 frames
- run: 6 frames
- jump: 2 frames
- slide: 2 frames
- death: 4 frames

Tamaño base: 32x48 píxeles
"""

import argparse
from pathlib import Path
from PIL import Image, ImageDraw
import json
from palette import get_palette


def draw_pixel_rect(draw, x, y, w, h, color):
    """Dibuja un rectángulo de píxeles."""
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=color)


def draw_theseus_idle(draw, x_offset, y_offset, frame, palette):
    """Dibuja frame de animación idle."""
    # Cabeza
    draw_pixel_rect(draw, x_offset + 12, y_offset + 4, 8, 8, palette["AZUL"])

    # Casco/casco
    draw_pixel_rect(draw, x_offset + 10, y_offset + 2, 12, 3, palette["AZUL_OSCURO"])

    # Ojos
    draw.point((x_offset + 14, y_offset + 7), fill=palette["BLANCO"])
    draw.point((x_offset + 17, y_offset + 7), fill=palette["BLANCO"])

    # Cuerpo
    draw_pixel_rect(draw, x_offset + 10, y_offset + 12, 12, 14, palette["AZUL"])

    # Cinturón
    draw_pixel_rect(draw, x_offset + 10, y_offset + 20, 12, 2, palette["GRIS_OSCURO"])

    # Brazos
    if frame == 0:
        draw_pixel_rect(draw, x_offset + 6, y_offset + 14, 4, 10, palette["AZUL_CLARO"])
        draw_pixel_rect(
            draw, x_offset + 22, y_offset + 14, 4, 10, palette["AZUL_CLARO"]
        )
    else:
        draw_pixel_rect(draw, x_offset + 6, y_offset + 15, 4, 10, palette["AZUL_CLARO"])
        draw_pixel_rect(
            draw, x_offset + 22, y_offset + 13, 4, 10, palette["AZUL_CLARO"]
        )

    # Piernas
    draw_pixel_rect(draw, x_offset + 11, y_offset + 26, 5, 10, palette["AZUL_OSCURO"])
    draw_pixel_rect(draw, x_offset + 16, y_offset + 26, 5, 10, palette["AZUL_OSCURO"])

    # Pies
    draw_pixel_rect(draw, x_offset + 10, y_offset + 36, 6, 4, palette["GRIS_OSCURO"])
    draw_pixel_rect(draw, x_offset + 16, y_offset + 36, 6, 4, palette["GRIS_OSCURO"])

    # Espada
    draw_pixel_rect(draw, x_offset + 24, y_offset + 18, 2, 12, palette["GRIS"])
    draw_pixel_rect(draw, x_offset + 24, y_offset + 16, 2, 2, palette["ORO"])


def draw_theseus_run(draw, x_offset, y_offset, frame, palette):
    """Dibuja frame de animación run."""
    # Cabeza
    draw_pixel_rect(draw, x_offset + 12, y_offset + 2, 8, 8, palette["AZUL"])

    # Casco
    draw_pixel_rect(draw, x_offset + 10, y_offset + 0, 12, 3, palette["AZUL_OSCURO"])

    # Penacho (cresta)
    if frame % 2 == 0:
        draw_pixel_rect(draw, x_offset + 14, y_offset - 2, 4, 3, palette["ROJO"])

    # Ojos
    draw.point((x_offset + 14, y_offset + 5), fill=palette["BLANCO"])
    draw.point((x_offset + 17, y_offset + 5), fill=palette["BLANCO"])

    # Cuerpo inclinado
    draw_pixel_rect(draw, x_offset + 11, y_offset + 10, 10, 14, palette["AZUL"])

    # Brazos en movimiento
    arm_offset = -2 if frame % 2 == 0 else 2
    draw_pixel_rect(
        draw, x_offset + 7, y_offset + 12 + arm_offset, 4, 8, palette["AZUL_CLARO"]
    )
    draw_pixel_rect(
        draw, x_offset + 21, y_offset + 12 - arm_offset, 4, 8, palette["AZUL_CLARO"]
    )

    # Piernas en ciclo
    if frame < 2:
        # Pierna izquierda adelante
        draw_pixel_rect(
            draw, x_offset + 8, y_offset + 24, 5, 10, palette["AZUL_OSCURO"]
        )
        draw_pixel_rect(
            draw, x_offset + 16, y_offset + 28, 5, 8, palette["AZUL_OSCURO"]
        )
    elif frame < 4:
        # Ambas piernas juntas
        draw_pixel_rect(
            draw, x_offset + 11, y_offset + 24, 5, 12, palette["AZUL_OSCURO"]
        )
        draw_pixel_rect(
            draw, x_offset + 15, y_offset + 26, 5, 10, palette["AZUL_OSCURO"]
        )
    else:
        # Pierna derecha adelante
        draw_pixel_rect(
            draw, x_offset + 15, y_offset + 24, 5, 10, palette["AZUL_OSCURO"]
        )
        draw_pixel_rect(draw, x_offset + 9, y_offset + 28, 5, 8, palette["AZUL_OSCURO"])

    # Pies
    draw_pixel_rect(draw, x_offset + 8, y_offset + 36, 6, 3, palette["GRIS_OSCURO"])
    draw_pixel_rect(draw, x_offset + 15, y_offset + 38, 6, 3, palette["GRIS_OSCURO"])

    # Espada
    draw_pixel_rect(draw, x_offset + 23, y_offset + 14, 2, 10, palette["GRIS"])
    draw_pixel_rect(draw, x_offset + 23, y_offset + 12, 2, 2, palette["ORO"])


def draw_theseus_jump(draw, x_offset, y_offset, frame, palette):
    """Dibuja frame de animación jump."""
    # Cabeza
    draw_pixel_rect(draw, x_offset + 12, y_offset + 6, 8, 8, palette["AZUL"])

    # Casco
    draw_pixel_rect(draw, x_offset + 10, y_offset + 4, 12, 3, palette["AZUL_OSCURO"])

    # Cuerpo
    draw_pixel_rect(draw, x_offset + 10, y_offset + 14, 12, 12, palette["AZUL"])

    # Brazos arriba
    if frame == 0:
        draw_pixel_rect(draw, x_offset + 4, y_offset + 10, 6, 8, palette["AZUL_CLARO"])
        draw_pixel_rect(draw, x_offset + 22, y_offset + 10, 6, 8, palette["AZUL_CLARO"])
    else:
        draw_pixel_rect(draw, x_offset + 4, y_offset + 8, 6, 10, palette["AZUL_CLARO"])
        draw_pixel_rect(draw, x_offset + 22, y_offset + 8, 6, 10, palette["AZUL_CLARO"])

    # Piernas dobladas
    draw_pixel_rect(draw, x_offset + 10, y_offset + 26, 6, 8, palette["AZUL_OSCURO"])
    draw_pixel_rect(draw, x_offset + 16, y_offset + 26, 6, 8, palette["AZUL_OSCURO"])


def draw_theseus_slide(draw, x_offset, y_offset, frame, palette):
    """Dibuja frame de animación slide/duck."""
    # Cabeza agachada
    draw_pixel_rect(draw, x_offset + 12, y_offset + 20, 8, 8, palette["AZUL"])

    # Casco
    draw_pixel_rect(draw, x_offset + 10, y_offset + 18, 12, 3, palette["AZUL_OSCURO"])

    # Cuerpo horizontal
    draw_pixel_rect(draw, x_offset + 6, y_offset + 28, 20, 8, palette["AZUL"])

    # Brazo extendido
    draw_pixel_rect(draw, x_offset + 2, y_offset + 30, 6, 4, palette["AZUL_CLARO"])

    # Piernas dobladas
    draw_pixel_rect(draw, x_offset + 16, y_offset + 34, 10, 6, palette["AZUL_OSCURO"])


def draw_theseus_death(draw, x_offset, y_offset, frame, palette):
    """Dibuja frame de animación death."""
    if frame < 2:
        # Cayendo
        draw_pixel_rect(
            draw, x_offset + 10, y_offset + 10 + frame * 4, 12, 12, palette["AZUL"]
        )
        draw_pixel_rect(
            draw, x_offset + 12, y_offset + 6 + frame * 4, 8, 6, palette["AZUL"]
        )
        draw_pixel_rect(
            draw, x_offset + 6, y_offset + 14 + frame * 4, 6, 8, palette["AZUL_CLARO"]
        )
        draw_pixel_rect(
            draw, x_offset + 20, y_offset + 14 + frame * 4, 6, 8, palette["AZUL_CLARO"]
        )
    else:
        # En el suelo
        y = y_offset + 30
        draw_pixel_rect(draw, x_offset + 4, y, 24, 6, palette["AZUL"])
        draw_pixel_rect(draw, x_offset + 6, y - 4, 8, 4, palette["AZUL"])
        if frame == 3:
            # Partículas
            draw.point((x_offset + 2, y - 2), fill=palette["GRIS"])
            draw.point((x_offset + 28, y - 2), fill=palette["GRIS"])


def generate_theseus_spritesheet(scale=1, palette_name="default", output_dir="assets"):
    """Genera el spritesheet completo de Theseus."""
    palette = get_palette(palette_name)

    # Dimensiones
    sprite_w, sprite_h = 32, 48
    animations = {
        "idle": 2,
        "run": 6,
        "jump": 2,
        "slide": 2,
        "death": 4,
    }

    total_frames = sum(animations.values())
    sheet_width = sprite_w * total_frames
    sheet_height = sprite_h

    # Crear imagen
    img = Image.new("RGBA", (sheet_width, sheet_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Metadata
    meta = {
        "name": "theseus",
        "sprite_width": sprite_w,
        "sprite_height": sprite_h,
        "animations": {},
    }

    frame_x = 0

    # Idle
    frames_data = []
    for i in range(animations["idle"]):
        draw_theseus_idle(draw, frame_x, 0, i, palette)
        frames_data.append(
            {"x": frame_x, "y": 0, "w": sprite_w, "h": sprite_h, "duration": 500}
        )
        frame_x += sprite_w
    meta["animations"]["idle"] = {"frames": frames_data, "loop": True}

    # Run
    frames_data = []
    for i in range(animations["run"]):
        draw_theseus_run(draw, frame_x, 0, i, palette)
        frames_data.append(
            {"x": frame_x, "y": 0, "w": sprite_w, "h": sprite_h, "duration": 100}
        )
        frame_x += sprite_w
    meta["animations"]["run"] = {"frames": frames_data, "loop": True}

    # Jump
    frames_data = []
    for i in range(animations["jump"]):
        draw_theseus_jump(draw, frame_x, 0, i, palette)
        frames_data.append(
            {"x": frame_x, "y": 0, "w": sprite_w, "h": sprite_h, "duration": 200}
        )
        frame_x += sprite_w
    meta["animations"]["jump"] = {"frames": frames_data, "loop": False}

    # Slide
    frames_data = []
    for i in range(animations["slide"]):
        draw_theseus_slide(draw, frame_x, 0, i, palette)
        frames_data.append(
            {"x": frame_x, "y": 0, "w": sprite_w, "h": sprite_h, "duration": 150}
        )
        frame_x += sprite_w
    meta["animations"]["slide"] = {"frames": frames_data, "loop": True}

    # Death
    frames_data = []
    for i in range(animations["death"]):
        draw_theseus_death(draw, frame_x, 0, i, palette)
        frames_data.append(
            {"x": frame_x, "y": 0, "w": sprite_w, "h": sprite_h, "duration": 200}
        )
        frame_x += sprite_w
    meta["animations"]["death"] = {"frames": frames_data, "loop": False}

    # Escalar si es necesario
    if scale > 1:
        new_size = (sheet_width * scale, sheet_height * scale)
        img = img.resize(new_size, Image.NEAREST)

    # Guardar
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    (output_path / "sprites").mkdir(exist_ok=True)
    (output_path / "meta").mkdir(exist_ok=True)

    img.save(output_path / "sprites" / "theseus_spritesheet.png")

    with open(output_path / "meta" / "theseus.json", "w") as f:
        json.dump(meta, f, indent=2)

    print(f"✓ Theseus spritesheet generado: {total_frames} frames")
    print(f"  - {output_path / 'sprites' / 'theseus_spritesheet.png'}")
    print(f"  - {output_path / 'meta' / 'theseus.json'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Genera spritesheet de Theseus")
    parser.add_argument("--scale", type=int, default=1, help="Escala del sprite (1-4)")
    parser.add_argument("--palette", default="default", help="Paleta de colores")
    parser.add_argument("--out", default="assets", help="Directorio de salida")

    args = parser.parse_args()
    generate_theseus_spritesheet(args.scale, args.palette, args.out)
