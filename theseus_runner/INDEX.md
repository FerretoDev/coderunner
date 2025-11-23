# 📖 Theseus Runner - Índice de Documentación

Bienvenido al sistema de generación programática de assets pixel art para Theseus Runner.

## 🚀 Inicio Rápido

**Para empezar inmediatamente:**

```bash
# Opción 1: Script automático
./quickstart.sh

# Opción 2: Manual
pip install -r requirements.txt
python generate_all.py --scale 2
python demo.py
```

## 📚 Documentación

### Para Usuarios

1. **[README.md](README.md)** - Documentación principal
   - Instalación
   - Uso básico del generador
   - Ejemplos de código Pygame
   - Paleta de colores completa

2. **[FAQ.md](FAQ.md)** - Preguntas Frecuentes
   - Problemas comunes y soluciones
   - Personalización de assets
   - Integración en diferentes motores
   - Tips de rendimiento

3. **[RESUMEN_COMPLETO.md](RESUMEN_COMPLETO.md)** - Estadísticas del Proyecto
   - Lista completa de assets generados
   - Características técnicas
   - Paleta de colores detallada
   - Estructura de carpetas

4. **[EJEMPLOS_INTEGRACION.py](EJEMPLOS_INTEGRACION.py)** - Código de Ejemplo
   - Sprites animados
   - Sistema de parallax
   - Tilemap
   - Partículas
   - UI/Botones
   - Audio manager
   - Mini-juego completo

### Para Desarrolladores

5. **[generate_all.py](generate_all.py)** - Orquestador Principal
   - Ejecuta todos los generadores
   - Parámetros: `--scale`, `--palette`, `--out`
   
6. **[palette.py](palette.py)** - Sistema de Paletas
   - 3 paletas predefinidas (default, night, lava)
   - 16 colores cada una
   - Función `get_palette(name)`

7. **Scripts de Generación** (carpeta `scripts/`)
   - `generate_theseus.py` - Protagonista (32x48, 5 animaciones)
   - `generate_minotaur.py` - Boss (48x48, 5 animaciones)
   - `generate_enemies.py` - Enemigos menores
   - `generate_tileset.py` - Tiles modulares 16x16 y 32x32
   - `generate_backgrounds.py` - Fondos parallax
   - `generate_collectibles.py` - Items coleccionables
   - `generate_particles.py` - Efectos visuales
   - `generate_ui.py` - Interfaz (botones, HUD, iconos)
   - `generate_fonts.py` - Fuente bitmap pixel art
   - `generate_audio.py` - Música y SFX chiptune

8. **[demo.py](demo.py)** - Demostración Interactiva
   - Muestra todos los assets en acción
   - Controles: ESPACIO (cambiar animación), M (Minotauro), C (sonido)

## 🎯 Flujo de Trabajo Recomendado

### Primera Vez

1. Leer [README.md](README.md) secciones "Instalación" y "Uso Básico"
2. Ejecutar `./quickstart.sh` o `python generate_all.py --scale 2`
3. Explorar la carpeta `assets/` generada
4. Ejecutar `python demo.py` para ver los assets

### Integración en tu Juego

1. Estudiar [EJEMPLOS_INTEGRACION.py](EJEMPLOS_INTEGRACION.py)
2. Copiar las clases relevantes (AnimatedSprite, ParallaxBackground, etc.)
3. Adaptar a tu motor/framework
4. Consultar [FAQ.md](FAQ.md) para problemas comunes

### Personalización

1. Decidir qué modificar (personajes, tiles, paleta, etc.)
2. Editar el script correspondiente en `scripts/`
3. Regenerar assets: `python generate_all.py`
4. Probar en la demo o tu juego

### Resolución de Problemas

1. Consultar [FAQ.md](FAQ.md) sección "Problemas Comunes"
2. Verificar logs de generación en terminal
3. Revisar estructura de `assets/` y archivos JSON

## 📊 Estructura del Proyecto

```
theseus_runner/
├── 📄 README.md              # Documentación principal
├── 📄 FAQ.md                 # Preguntas frecuentes
├── 📄 RESUMEN_COMPLETO.md    # Estadísticas y resumen
├── 📄 EJEMPLOS_INTEGRACION.py # Código de ejemplo
├── 📄 INDEX.md               # Este archivo
├── 📄 requirements.txt       # Dependencias Python
├── 🔧 generate_all.py        # Generador principal
├── 🔧 palette.py             # Paletas de colores
├── 🎮 demo.py                # Demo interactiva
├── 🚀 quickstart.sh          # Script de inicio rápido
├── 📁 scripts/               # Generadores individuales (10 archivos)
└── 📁 assets/                # Assets generados (creado al ejecutar)
    ├── sprites/              # Personajes y animaciones
    ├── tiles/                # Tileset del laberinto
    ├── ui/                   # Interfaz y HUD
    ├── fonts/                # Fuente pixel
    ├── backgrounds/          # Fondos parallax
    ├── particles/            # Efectos de partículas
    ├── audio/                # Música y SFX
    └── meta/                 # JSON con metadata
```

