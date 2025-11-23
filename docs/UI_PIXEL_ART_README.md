# Sistema UI Pixel Art - CodeRunner

Sistema completo de interfaz de usuario estilo pixel art inspirado en juegos retro clásicos.

## 🎨 Características

- **Paleta de 16 colores** inspirada en juegos GBA/SNES
- **Componentes modulares** reutilizables
- **Estilo pixel art** con referencias a juegos clásicos
- **Sistema de temas** (GBA, translúcido, decorado, simple)

## 📦 Componentes Disponibles

### 1. PaletaUI (`interfaz/paleta_ui.py`)

Paleta de colores centralizada con 16 colores base:

```python
from interfaz.paleta_ui import PaletaUI

# Colores principales
color_fondo = PaletaUI.DARK
color_texto = PaletaUI.LIGHT
color_acento = PaletaUI.GOLD

# Color dinámico según vida
color_vida = PaletaUI.obtener_color_vida(75)  # Verde si >50%
```

**Colores disponibles:**
- UI_DARK, UI_GRAY, UI_LIGHT, UI_WHITE
- UI_GOLD, UI_GOLD_DARK
- UI_BLUE, UI_BLUE_LIGHT
- UI_RED, UI_RED_DARK
- UI_GREEN, UI_GREEN_DARK

### 2. Boton (`interfaz/componentes/boton.py`)

Botón pixel art con 4 estados y sombra diagonal:

```python
from interfaz.componentes import Boton

# Crear botón
boton = Boton(
    x=100, y=100,
    ancho=160, alto=40,
    texto="INICIAR",
    accion=lambda: print("Click!")
)

# En loop de eventos
boton.manejar_evento(evento)
boton.actualizar(pos_mouse)
boton.dibujar(surface)
```

**Estados:**
- Normal (azul)
- Hover (dorado al pasar mouse)
- Pressed (dorado oscuro al click)
- Disabled (gris)

**Características:**
- Borde de 2px
- Sombra diagonal 2px offset
- Texto con sombra
- Callback opcional

### 3. Panel (`interfaz/componentes/panel.py`)

Paneles decorativos con 4 estilos diferentes:

```python
from interfaz.componentes import Panel

# Panel estilo Zelda Minish Cap
panel_gba = Panel(x=50, y=50, ancho=200, alto=100, tipo="gba")

# Panel translúcido estilo Hyper Light Drifter
panel_trans = Panel(x=50, y=50, ancho=200, alto=100, 
                   tipo="translucido", alpha=200)

# Panel decorado estilo Shovel Knight
panel_deco = Panel(x=50, y=50, ancho=200, alto=100, tipo="decorado")

# Panel simple
panel_simple = Panel(x=50, y=50, ancho=200, alto=100, tipo="simple")

panel.dibujar(surface)
```

**Estilos:**
- `gba`: Bordes dobles, esquinas decoradas (Zelda Minish Cap)
- `translucido`: Fondo semi-transparente, borde neón (Hyper Light Drifter)
- `decorado`: Esquinas con triángulos grandes (Shovel Knight)
- `simple`: Borde sencillo, fondo sólido

### 4. BarraVida (`interfaz/componentes/barra_vida.py`)

Indicador de salud con 2 estilos:

```python
from interfaz.componentes import BarraVida

# Estilo corazones (Zelda)
vida_corazones = BarraVida(x=10, y=10, max_vida=10, estilo="corazones")
vida_corazones.actualizar(7)  # 3.5 corazones llenos

# Estilo barra segmentada (Dead Cells)
vida_barra = BarraVida(x=10, y=10, max_vida=100, estilo="segmentada")
vida_barra.actualizar(75)  # 75% verde

vida.dibujar(surface)
```

**Estilos:**
- `corazones`: Corazones pixelados 16×16px (Zelda)
  - Estados: lleno, medio, vacío
  - Máximo 10 corazones
  - Cada corazón = 2 HP
  
- `segmentada`: Barra con segmentos (Dead Cells)
  - 20 segmentos de 8px
  - Color cambia según porcentaje:
    - Verde: >50%
    - Dorado: 25-50%
    - Rojo: <25%

### 5. HUD (`interfaz/componentes/hud.py`)

Sistema completo de interfaz en juego:

```python
from interfaz.componentes import HUD

# Crear HUD
hud = HUD(screen_width=800, screen_height=600)

# Actualizar cada frame
hud.actualizar(
    vida=85,
    llaves=3,
    puntaje=1250,
    tiempo=120
)

# Dibujar
hud.dibujar(surface)
```

**Elementos incluidos:**
- Barra de vida (top-left)
- Contador de llaves con ícono (top-right)
- Panel de puntaje/distancia (top-center)
- Espacio para minimapa (bottom-right)

## 🎮 Referencias de Juegos

El diseño está inspirado en:

