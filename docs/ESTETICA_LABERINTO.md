# Estética Retro/Arcade del Laberinto - Theseus Runner

## 🎨 Paleta de Colores General

### Fondo
- **Color base**: `(10, 12, 18)` - Negro azulado profundo

### Elementos del Juego
- **Jugador**: Esfera cyan pulsante `(50, 200-255, 200-255)`
- **Computadora**: Esfera roja pulsante `(200-255, 50, 50)`
- **Obsequios**: Diamante dorado giratorio `(255, 215, 0)`

---

## 🧱 Muros (Paredes)

### Diseño
- **Fondo**: `(20, 25, 40)` - Azul oscuro
- **Patrón**: Cuadrícula 4x4 con variación de brillo
- **Borde neón**: `(0, 200, 255)` - Cyan brillante (2px)
- **Borde interior**: `(0, 120, 180)` - Cyan tenue (1px)

### Características
- Patrón de cuadrícula interior con variación de color
- Efecto de profundidad con doble borde
- Estilo neón/Tron
- Contraste alto para visibilidad

```python
# Cuadrícula interior
for i in range(4):
    for j in range(4):
        color_var = 30 + ((i + j) % 2) * 10
        # Alterna entre tonos oscuros
```

---

## 🛤️ Pasillos (Suelo)

### Diseño
- **Fondo**: `(15, 18, 25)` - Negro azulado
- **Patrón de puntos**: Cuadrícula 8x8 píxeles
- **Color de puntos**: `(0, 40-50, 60-70)` con pulsación
- **Borde**: `(0, 60, 80)` - Cyan muy sutil (1px)

### Características
- Puntos pulsantes que crean efecto de movimiento
- Pulsación basada en posición y tiempo: `sin((frame + x + y) * 0.05)`
- Efecto de "rejilla digital" estilo Tron
- No distrae pero guía visualmente

```python
# Pulsación por posición
pulso = abs(math.sin((frame_count + dx + dy) * 0.05)) * 10
color = (0, 40 + pulso, 60 + pulso)
```

---

## 💎 Obsequios (Coleccionables)

### Diseño
- **Forma**: Diamante rotatorio (4 puntos)
- **Color principal**: `(255, 215, 0)` - Dorado
- **Borde**: `(255, 255, 255)` - Blanco brillante (2px)
- **Aura**: Círculos concéntricos amarillos
- **Centro**: Estrella de 8 puntas giratoria

### Animaciones
1. **Rotación**: Gira continuamente a velocidad constante
2. **Pulsación**: El tamaño varía ±3 píxeles
3. **Aura**: 3 círculos concéntricos difuminados
4. **Estrella central**: 8 líneas desde el centro, rotación inversa

```python
# Rotación del diamante
rotacion = (frame_count * 0.05) % (2 * PI)

# Pulsación de tamaño
pulso = abs(sin(frame_count * 0.1)) * 3
radio = 10 + pulso

# Estrella central (rotación inversa)
estrella_rot = rotacion * 0.5
```

---

## 🎯 Jerarquía Visual

### Prioridad de Atención
1. **Jugador/Computadora** - Esferas pulsantes (más visibles)
2. **Obsequios** - Diamantes giratorios (muy llamativos)
3. **Muros** - Bordes neón (definen espacio)
4. **Pasillos** - Puntos sutiles (fondo navegable)

### Contraste
- **Alto contraste**: Personajes vs fondo
- **Medio contraste**: Muros vs pasillos
- **Animación continua**: Todos los elementos tienen movimiento sutil

---

## 🔧 Valores Técnicos

### Tamaños
- **Celda**: 32x32 píxeles (estándar)
- **Jugador/Computadora**: Radio 20px (aprox 40x40)
- **Obsequios**: Radio 10-13px (con pulsación)
- **Puntos de pasillo**: 1-2px
- **Cuadrícula de muro**: 8x8px

### Velocidades de Animación
- **Esferas**: `sin(frame * 0.2)` y `sin(frame * 0.15)`
- **Obsequios rotación**: `frame * 0.05`
- **Obsequios pulsación**: `sin(frame * 0.1)`
- **Puntos pasillo**: `sin((frame + pos) * 0.05)`
- **Estrella obsequio**: `rotacion * 0.5`

### Bordes
- **Muro exterior**: 2px cyan brillante
- **Muro interior**: 1px cyan tenue
- **Pasillo**: 1px cyan muy sutil
- **Diamante**: 2px blanco brillante
- **Esferas**: 2px blanco

---

## 🎮 Inspiración y Estilo

### Referencias
- **Tron** (1982) - Estética neón y cuadrícula
- **Pac-Man** (1980) - Laberintos con puntos
- **Arcade clásico** - Colores brillantes sobre fondo oscuro
- **Synthwave/Vaporwave** - Paleta cyan/magenta/dorado

### Características del Estilo
- ✨ Todo está en movimiento (pulsaciones, rotaciones)
- 🌟 Efectos de brillo/neón omnipresentes
- 🎨 Paleta limitada pero impactante
- 📐 Geometría simple y clara
- 🔲 Patrones repetitivos (cuadrículas, puntos)

---

## 🧪 Scripts de Prueba

### Visualizar Laberinto Completo
```bash
python test_laberinto_estetica.py
```

### Visualizar Solo Personajes
```bash
python test_esferas_ambas.py
```

---

## 📊 Ventajas de esta Estética

✅ **Alta legibilidad** - Fácil distinguir elementos  
✅ **Feedback visual** - Animaciones indican interactividad  
✅ **Cohesión** - Todos los elementos comparten el estilo  
✅ **Rendimiento** - Todo es procedural, sin texturas pesadas  
✅ **Escalable** - Fácil ajustar tamaños y colores  
✅ **Memorable** - Estilo distintivo y retro  
✅ **Accesible** - Buenos contrastes para visibilidad  

---

## 🎨 Posibles Variaciones

### Para diferentes niveles/temas:
- **Nivel 1**: Cyan/Azul (actual)
- **Nivel 2**: Magenta/Rosa
- **Nivel 3**: Verde/Lima
- **Nivel 4**: Amarillo/Naranja
- **Nivel Final**: Arcoíris/Multicolor

Cambiar solo los valores RGB manteniendo la misma estructura visual.
