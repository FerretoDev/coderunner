# 🎨 Guía de Diseño UI/HUD - Theseus Runner
## Estilo Pixel Art Basado en Juegos Retro Clásicos

**IMPORTANTE**: Esta guía NO usa generación programática. Todos los elementos están basados en estilos reales de juegos retro existentes.

---

## 📐 Especificaciones Generales

### Paleta de Colores Base (inspirada en GBA/SNES)

```
REFERENCIAS:
- The Legend of Zelda: Minish Cap (GBA, 2004)
- Castlevania: Aria of Sorrow (GBA, 2003)
- Shovel Knight (2014, estilo NES/SNES)
```

**Paleta Principal (16 colores)**

```hex
UI_DARK:       #1a1c2c  (Fondo oscuro - estilo Dead Cells)
UI_GRAY:       #5d5d81  (Sombras - estilo Zelda GBA)
UI_LIGHT:      #c4c4d4  (Bordes claros - estilo Shovel Knight)
UI_WHITE:      #f4f4f4  (Highlights - universal retro)

UI_GOLD:       #ffd700  (Marcos dorados - estilo Castlevania)
UI_GOLD_DARK:  #b8860b  (Sombras doradas)

UI_BLUE:       #3b5dc9  (Azul primario - estilo Hyper Light Drifter)
UI_BLUE_LIGHT: #41a6f6  (Azul claro - iconos activos)

UI_RED:        #cc3333  (Vida baja/peligro - universal)
UI_RED_DARK:   #8b2528  (Sombras rojas)

UI_GREEN:      #38b764  (Vida completa - estilo Zelda)
UI_GREEN_DARK: #257179  (Sombras verdes)

TRANSPARENT:   #000000  (Color clave para transparencia)
```

---

## 1. 🔘 BOTONES ESTILO GBA/SNES

### Referencias Visuales
- **Shovel Knight** - Bordes gruesos pixelados (2px), sombras pronunciadas
- **The Legend of Zelda: Minish Cap** - Botones con bisel 3D sutil
- **Castlevania: Aria of Sorrow** - Marcos decorativos góticos

### Diseño de Botones

#### Tamaño Pequeño: 64×20px
```
ESTRUCTURA:
┌─────────────────────┐
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│ ← Borde superior claro (1px)
│▓░░░░░░░░░░░░░░░░░░▓│ ← Área de texto
│▓░░░░TEXTO░░░░░░░░░▓│
│▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓│ ← Sombra inferior (1px)
└─────────────────────┘

ESTADOS:
- Normal:  Fondo #3b5dc9, Borde #f4f4f4, Sombra #1a1c2c
- Hover:   Fondo #41a6f6, Borde #f4f4f4, Sombra #3b5dc9
- Pressed: Fondo #1a1c2c, Borde #5d5d81, Sombra #000000
```

#### Tamaño Mediano: 96×32px
```
Estilo Zelda GBA con esquinas redondeadas (2px radius en pixel art)

COLORES:
- Normal:  Gradiente #38b764 → #257179
- Hover:   Gradiente #41a6f6 → #3b5dc9
- Pressed: Sólido #1a1c2c con borde #5d5d81
```

#### Tamaño Grande: 128×40px
```
Estilo Castlevania con decoración gótica

ELEMENTOS:
- Marco exterior dorado (#ffd700)
- Esquinas decoradas con pequeños triángulos
- Centro degradado vertical
- Texto centrado con sombra pixelada
```

### Assets Recomendados
```
ui/buttons/
├── btn_small_normal.png    (64×20)
├── btn_small_hover.png     (64×20)
├── btn_small_pressed.png   (64×20)
├── btn_medium_normal.png   (96×32)
├── btn_medium_hover.png    (96×32)
├── btn_medium_pressed.png  (96×32)
├── btn_large_normal.png    (128×40)
├── btn_large_hover.png     (128×40)
└── btn_large_pressed.png   (128×40)
```

---

## 2. 🎯 ICONOS PIXEL ART (16×16 y 32×32)

### Corazón de Vida (estilo Zelda)

**Referencia**: The Legend of Zelda: A Link to the Past / Minish Cap

