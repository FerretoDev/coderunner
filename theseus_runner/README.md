# Theseus Runner - Generador de Assets Pixel Art

Sistema completo de generación programática de assets para el juego "Theseus Runner", un runner/auto-scroll basado en el mito del Minotauro.

## Características

- **Generación 100% programática**: Todos los assets se crean mediante código Python
- **Estilo pixel art retro**: Paleta limitada de 16 colores, píxeles perfectos sin anti-aliasing
- **Escalable**: Todos los sprites diseñados para escalar por enteros (x2, x3, x4)
- **Completo**: Personajes, tiles, UI, fuentes, audio, efectos y fondos

## Paleta de Colores (16 colores)

```
NEGRO = #0d0d0d
GRIS_OSCURO = #3a3a3a
GRIS = #6b6b6b
GRIS_CLARO = #a0a0a0
BLANCO = #e8e8e8

PIEDRA_OSCURA = #4a3c2e
PIEDRA = #6b5544
PIEDRA_CLARA = #8b7355

ROJO_OSCURO = #6b2020
ROJO = #b83232
ROJO_CLARO = #e85050

AZUL_OSCURO = #2a4a6b
AZUL = #4080c0
AZUL_CLARO = #80b0e8

ORO = #d4af37
```

## Instalación

```bash
cd theseus_runner
pip install -r requirements.txt
```

## Generación de Assets

### Generar todos los assets:
```bash
python generate_all.py
```

### Generar assets específicos:
```bash
python scripts/generate_theseus.py --scale 2 --out assets/
python scripts/generate_minotaur.py --scale 2 --out assets/
python scripts/generate_tileset.py --scale 1 --out assets/
python scripts/generate_ui.py --out assets/
python scripts/generate_audio.py --out assets/
```

### Opciones disponibles:
- `--scale N`: Escala los sprites por N (1, 2, 3, 4)
- `--palette alt1`: Usa paleta alternativa (noche, lava)
- `--out DIR`: Directorio de salida (default: assets/)

## Estructura de Assets Generados

```
assets/
├── sprites/
│   ├── theseus_spritesheet.png
│   ├── minotaur_spritesheet.png
│   ├── enemies_spritesheet.png
│   └── collectibles_spritesheet.png
├── tiles/
│   ├── tileset_16.png
│   └── tileset_32.png
├── ui/
│   ├── button_start.png
│   ├── button_options.png
│   ├── healthbar.png
│   └── icons.png
├── fonts/
│   └── theseus_font.png
├── bg/
│   ├── parallax_0.png
│   ├── parallax_1.png
│   └── parallax_2.png
├── audio/
│   ├── menu_loop.wav
│   ├── game_loop.wav
│   ├── boss_loop.wav
│   └── sfx_*.wav
└── meta/
    ├── theseus.json
    ├── minotaur.json
    ├── tileset_16.json
    └── font.json
```

## Uso en Pygame

### Cargar spritesheet con metadata:

```python
import pygame
import json
from pathlib import Path

class AnimatedSprite:
    def __init__(self, spritesheet_path, meta_path):
        # Cargar spritesheet
        self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
        
        # Cargar metadata
        with open(meta_path) as f:
            self.meta = json.load(f)
        
        # Extraer frames
        self.frames = {}
        for anim_name, anim_data in self.meta['animations'].items():
            frames = []
            for frame in anim_data['frames']:
                rect = pygame.Rect(frame['x'], frame['y'], 
                                  frame['w'], frame['h'])
                surface = self.spritesheet.subsurface(rect)
                frames.append(surface)
            self.frames[anim_name] = frames
    
    def get_frame(self, animation, index):
        return self.frames[animation][index % len(self.frames[animation])]

# Uso
theseus = AnimatedSprite('assets/sprites/theseus_spritesheet.png',
                         'assets/meta/theseus.json')
frame = theseus.get_frame('run', 0)
screen.blit(frame, (100, 100))
```

### Cargar tileset:

```python
def load_tileset(image_path, meta_path, tile_size=16):
    image = pygame.image.load(image_path).convert_alpha()
    with open(meta_path) as f:
        meta = json.load(f)
    
    tiles = []
    for tile in meta['tiles']:
        x = (tile['id'] % (image.get_width() // tile_size)) * tile_size
        y = (tile['id'] // (image.get_width() // tile_size)) * tile_size
        rect = pygame.Rect(x, y, tile_size, tile_size)
        tiles.append(image.subsurface(rect))
    
    return tiles

tiles = load_tileset('assets/tiles/tileset_16.png',
                    'assets/meta/tileset_16.json', 16)
```

## Demo

Ejecuta el demo interactivo:
```bash
python demo.py
```

El demo muestra:
- Pantalla de título con logo animado
- Animaciones de Theseus (idle, run, jump)
- Animaciones del Minotauro
- Tileset del laberinto
- UI y HUD básico
- Efectos de partículas

## Variantes de Paleta

Genera assets con paletas alternativas:

```bash
# Modo noche (tonos azules oscuros)
python generate_all.py --palette night

# Modo lava (tonos rojos/naranjas)
python generate_all.py --palette lava
```

## Créditos

Todos los assets generados programáticamente usando Python + Pillow.
Música generada con síntesis de onda simple (chiptune).
Compatible con Pygame 2.0+.
