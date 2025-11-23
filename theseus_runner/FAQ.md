# FAQ - Theseus Runner Asset Generator

## Preguntas Frecuentes

### 📋 General

**P: ¿Qué es Theseus Runner?**
R: Es un sistema de generación programática de assets pixel art para un juego de runner basado en la mitología del Minotauro. Genera todos los recursos visuales y de audio necesarios para crear un juego completo.

**P: ¿Necesito experiencia en diseño gráfico?**
R: No. Todo se genera mediante código Python. No necesitas dibujar ni editar imágenes manualmente.

**P: ¿Puedo usar estos assets en mi juego comercial?**
R: Los assets generados son completamente tuyos. Puedes usarlos en proyectos personales o comerciales.

### 🔧 Instalación y Configuración

**P: ¿Qué necesito para ejecutar el generador?**
R: Python 3.10 o superior y las dependencias listadas en `requirements.txt`:
```bash
pip install -r requirements.txt
```

**P: ¿Funciona en Windows/Mac/Linux?**
R: Sí, es multiplataforma. Python y las bibliotecas usadas funcionan en todos los sistemas operativos.

**P: ¿Cuánto espacio ocupan los assets generados?**
R: Aproximadamente 324KB con escala x2. El tamaño varía según la escala elegida.

### 🎨 Generación de Assets

**P: ¿Cómo genero los assets?**
R: Ejecuta:
```bash
python generate_all.py --scale 2
```

**P: ¿Qué significa el parámetro `--scale`?**
R: Multiplica el tamaño de los sprites. `--scale 1` genera sprites pequeños (32x48 para Theseus), `--scale 2` los duplica (64x96), etc. Útil para diferentes resoluciones.

**P: ¿Puedo cambiar los colores?**
R: Sí, usa el parámetro `--palette`:
```bash
python generate_all.py --palette night    # Paleta oscura/nocturna
python generate_all.py --palette lava     # Paleta roja/naranja
python generate_all.py --palette default  # Paleta estándar
```

**P: ¿Cómo agrego mi propia paleta?**
R: Edita `palette.py` y añade un nuevo diccionario:
```python
PALETTE_MI_TEMA = {
    'NEGRO': (0, 0, 0),
    'BLANCO': (255, 255, 255),
    # ... resto de colores
}
```

**P: ¿Cuánto tiempo tarda la generación?**
R: Menos de 5 segundos en hardware moderno. Los assets de audio pueden tardar un poco más.

**P: ¿Puedo generar solo un tipo de asset?**
R: Sí, ejecuta directamente el script correspondiente:
```bash
python scripts/generate_theseus.py --scale 2
python scripts/generate_tileset.py --palette night
```

### 🎮 Integración en Juegos

**P: ¿Cómo uso los assets en Pygame?**
R: Revisa `EJEMPLOS_INTEGRACION.py` para código de ejemplo completo. Básicamente:
```python
sprite = AnimatedSprite('assets/sprites/theseus_spritesheet.png',
                        'assets/meta/theseus.json')
sprite.set_animation('run')
```

**P: ¿Funcionan en otros motores (Unity, Godot, etc.)?**
R: Sí. Los PNG y WAV son formatos estándar. Los archivos JSON contienen las coordenadas de frames para usar en cualquier motor.

**P: ¿Cómo cargo las animaciones en Unity?**
R: Importa el spritesheet PNG, y usa el JSON para configurar el Sprite Editor con las coordenadas de cada frame.

**P: ¿Qué información contienen los archivos JSON?**
R: Coordenadas (x, y, width, height) de cada frame, duración en milisegundos, si la animación hace loop, etc.

### 🎵 Audio

**P: ¿Por qué el audio suena "simple" o "retro"?**
R: Es intencional. El audio se genera usando ondas cuadradas (chiptune/8-bit) para mantener la estética pixel art retro.

**P: ¿Puedo reemplazar el audio generado con archivos propios?**
R: Sí, solo reemplaza los archivos WAV en `assets/audio/`. Mantén los mismos nombres para que el código funcione.

**P: ¿Puedo ajustar la música generada?**
R: Edita `scripts/generate_audio.py` y modifica la lista `melody` en `generate_bgm_loop()` con nuevas frecuencias/duraciones.

### 🖼️ Personalización