```
16×16px - Corazón completo:

    ▓▓    ▓▓
  ▓▓██▓▓▓▓██▓▓
 ▓██████████████▓
▓████████████████▓
▓████████████████▓
 ▓██████████████▓
  ▓████████████▓
   ▓██████████▓
    ▓████████▓
     ▓██████▓
      ▓████▓
       ▓██▓
        ▓▓

COLORES:
- Lleno:  #cc3333 (rojo), Borde #8b2528, Highlight #ff6666
- Medio:  #ffd700 (dorado)
- Vacío:  #5d5d81 (gris), solo contorno
```

**Archivo**: `ui/icons/heart_full.png`, `heart_half.png`, `heart_empty.png`

### Llave (estilo Minish Cap)

**Referencia**: The Legend of Zelda: Minish Cap - Small Key

```
16×16px - Llave dorada:

      ▓▓▓▓
     ▓████▓
     ▓▓██▓▓
       ██
       ██
       ██
       ██
      ▓██▓
      ▓▓▓▓

COLORES:
- Base: #ffd700
- Sombra: #b8860b
- Highlight: #ffff00
```

**Archivo**: `ui/icons/key_gold.png`, `key_silver.png`

### Casco Griego (estilo Castlevania)

**Referencia**: Castlevania: Aria of Sorrow - Armor Icons

```
32×32px - Casco espartano:

       ▓▓▓▓▓▓
      ▓██████▓
     ▓████████▓
    ▓██▓▓██▓▓██▓
    ▓██░░██░░██▓  ← Ojos
   ▓████████████▓
   ▓▓██████████▓▓
     ▓▓▓▓▓▓▓▓▓▓

COLORES:
- Metal: #c4c4d4, #5d5d81
- Cresta: #cc3333
- Sombras: #1a1c2c
```

**Archivo**: `ui/icons/helmet_spartan.png`

### Icono de Laberinto (estilo Hyper Light Drifter)

**Referencia**: Hyper Light Drifter - Map Icons

```
16×16px - Laberinto minimalista:

▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓░░▓░░░░░░▓░░░▓
▓░░▓▓▓▓▓░░▓░▓░▓
▓░░░░░░▓░░░░▓░▓
▓▓▓▓▓░░▓▓▓▓▓▓░▓
▓░░░░░░░░░░░░░▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

COLORES:
- Paredes: #3b5dc9
- Camino: #41a6f6
- Fondo: transparente o #1a1c2c
```

**Archivo**: `ui/icons/maze_icon.png`

### Iconos de Sistema (estilo Shovel Knight)

**Referencia**: Shovel Knight - UI Elements

```
16×16px - Pausa:

  ▓▓▓▓  ▓▓▓▓
  ▓██▓  ▓██▓
  ▓██▓  ▓██▓
  ▓██▓  ▓██▓
  ▓██▓  ▓██▓
  ▓▓▓▓  ▓▓▓▓

16×16px - Settings (engranaje):

    ▓▓▓▓
  ▓▓▓██▓▓▓
 ▓██▓▓▓▓██▓
▓███▓░░▓███▓
▓███▓░░▓███▓
 ▓██▓▓▓▓██▓
  ▓▓▓██▓▓▓
    ▓▓▓▓

COLORES:
- Base: #c4c4d4
- Sombra: #5d5d81
```

**Archivos**: `ui/icons/pause.png`, `ui/icons/settings.png`, `ui/icons/exit.png`

---

## 3. ❤️ BARRAS DE VIDA

### Estilo Zelda - Sistema de Corazones

**Referencia**: The Legend of Zelda: A Link to the Past

```
LAYOUT HORIZONTAL:
┌────────────────────────────┐
│ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥      │
└────────────────────────────┘

IMPLEMENTACIÓN:
- Cada corazón: 16×16px
- Espaciado: 2px entre corazones
- Máximo visible: 10 corazones por fila
- Estados: Lleno, Medio (mitad), Vacío

FÓRMULA:
Vida = (Corazones_llenos × 2) + (Corazones_medio × 1)
Ejemplo: 7.5 corazones = 15 puntos de vida
```

**Archivos necesarios**:
```
ui/health/
├── heart_container_empty.png   (16×16, contorno gris)
├── heart_full.png               (16×16, rojo completo)
├── heart_half.png               (16×16, mitad rojo/mitad gris)
└── heart_frame.png              (opcional, marco decorativo)
```