| Juego | Elemento | Aplicación |
|-------|----------|------------|
| **Zelda: Minish Cap** | Diálogos GBA | Paneles con doble borde |
| **Castlevania: AoS** | Iconos de items | Diseño de íconos 16×16 |
| **Shovel Knight** | Bordes y sombras | Sombras diagonales en botones |
| **Hyper Light Drifter** | Paneles translúcidos | Paneles con alpha y neón |
| **Dead Cells** | Barra de vida | Segmentos con cambio de color |

## 📖 Uso Básico

### Pantalla de Demostración

Ejecuta la demo completa para ver todos los componentes:

```bash
python test_demo_ui.py
```

**Controles de la demo:**
- `↑↓`: Cambiar vida
- `←→`: Cambiar llaves
- `Click`: Interactuar con botones
- `ESC`: Salir

### Integración en Pantalla Nueva

```python
import pygame
from interfaz.pantallas.pantalla_base import PantallaBase
from interfaz.paleta_ui import PaletaUI
from interfaz.componentes import Boton, Panel, BarraVida

class MiPantalla(PantallaBase):
    def __init__(self, screen):
        super().__init__(screen)
        
        # Crear componentes
        self.panel_fondo = Panel(50, 50, 300, 200, tipo="gba")
        self.boton_jugar = Boton(100, 100, 200, 50, "JUGAR", 
                                 accion=self.iniciar_juego)
        self.vida = BarraVida(10, 10, max_vida=100, estilo="segmentada")
        
    def manejar_eventos(self, eventos):
        for evento in eventos:
            self.boton_jugar.manejar_evento(evento)
    
    def actualizar(self):
        pos_mouse = pygame.mouse.get_pos()
        self.boton_jugar.actualizar(pos_mouse)
    
    def dibujar(self):
        self.screen.fill(PaletaUI.DARK)
        self.panel_fondo.dibujar(self.screen)
        self.boton_jugar.dibujar(self.screen)
        self.vida.dibujar(self.screen)
```

### Desde el Menú Principal

El juego ahora incluye una opción "Demo UI" en el menú principal:

1. Ejecuta el juego: `python src/main.py`
2. Selecciona "Demo UI"
3. Interactúa con todos los componentes

## 🎨 Paleta de Colores

La paleta completa en formato HEX:

```
DARK:       #1a1a2e (Fondo principal)
GRAY:       #16213e (Fondo secundario)
LIGHT:      #e8e8e8 (Texto principal)
WHITE:      #ffffff (Texto destacado)

GOLD:       #f4a261 (Acento principal)
GOLD_DARK:  #d08c47 (Acento presionado)

BLUE:       #4a90e2 (UI principal)
BLUE_LIGHT: #64b5f6 (UI hover)

RED:        #e63946 (Peligro/bajo)
RED_DARK:   #c5303a (Peligro oscuro)

GREEN:      #06d6a0 (Éxito/alto)
GREEN_DARK: #05b587 (Éxito oscuro)
```

## 📁 Estructura de Archivos

```
src/interfaz/
├── paleta_ui.py              # Sistema de colores
├── gestor_fuentes.py         # Gestión de fuentes
├── componentes/
│   ├── __init__.py           # Exports (nuevo + legacy)
│   ├── boton.py             # Botón pixel art
│   ├── panel.py             # Paneles decorativos
│   ├── barra_vida.py        # Indicadores de salud
│   ├── hud.py               # HUD completo
│   ├── input_texto.py       # (Legacy) BotonLegacy
│   └── overlay.py           # (Legacy) PanelLegacy
└── pantallas/
    ├── __init__.py
    ├── pantalla_demo_ui.py  # Demo interactiva
    └── ...
```

## 🔧 Compatibilidad

El sistema mantiene compatibilidad con código existente:

```python
# Nuevo sistema (recomendado)
from interfaz.componentes import Boton, Panel

# Sistema legacy (todavía funciona)
from interfaz.componentes import BotonLegacy, PanelLegacy
```

## 📝 Notas de Diseño

- **No antialiasing**: Todos los componentes usan píxeles nítidos
- **Sombras discretas**: 2px offset diagonal (estilo Shovel Knight)
- **Bordes consistentes**: 2px para todos los elementos principales
- **Espaciado**: Múltiplos de 4px para grid consistency
- **Tamaños de íconos**: 16×16px estándar (GBA/SNES)

## 🚀 Próximos Pasos

Para integrar completamente en el juego:

1. **Actualizar MenuPrincipal**: Usar nuevos botones
2. **Actualizar PantallaJuego**: Usar nuevo HUD
3. **Crear íconos sprite**: Reemplazar dibujo programático
4. **Añadir animaciones**: Transiciones suaves entre estados
5. **Sonidos UI**: Feedback auditivo para interacciones

## 📚 Documentación Adicional

- [UI_DESIGN_GUIDE.md](../docs/UI_DESIGN_GUIDE.md) - Guía completa de diseño (700+ líneas)
- Incluye mockups, especificaciones exactas y referencias visuales

---

**Versión:** 1.0  
**Fecha:** 2024  
**Licencia:** Igual que CodeRunner