## 🎨 Assets Generados por Categoría

| Categoría | Archivos | Descripción |
|-----------|----------|-------------|
| **Personajes** | 3 spritesheets | Theseus, Minotauro, enemigos |
| **Mundo** | 2 tilesets + 3 fondos | Tiles 16x16/32x32, parallax |
| **Coleccionables** | 1 spritesheet | Llaves, gemas, monedas, vida |
| **Efectos** | 1 spritesheet | Polvo, chispas, sangre, brillo |
| **UI** | 3 imágenes | Botones, HUD, iconos |
| **Fuentes** | 2 fuentes | 8px y 16px bitmap |
| **Audio** | 6 archivos WAV | 5 SFX + 1 música de fondo |
| **Metadata** | 11 archivos JSON | Coordenadas y configuración |

**Total: 32 archivos (~324 KB con escala x2)**

## 🛠️ Herramientas y Comandos Útiles

```bash
# Generar con diferentes configuraciones
python generate_all.py --scale 1     # Sprites pequeños
python generate_all.py --scale 2     # Tamaño estándar
python generate_all.py --scale 4     # Sprites grandes (HD)

# Paletas alternativas
python generate_all.py --palette night    # Tema nocturno
python generate_all.py --palette lava     # Tema fuego/lava

# Directorios personalizados
python generate_all.py --out production/  # Para build final
python generate_all.py --out test/        # Para pruebas

# Generar solo un tipo de asset
python scripts/generate_theseus.py --scale 2
python scripts/generate_tileset.py
python scripts/generate_audio.py

# Ejecutar demo
python demo.py
```

## 📖 Guías por Tarea

### "Quiero empezar ahora mismo"
→ `./quickstart.sh` → Listo

### "Quiero entender cómo funciona"
→ [README.md](README.md) → [generate_all.py](generate_all.py) → `scripts/generate_theseus.py`

### "Quiero integrar en mi juego"
→ [EJEMPLOS_INTEGRACION.py](EJEMPLOS_INTEGRACION.py) → [FAQ.md](FAQ.md) sección "Integración"

### "Quiero personalizar los personajes"
→ [FAQ.md](FAQ.md) sección "Personalización" → Editar `scripts/generate_X.py` → Regenerar

### "Quiero cambiar los colores"
→ [palette.py](palette.py) → Añadir nueva paleta → Usar `--palette mi_paleta`

### "Tengo un problema/error"
→ [FAQ.md](FAQ.md) sección "Problemas Comunes" → Logs del terminal → Verificar instalación

### "Quiero ver estadísticas completas"
→ [RESUMEN_COMPLETO.md](RESUMEN_COMPLETO.md)

## 🎓 Recursos de Aprendizaje

### Para Pixel Art Programático
- Estudia `scripts/generate_theseus.py` (más completo)
- Revisa funciones `draw_pixel_rect()` y `draw_theseus_X()`
- Experimenta cambiando coordenadas y colores

### Para Integración con Pygame
- Lee clase `AnimatedSprite` en [EJEMPLOS_INTEGRACION.py](EJEMPLOS_INTEGRACION.py)
- Ejecuta `demo.py` y lee su código fuente
- Prueba modificar la demo

### Para Generación Procedural
- Examina `generate_backgrounds.py` (uso de random seed)
- Mira `generate_particles.py` (variaciones aleatorias)
- Estudia `generate_audio.py` (síntesis de ondas)

## 🔗 Enlaces Rápidos

- **Instalación**: [README.md#instalación](README.md)
- **Uso Básico**: [README.md#uso-básico](README.md)
- **Paleta de Colores**: [README.md#paleta-de-colores](README.md)
- **Integración Pygame**: [EJEMPLOS_INTEGRACION.py](EJEMPLOS_INTEGRACION.py)
- **Problemas Comunes**: [FAQ.md#problemas-comunes](FAQ.md)
- **Personalización**: [FAQ.md#personalización](FAQ.md)
- **Estadísticas Completas**: [RESUMEN_COMPLETO.md](RESUMEN_COMPLETO.md)

## ✅ Checklist de Inicio

- [ ] Python 3.10+ instalado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Assets generados (`python generate_all.py --scale 2`)
- [ ] Demo ejecutada exitosamente (`python demo.py`)
- [ ] Leído README.md completo
- [ ] Explorada carpeta `assets/`
- [ ] Probado código de EJEMPLOS_INTEGRACION.py
- [ ] Consultado FAQ.md para dudas

## 🎉 ¡Listo para Crear!

Ahora tienes todo lo necesario para:
- ✅ Generar assets pixel art profesionales
- ✅ Integrarlos en tu juego
- ✅ Personalizarlos a tu gusto
- ✅ Resolver problemas comunes
- ✅ Extender el sistema con nuevos assets

**¡Disfruta creando tu juego de Theseus Runner!** 🏃‍♂️🏺🐂

---

*Última actualización: Noviembre 2025*
*Versión del sistema: 1.0.0*