### Estilo Dead Cells - Barra Segmentada

**Referencia**: Dead Cells - Health Bar

```
DISEÑO:
┌──────────────────────────────────┐
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░│
└──────────────────────────────────┘
  ↑12 segmentos llenos  ↑8 vacíos

ESPECIFICACIONES:
- Tamaño total: 160×12px
- 20 segmentos de 8×8px cada uno
- Separación: 1px negro entre segmentos
- Borde exterior: 1px blanco (#f4f4f4)

COLORES POR ESTADO:
- 100%-75%:  #38b764 (verde)
- 74%-40%:   #ffd700 (amarillo)
- 39%-15%:   #ff8800 (naranja)
- 14%-0%:    #cc3333 (rojo parpadeante)
```

**Archivo**: `ui/health/health_bar_segmented.png` (spritesheet con estados)

---

## 4. 🖼️ PANELES Y VENTANAS

### Caja de Diálogo estilo GBA

**Referencia**: The Legend of Zelda: Minish Cap

```
DIMENSIONES: 240×64px (estándar GBA)

┌─────────────────────────────────────┐
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓│
│▓░ Texto del diálogo aquí...    ░▓│
│▓░                               ░▓│
│▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓│
└─────────────────────────────────────┘

COLORES:
- Fondo interior: #1a1c2c (casi negro)
- Borde exterior: #f4f4f4 (blanco)
- Borde interior: #3b5dc9 (azul)
- Sombra: #000000 (2px offset abajo-derecha)

DECORACIÓN:
- Esquinas con pequeños triángulos dorados (4×4px)
- Indicador de "continuar" parpadeante (triángulo)
```

**Archivo**: `ui/panels/dialogue_box.png`

### Panel Translúcido (estilo Hyper Light Drifter)

**Referencia**: Hyper Light Drifter - Inventory/Menu

```
DIMENSIONES: 200×150px (variable)

▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓
▓▒░░░░░░░░░░░░░░░░▒▓
▓▒░               ░▒▓
▓▒░   CONTENIDO   ░▒▓
▓▒░               ░▒▓
▓▒░░░░░░░░░░░░░░░░▒▓
▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

COLORES:
- Fondo: #1a1c2c con alpha 85% (casi opaco)
- Borde grueso: #41a6f6 (azul neón, 2px)
- Borde fino interior: #3b5dc9 (1px)
- Efecto glow exterior: #41a6f6 con blur

CARACTERÍSTICAS:
- Minimalista, geométrico
- Sin decoraciones
- Líneas limpias de 1-2px
```

**Archivo**: `ui/panels/panel_translucent.png`

### Marco Decorado (estilo Shovel Knight)

**Referencia**: Shovel Knight - Character Select Frame

```
DIMENSIONES: 180×220px

    ╔═══════════════╗
    ║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓║
   ◄║▓░░░░░░░░░░░░░▓║►
    ║▓░           ░▓║
    ║▓░ CONTENIDO ░▓║
    ║▓░           ░▓║
   ◄║▓░░░░░░░░░░░░░▓║►
    ║▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓║
    ╚═══════════════╝

ELEMENTOS:
- Marco dorado grueso (4px): #ffd700
- Esquinas redondeadas con decoración
- Pequeñas puntas/flechas laterales (◄►)
- Sombra diagonal pronunciada (4px offset)
- Patrón decorativo en bordes

COLORES:
- Marco: #ffd700, sombra #b8860b
- Fondo: #3b5dc9 degradado a #1a1c2c
- Decoraciones: #f4f4f4
```

**Archivo**: `ui/panels/frame_decorated.png`

### Inventario/Grid (estilo Minish Cap)

**Referencia**: The Legend of Zelda: Minish Cap - Item Screen

```
LAYOUT: Grid 4×3 de items (48×48px cada celda)

┌─────────────────────────────────┐
│ □ □ □ □  EQUIPO  ▼             │
├─────────────────────────────────┤
│ [item] [item] [item] [item]     │
│ [item] [item] [item] [item]     │
│ [item] [item] [item] [item]     │
├─────────────────────────────────┤
│ DESCRIPCIÓN: Llave dorada...    │
└─────────────────────────────────┘

CELDAS:
- Tamaño: 48×48px
- Borde: 2px #c4c4d4
- Seleccionada: borde dorado #ffd700 parpadeante
- Vacía: fondo #5d5d81
- Ocupada: fondo #1a1c2c + icono centrado

COLORES:
- Fondo general: #1a1c2c
- Separadores: #3b5dc9
- Texto: #f4f4f4
```

