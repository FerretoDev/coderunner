"""
Generador de elementos UI (botones, HUD, iconos).
"""

import json
from pathlib import Path
from PIL import Image, ImageDraw
import sys
sys.path.append(str(Path(__file__).parent.parent))
from palette import get_palette


def draw_button(draw, x, y, w, h, palette, state='normal'):
    """Dibuja un botón pixel art."""
    colors = {
        'normal': palette['AZUL'],
        'hover': palette['AZUL_CLARO'],
        'pressed': palette['AZUL_OSCURO']
    }
    
    color = colors.get(state, palette['AZUL'])
    
    # Fondo
    draw.rectangle([x + 2, y + 2, x + w - 3, y + h - 3], fill=color)
    
    # Borde
    draw.rectangle([x, y, x + w - 1, y + h - 1], outline=palette['BLANCO'])
    
    # Sombra
    if state != 'pressed':
        draw.line([x + 2, y + h - 1, x + w - 1, y + h - 1], fill=palette['GRIS_OSCURO'])
        draw.line([x + w - 1, y + 2, x + w - 1, y + h - 1], fill=palette['GRIS_OSCURO'])


def draw_health_bar(draw, x, y, width, height, palette, fill_percent):
    """Dibuja barra de vida."""
    # Fondo
    draw.rectangle([x, y, x + width - 1, y + height - 1], fill=palette['GRIS_OSCURO'])
    
    # Vida
    fill_width = int((width - 4) * fill_percent)
    if fill_percent > 0.5:
        color = palette['AZUL_CLARO']
    elif fill_percent > 0.25:
        color = palette['ORO']
    else:
        color = palette['ROJO']
    
    if fill_width > 0:
        draw.rectangle([x + 2, y + 2, x + 2 + fill_width, y + height - 3], fill=color)
    
    # Borde
    draw.rectangle([x, y, x + width - 1, y + height - 1], outline=palette['BLANCO'])


def draw_key_icon(draw, x, y, size, palette):
    """Dibuja icono de llave."""
    # Cabeza de llave
    draw.ellipse([x + 2, y + 2, x + size // 2, y + size // 2], fill=palette['ORO'])
    
    # Vástago
    draw.rectangle([x + size // 4, y + size // 2, 
                   x + size // 2, y + size - 4], fill=palette['ORO'])
    
    # Dientes
    draw.point((x + size // 4, y + size - 4), fill=palette['ORO'])
    draw.point((x + size // 2, y + size - 6), fill=palette['ORO'])


def draw_gem_icon(draw, x, y, size, palette):
    """Dibuja icono de gema."""
    center_x = x + size // 2
    center_y = y + size // 2
    
    # Diamante
    points = [
        (center_x, y + 2),
        (x + size - 2, center_y),
        (center_x, y + size - 2),
        (x + 2, center_y)
    ]
    
    draw.polygon(points, fill=palette['AZUL_CLARO'])
    draw.polygon(points, outline=palette['BLANCO'])


def draw_coin_icon(draw, x, y, size, palette):
    """Dibuja icono de moneda."""
    draw.ellipse([x + 2, y + 2, x + size - 3, y + size - 3], fill=palette['ORO'])
    draw.ellipse([x + 4, y + 4, x + size - 5, y + size - 5], outline=palette['BLANCO'])


def generate_ui_assets(scale=1, palette_name='default', output_dir='assets'):
    """Genera todos los assets de UI."""
    palette = get_palette(palette_name)
    
    # Panel de botones (3 estados: normal, hover, pressed)
    button_w, button_h = 64, 16
    buttons_img = Image.new('RGBA', (button_w * 3, button_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(buttons_img)
    
    for i, state in enumerate(['normal', 'hover', 'pressed']):
        draw_button(draw, i * button_w, 0, button_w, button_h, palette, state)
    
    # HUD elements
    hud_img = Image.new('RGBA', (128, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(hud_img)
    
    # Barras de vida en diferentes estados
    for i, percent in enumerate([1.0, 0.6, 0.3]):
        draw_health_bar(draw, 4, i * 12, 100, 8, palette, percent)
    
    # Iconos
    icons_img = Image.new('RGBA', (16 * 3, 16), (0, 0, 0, 0))
    draw = ImageDraw.Draw(icons_img)
    
    draw_key_icon(draw, 0, 0, 16, palette)
    draw_gem_icon(draw, 16, 0, 16, palette)
    draw_coin_icon(draw, 32, 0, 16, palette)
    
    # Escalar si es necesario
    if scale > 1:
        buttons_img = buttons_img.resize(
            (buttons_img.width * scale, buttons_img.height * scale), 
            Image.NEAREST
        )
        hud_img = hud_img.resize(
            (hud_img.width * scale, hud_img.height * scale), 
            Image.NEAREST
        )
        icons_img = icons_img.resize(
            (icons_img.width * scale, icons_img.height * scale), 
            Image.NEAREST
        )
    
    # Guardar
    output_path = Path(output_dir)
    (output_path / 'ui').mkdir(parents=True, exist_ok=True)
    (output_path / 'meta').mkdir(exist_ok=True)
    
    buttons_img.save(output_path / 'ui' / 'buttons.png')
    hud_img.save(output_path / 'ui' / 'hud.png')
    icons_img.save(output_path / 'ui' / 'icons.png')
    
    # Metadata
    meta = {
        'buttons': {
            'width': button_w,
            'height': button_h,
            'states': ['normal', 'hover', 'pressed']
        },
        'health_bar': {
            'width': 100,
            'height': 8
        },
        'icons': {
            'size': 16,
            'types': ['key', 'gem', 'coin']
        }
    }
    
    with open(output_path / 'meta' / 'ui.json', 'w') as f:
        json.dump(meta, f, indent=2)
    
    print("✓ UI assets generados")
    print(f"  - {output_path / 'ui' / 'buttons.png'}")
    print(f"  - {output_path / 'ui' / 'hud.png'}")
    print(f"  - {output_path / 'ui' / 'icons.png'}")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--scale', type=int, default=1)
    parser.add_argument('--palette', default='default')
    parser.add_argument('--out', default='assets')
    args = parser.parse_args()
    
    generate_ui_assets(args.scale, args.palette, args.out)