**P: ¿Puedo modificar el tamaño de Theseus?**
R: Sí, edita `generate_theseus.py` y cambia:
```python
sprite_w, sprite_h = 32, 48  # Cambia estos valores
```

**P: ¿Cómo añado más animaciones a un personaje?**
R: 1) Edita el script del personaje (ej. `generate_theseus.py`)
2) Crea una función `draw_theseus_nueva_animacion()`
3) Añádela al diccionario `animations`
4) Regenera los assets

**P: ¿Puedo añadir más enemigos?**
R: Sí, edita `scripts/generate_enemies.py` y añade nuevas funciones de dibujo. Sigue el patrón de `draw_rat_run()` y `draw_statue_idle()`.

**P: ¿Cómo creo más tiles para el tileset?**
R: Edita `scripts/generate_tileset.py` y añade nuevas funciones `draw_tile_X()`. Agrégalas a la lista `tile_types`.

### 🐛 Problemas Comunes

**P: Obtengo error "ModuleNotFoundError: No module named 'PIL'"**
R: Instala las dependencias:
```bash
pip install -r requirements.txt
```

**P: La demo no se ejecuta / pantalla negra**
R: Asegúrate de generar los assets primero:
```bash
python generate_all.py --scale 2
python demo.py
```

**P: Los sprites se ven borrosos/pixelados incorrectamente**
R: Asegúrate de usar `Image.NEAREST` al escalar:
```python
img = img.resize((new_w, new_h), Image.NEAREST)
```

**P: El audio no se reproduce en la demo**
R: Verifica que `pygame.mixer` esté inicializado y que los archivos WAV existan en `assets/audio/`.

**P: Error "No newline at end of file" en los scripts**
R: Es un warning de estilo (lint). No afecta la funcionalidad. Puedes ignorarlo o agregar una línea en blanco al final del archivo.

### 📦 Distribución

**P: ¿Cómo distribuyo mi juego con estos assets?**
R: Incluye la carpeta `assets/` completa con tu juego. No necesitas incluir los scripts de generación.

**P: ¿Puedo regenerar los assets con diferentes configuraciones para distintas plataformas?**
R: Sí. Por ejemplo:
```bash
# Móvil (escala pequeña)
python generate_all.py --scale 1 --out assets_mobile/

# PC/Consola (escala grande)
python generate_all.py --scale 4 --out assets_pc/
```

### 🚀 Rendimiento

**P: ¿Los assets generados afectan el rendimiento del juego?**
R: No más que cualquier asset dibujado a mano. El tamaño es pequeño (PNG comprimidos eficientemente).

**P: ¿Debo regenerar en cada ejecución del juego?**
R: No. Genera una vez, guarda los assets, y cárgalos normalmente en tu juego.

### 📚 Aprendizaje

**P: ¿Cómo aprendo a modificar los generadores?**
R: 1) Empieza leyendo `generate_theseus.py` para entender el patrón
2) Modifica valores (colores, tamaños) y regenera para ver cambios
3) Revisa `EJEMPLOS_INTEGRACION.py` para uso en juegos

**P: ¿Dónde aprendo sobre generación procedural de arte?**
R: Conceptos clave:
- Pixel art programático: dibujar rectángulos/puntos individuales
- Spritesheets: organizar frames en una imagen
- Animación por frames: cambiar imágenes a intervalos
- Síntesis de audio: generar ondas con matemáticas

### 💡 Extensiones

**P: ¿Puedo añadir más efectos visuales?**
R: Sí. Crea nuevos tipos en `generate_particles.py` o añade post-procesamiento en los shaders del motor.

**P: ¿Puedo generar assets 3D?**
R: Este proyecto es específico para 2D pixel art. Para 3D necesitarías bibliotecas como `trimesh` o `pyrender`.

**P: ¿Hay plan para añadir más personajes/enemigos?**
R: El sistema está diseñado para ser extensible. Puedes crear nuevos generadores siguiendo el patrón existente.

---

## 🆘 Soporte

**¿No encuentras tu pregunta aquí?**

1. Revisa `README.md` para documentación completa
2. Lee `EJEMPLOS_INTEGRACION.py` para código de ejemplo
3. Examina `RESUMEN_COMPLETO.md` para estadísticas del proyecto
4. Inspecciona los scripts en `scripts/` para entender la generación

**Contribuciones:**
Si mejoras el sistema, considera compartir tus modificaciones con la comunidad.