**Archivo**: `ui/panels/inventory_grid.png` (template 4×3)

---

## 5. 🎮 HUD COMPLETO PARA RUNNER

### Layout Propuesto

```
┌─────────────────────────────────────────────────────┐
│ ❤❤❤❤❤     DISTANCIA: 1250m      🗝️ ×3  ⚙️       │  ← HUD Superior
├─────────────────────────────────────────────────────┤
│                                                      │
│                                                      │
│                     ÁREA DE JUEGO                    │
│                                                      │
│                                            ┌────┐    │  ← Mini-mapa
│                                            │▓▓▓░│    │
│                                            │▓░▓░│    │
└─────────────────────────────────────────────────────┘
```

### Componentes Detallados

#### A) Vida (Arriba Izquierda) - Estilo Zelda
```
Posición: (10, 10)
Tamaño: 170×20px

┌──────────────────────────┐
│ ♥♥♥♥♥                    │
└──────────────────────────┘

- 5 corazones máximo
- Cada corazón: 16×16px
- Espaciado: 2px
- Fondo semi-transparente opcional
```

**Assets**: `ui/hud/hearts_container.png`

#### B) Llaves Recolectadas (Arriba Derecha)
```
Posición: (screenWidth - 120, 10)
Tamaño: 100×24px

┌────────────────┐
│ 🗝️ × 3        │
└────────────────┘

ELEMENTOS:
- Icono llave: 16×16px (dorado)
- Símbolo "×": fuente pixel
- Número: fuente grande, blanco con sombra
- Fondo: panel oscuro 100×24px
```

**Assets**: `ui/hud/key_counter.png` (fondo) + `ui/icons/key_gold.png`

#### C) Distancia/Puntaje (Centro Arriba)
```
Posición: (screenWidth/2 - 100, 10)
Tamaño: 200×32px

┌──────────────────────────┐
│   DISTANCIA: 1250m       │
└──────────────────────────┘

ESTILO Dead Cells:
- Fondo: panel azul oscuro translúcido
- Texto: fuente pixel grande (#f4f4f4)
- Label pequeño: "DISTANCIA"
- Valor grande: "1250m"
- Borde neón azul (#41a6f6)
```

**Assets**: `ui/hud/score_panel.png`

#### D) Mini-mapa (Esquina Inferior Derecha) - Estilo Zelda
```
Posición: (screenWidth - 90, screenHeight - 90)
Tamaño: 80×80px

┌────────────┐
│ ▓▓▓░░░░▓▓ │
│ ▓░░▓▓▓░▓▓ │
│ ▓░░░░░░▓▓ │  ← Laberinto simplificado
│ ▓▓▓▓░▓▓▓▓ │
│    ● ←     │  ← Jugador (punto rojo)
└────────────┘

COLORES:
- Fondo: #1a1c2c con alpha 90%
- Paredes: #5d5d81
- Caminos: #3b5dc9
- Jugador: #cc3333 (punto parpadeante)
- Borde: #f4f4f4 (2px)

CARACTERÍSTICAS:
- Vista cenital simplificada
- Actualización en tiempo real
- Escala: 1 tile del juego = 2px en mapa
```

**Assets**: `ui/hud/minimap_frame.png` + lógica de renderizado

#### E) Botón Pausa (Esquina Superior Derecha)
```
Posición: (screenWidth - 40, 10)
Tamaño: 32×32px

┌──────┐
│ ║ ║ │  ← Icono pausa
└──────┘

- Icono: 16×16px centrado
- Fondo: círculo o cuadrado 32×32px
- Hover: brillo/glow azul
- Color: #c4c4d4 normal, #41a6f6 hover
```

**Assets**: `ui/hud/pause_button.png` + `ui/icons/pause.png`

---

## 6. 🔤 FUENTES PIXEL ART RECOMENDADAS

### Opción 1: Press Start 2P (RECOMENDADA)
```
CARACTERÍSTICAS:
- Estilo: NES/Arcade clásico
- Tamaños: 8px, 16px, 24px
- Licencia: Open Font License (OFL)
- Descarga: fonts.google.com/specimen/Press+Start+2P

USO EN PYGAME:
font = pygame.font.Font('fonts/PressStart2P.ttf', 16)

PERFECTA PARA:
- Títulos de menú
- Puntajes
- Diálogos de juego
```

### Opción 2: 04b03
```
CARACTERÍSTICAS:
- Estilo: Game Boy / GBA
- Tamaño: 8px (muy pequeña y legible)
- Licencia: Freeware
- Descarga: dafont.com/04b03.font

USO EN PYGAME:
font = pygame.font.Font('fonts/04b03.ttf', 8)

PERFECTA PARA:
- Descripciones pequeñas
- Tooltips
- Subtítulos
```

### Opción 3: Pixel Operator
```
CARACTERÍSTICAS:
- Estilo: SNES/Genesis híbrido
- Tamaños: 8px, Mono (monoespaciada)
- Licencia: SIL Open Font License
- Descarga: github.com/PixelOperator

USO EN PYGAME:
font = pygame.font.Font('fonts/PixelOperator.ttf', 8)
font_mono = pygame.font.Font('fonts/PixelOperatorMono.ttf', 8)

PERFECTA PARA:
- Números (usar versión Mono)
- Cronómetros
- Código/Stats
```

### Implementación en Pygame

```python
# Configuración de fuentes
FONTS = {
    'title': pygame.font.Font('assets/fonts/PressStart2P.ttf', 24),
    'menu': pygame.font.Font('assets/fonts/PressStart2P.ttf', 16),
    'dialogue': pygame.font.Font('assets/fonts/04b03.ttf', 8),
    'score': pygame.font.Font('assets/fonts/PixelOperatorMono.ttf', 16),
    'small': pygame.font.Font('assets/fonts/04b03.ttf', 8)
}

# Renderizado con sombra pixel art
def render_text_with_shadow(font, text, color, shadow_color):
    # Sombra (offset 2px diagonal)
    shadow = font.render(text, False, shadow_color)
    # Texto principal
    main_text = font.render(text, False, color)
    
    # Surface combinada
    width = main_text.get_width() + 2
    height = main_text.get_height() + 2
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    surface.blit(shadow, (2, 2))
    surface.blit(main_text, (0, 0))
    
    return surface
```

---

## 7. 📦 ASSETS FINALES Y ESTRUCTURA

### Estructura de Carpetas Recomendada

```
assets/ui/
├── buttons/
│   ├── btn_small_normal.png
│   ├── btn_small_hover.png
│   ├── btn_small_pressed.png
│   ├── btn_medium_normal.png
│   ├── btn_medium_hover.png
│   ├── btn_medium_pressed.png
│   ├── btn_large_normal.png
│   ├── btn_large_hover.png
│   └── btn_large_pressed.png
│
├── icons/
│   ├── heart_full.png          (16×16)
│   ├── heart_half.png          (16×16)
│   ├── heart_empty.png         (16×16)
│   ├── key_gold.png            (16×16)
│   ├── key_silver.png          (16×16)
│   ├── helmet_spartan.png      (32×32)
│   ├── maze_icon.png           (16×16)
│   ├── pause.png               (16×16)
│   ├── settings.png            (16×16)
│   ├── exit.png                (16×16)
│   ├── trophy.png              (32×32)
│   └── coin.png                (16×16)
│
├── health/
│   ├── heart_container_empty.png
│   ├── heart_full_anim.png     (spritesheet 3 frames)
│   ├── health_bar_segmented.png
│   └── health_bar_fill.png
│
├── panels/
│   ├── dialogue_box.png        (240×64)
│   ├── panel_translucent.png   (200×150)
│   ├── frame_decorated.png     (180×220)
│   ├── inventory_grid.png      (template)
│   └── menu_background.png     (fullscreen)
│
├── hud/
│   ├── hearts_container.png
│   ├── key_counter_bg.png
│   ├── score_panel.png
│   ├── minimap_frame.png
│   ├── pause_button.png
│   └── hud_overlay.png         (fullscreen template)
│
└── fonts/
    ├── PressStart2P.ttf
    ├── 04b03.ttf
    ├── PixelOperator.ttf
    └── PixelOperatorMono.ttf
```

### Metadata JSON para UI

```json
{
  "buttons": {
    "small": {
      "width": 64,
      "height": 20,
      "states": ["normal", "hover", "pressed"]
    },
    "medium": {
      "width": 96,
      "height": 32,
      "states": ["normal", "hover", "pressed"]
    },
    "large": {
      "width": 128,
      "height": 40,
      "states": ["normal", "hover", "pressed"]
    }
  },
  "icons": {
    "heart": {
      "size": 16,
      "states": ["full", "half", "empty"],
      "animated": true,
      "frames": 3,
      "frame_duration": 200
    },
    "key": {
      "size": 16,
      "types": ["gold", "silver"]
    }
  },
  "health": {
    "hearts": {
      "type": "discrete",
      "icon_size": 16,
      "max_hearts": 10
    },
    "bar": {
      "type": "continuous",
      "width": 160,
      "height": 12,
      "segments": 20
    }
  },
  "hud": {
    "layout": "runner",
    "components": [
      {"id": "health", "position": [10, 10]},
      {"id": "keys", "position": [-120, 10], "anchor": "topright"},
      {"id": "score", "position": [0, 10], "anchor": "topcenter"},
      {"id": "minimap", "position": [-90, -90], "anchor": "bottomright"},
      {"id": "pause", "position": [-40, 10], "anchor": "topright"}
    ]
  }
}
```

---

## 8. 🎨 HERRAMIENTAS PARA CREAR/EDITAR ASSETS

### Herramientas Recomendadas

#### Aseprite (MEJOR OPCIÓN)
```
DESCRIPCIÓN: Editor pixel art profesional
PRECIO: $19.99 (o compila gratis desde GitHub)
CARACTERÍSTICAS:
- Animación de sprites
- Onion skinning
- Paletas personalizadas
- Exportación a spritesheets
- Soporte para tiles

DESCARGA: aseprite.org
```

#### Piskel (GRATIS, WEB)
```
DESCRIPCIÓN: Editor pixel art online
PRECIO: Gratis
CARACTERÍSTICAS:
- Interfaz web (no instalación)
- Animación básica
- Exporta PNG y GIF
- Paletas limitadas

USO: piskelapp.com
```

#### GraphicsGale (GRATIS)
```
DESCRIPCIÓN: Editor clásico de pixel art
PRECIO: Gratis
CARACTERÍSTICAS:
- Animación avanzada
- Edición frame-por-frame
- Onion skin
- Windows/Wine

DESCARGA: graphicsgale.com
```

### Paletas Pre-hechas

#### Importar en Aseprite/Piskel

**Archivo: `theseus_runner_palette.gpl`** (GIMP Palette)
```
GIMP Palette
Name: Theseus Runner UI
Columns: 4
#
 26  28  44  UI Dark
 93  93 129  UI Gray
196 196 212  UI Light
244 244 244  UI White
255 215   0  UI Gold
184 134  11  UI Gold Dark
 59  93 201  UI Blue
 65 166 246  UI Blue Light
204  51  51  UI Red
139  37  40  UI Red Dark
 56 183 100  UI Green
 37 113 121  UI Green Dark
```

**Para usar**: File → Import Palette → `theseus_runner_palette.gpl`

---

## 9. 📝 CHECKLIST DE IMPLEMENTACIÓN

### Fase 1: Assets Básicos
- [ ] Descargar las 3 fuentes pixel art (Press Start 2P, 04b03, Pixel Operator)
- [ ] Crear paleta de colores en Aseprite/Piskel
- [ ] Diseñar 3 tamaños de botones (9 archivos total)
- [ ] Crear iconos básicos: corazón, llave, pausa (6 archivos)

### Fase 2: Sistema de Vida
- [ ] Diseñar corazones: lleno, medio, vacío (3 archivos)
- [ ] Crear barra de vida segmentada (1 archivo)
- [ ] Implementar animación de corazón (3 frames)

### Fase 3: Paneles
- [ ] Caja de diálogo estilo GBA (1 archivo)
- [ ] Panel translúcido para menús (1 archivo)
- [ ] Marco decorado para selección (1 archivo)
- [ ] Template de inventario grid (1 archivo)

### Fase 4: HUD Completo
- [ ] Contenedor de corazones (1 archivo)
- [ ] Panel contador de llaves (1 archivo)
- [ ] Panel de puntaje/distancia (1 archivo)
- [ ] Marco de mini-mapa (1 archivo)
- [ ] Botón de pausa (1 archivo)

### Fase 5: Integración Pygame
- [ ] Cargar todas las fuentes
- [ ] Crear función de renderizado de texto con sombra
- [ ] Implementar clase Button con estados
- [ ] Implementar clase HealthBar (estilo Zelda)
- [ ] Crear sistema de HUD modular

---

## 10. 🖼️ MOCKUPS Y REFERENCIAS VISUALES

### Mockup de Pantalla de Juego

```
┌────────────────────────────────────────────────────────────┐
│ ❤❤❤♡♡         THESEUS RUNNER        🗝️×3  ⚙️  ║║       │
├────────────────────────────────────────────────────────────┤
│                                                             │
│                                                             │
│                          🏃                                 │
│     ▓▓▓                  │                                 │
│     ▓░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                             │
│     ▓░░░░░░░░░░░░░░░░░░░░░░░▓                             │
│     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     DISTANCIA: 1250m       │
│                                                             │
│                                            ┌──────┐         │
│                                            │▓▓▓░░▓│         │
│                                            │▓░▓░░▓│         │
│                                            │▓░░●░▓│ ← mapa │
│                                            │▓▓▓▓▓▓│         │
└────────────────────────────────────────────────────────────┘
```

### Mockup de Menú Principal

```
┌────────────────────────────────────────────────────────────┐
│                                                             │
│                                                             │
│                  🏛️ THESEUS RUNNER 🐂                      │
│                                                             │
│                                                             │
│              ╔═══════════════════════╗                     │
│              ║   ▶ NUEVA PARTIDA    ║                     │
│              ╚═══════════════════════╝                     │
│                                                             │
│              ╔═══════════════════════╗                     │
│              ║     CONTINUAR         ║                     │
│              ╚═══════════════════════╝                     │
│                                                             │
│              ╔═══════════════════════╗                     │
│              ║    SALÓN DE FAMA     ║                     │
│              ╚═══════════════════════╝                     │
│                                                             │
│              ╔═══════════════════════╗                     │
│              ║     OPCIONES         ║                     │
│              ╚═══════════════════════╝                     │
│                                                             │
│              ╔═══════════════════════╗                     │
│              ║       SALIR          ║                     │
│              ╚═══════════════════════╝                     │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

### Mockup de Game Over

```
┌────────────────────────────────────────────────────────────┐
│                                                             │
│                                                             │
│                     ╔═══════════════╗                      │
│                     ║  GAME OVER   ║                      │
│                     ╚═══════════════╝                      │
│                                                             │
│                         💀 ☠️ 💀                           │
│                                                             │
│                  Has recorrido: 1250m                       │
│                  Llaves obtenidas: 3/10                     │
│                  Tiempo: 05:42                              │
│                                                             │
│              ╔═══════════════════════╗                     │
│              ║  ▶ REINTENTAR        ║                     │
│              ╚═══════════════════════╝                     │
│                                                             │
│              ╔═══════════════════════╗                     │
│              ║    MENÚ PRINCIPAL    ║                     │
│              ╚═══════════════════════╝                     │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

---

## 📚 REFERENCIAS COMPLETAS POR JUEGO

### The Legend of Zelda: Minish Cap (GBA, 2004)
```
ELEMENTOS A REPLICAR:
✓ Sistema de corazones (vida)
✓ Contadores de items con iconos
✓ Caja de diálogo con esquinas decoradas
✓ Mini-mapa en esquina
✓ Paleta de 16 colores vibrante
✓ Botones con bisel sutil

COLORES CLAVE:
- Verde bosque: #38b764
- Azul agua: #3b5dc9
- Dorado: #ffd700
- Rojo vida: #cc3333

ESTUDIAR:
- Item screen (menú de inventario)
- HUD de exploración
- Transiciones de menú
```

### Castlevania: Aria of Sorrow (GBA, 2003)
```
ELEMENTOS A REPLICAR:
✓ Marcos dorados decorativos
✓ Iconos de armas/armor con detalle
✓ Paleta gótica oscura
✓ Barras de HP/MP segmentadas
✓ Fuente serif pixelada

COLORES CLAVE:
- Oro antiguo: #b8860b
- Rojo sangre: #8b2528
- Púrpura: #5d275d
- Gris piedra: #6e6e6e

ESTUDIAR:
- Equipment screen
- Status bars
- Menu decorations
```

### Hyper Light Drifter (2016, estilo 16-bit)
```
ELEMENTOS A REPLICAR:
✓ Paneles translúcidos minimalistas
✓ Iconografía geométrica simple
✓ Paleta cyan/magenta/negro
✓ Glow effects en bordes
✓ UI sin texto (solo iconos)

COLORES CLAVE:
- Cyan neón: #41a6f6
- Magenta: #ff006e
- Negro profundo: #1a1c2c
- Blanco puro: #f4f4f4

ESTUDIAR:
- Map icons
- Health indicators
- Weapon selection UI
```

### Dead Cells (2018, pixel art moderno)
```
ELEMENTOS A REPLICAR:
✓ Barra de vida segmentada horizontal
✓ HUD minimalista esquina superior
✓ Animaciones fluidas en UI
✓ Contadores numéricos grandes
✓ Iconos con outline

COLORES CLAVE:
- Verde tóxico: #38b764
- Naranja: #ff8800
- Azul oscuro: #29366f
- Rojo alerta: #cc3333

ESTUDIAR:
- Top bar HUD
- Item pickup notifications
- Boss health bars
```

### Shovel Knight (2014, estilo NES)
```
ELEMENTOS A REPLICAR:
✓ Botones con sombra diagonal marcada
✓ Marcos con esquinas decorativas
✓ Paleta NES de 64 colores
✓ Fuente retro clásica
✓ Bordes gruesos (2-3px)

COLORES CLAVE:
- Azul caballero: #3b5dc9
- Dorado tesoro: #ffd700
- Verde esmeralda: #38b764
- Gris armadura: #c4c4d4

ESTUDIAR:
- Character select screen
- Main menu layout
- Pause screen
- Item cards
```

---

## 🎯 PRIORIDADES DE IMPLEMENTACIÓN

### Semana 1: Core UI (CRÍTICO)
1. Corazones de vida (sistema Zelda)
2. Botones básicos (normal/hover/pressed)
3. Fuentes pixel art instaladas
4. Panel de diálogo

### Semana 2: HUD de Juego (ALTO)
5. Contador de llaves
6. Panel de distancia/puntaje
7. Botón de pausa
8. Mini-mapa básico

### Semana 3: Menús (MEDIO)
9. Menú principal con botones
10. Pantalla de Game Over
11. Pantalla de Pausa
12. Salón de Fama

### Semana 4: Detalles (BAJO)
13. Animaciones en iconos
14. Transiciones entre pantallas
15. Efectos de hover/glow
16. Sonidos de UI

---

## ✅ CONCLUSIÓN

**NO necesitas generar nada desde cero programáticamente.**

Esta guía te proporciona:
- ✅ Referencias visuales exactas de juegos retro reales
- ✅ Paletas de colores con códigos HEX
- ✅ Dimensiones precisas para cada elemento
- ✅ Estructura de carpetas organizada
- ✅ Fuentes pixel art gratuitas y específicas
- ✅ Mockups de pantallas completas
- ✅ Checklist de implementación paso a paso

**Herramientas a usar**:
- Aseprite (editor pixel art) o Piskel (gratis, web)
- Fuentes: Press Start 2P, 04b03, Pixel Operator
- Referencias: capturas de pantalla de los juegos mencionados

**Siguiente paso**:
1. Abre Aseprite/Piskel
2. Importa la paleta de colores proporcionada
3. Sigue las especificaciones exactas de cada elemento
4. Exporta como PNG con fondo transparente
5. Organiza en la estructura de carpetas recomendada

**Toda la UI será pixel art genuino, basado en estilos probados de juegos clásicos exitosos.** 🎮✨
