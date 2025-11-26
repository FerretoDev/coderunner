# 🏛️ Estética Mitológica Griega - Laberinto de Teseo

## 📖 Concepto

La interfaz del laberinto ha sido rediseñada para reflejar el **Mito de Teseo y el Minotauro**, con una estética inspirada en la Grecia antigua, mosaicos greco-romanos y arquitectura clásica.

## 🎨 Paleta de Colores

### Inspiración Mitológica
- **Mármol Griego**: Tonos beige/crema (210, 195, 170)
- **Terracota**: Arcilla rojiza (156, 102, 68)
- **Bronce Antiguo**: Metal oxidado (184, 115, 51)
- **Oro Mítico**: Dorado resplandeciente (218, 165, 32)
- **Pergamino**: Fondo claro (240, 230, 210)

## 🏺 Elementos Visuales

### 1. Muros - Piedra Antigua / Mármol Griego

**Concepto**: Bloques de mármol y piedra caliza como los templos griegos

**Implementación**:
```python
# Base de mármol beige
color_base = (210, 195, 170)

# Textura de bloques de piedra (3x3)
# - Vetas de mármol: Variación de color ±7 tonos
# - Líneas de mortero entre bloques
# - Sombras para profundidad
```

**Características**:
- ✅ Textura de bloques individuales (3x3 por celda)
- ✅ Vetas de mármol (variación procedural de color)
- ✅ Líneas de mortero entre bloques (color más oscuro)
- ✅ Borde de bronce oxidado (metal antiguo)
- ✅ Sombras interiores para efecto 3D

**Efecto visual**: Paredes de templo griego con bloques de mármol tallado

### 2. Pasillos - Mosaico Greco-Romano

**Concepto**: Suelo de mosaico terracota como las villas romanas

**Implementación**:
```python
# Base terracota
base_terracota = (156, 102, 68)

# Patrón de baldosas 4x4
# - 3 tonos: Crema, beige, terracota
# - Patrón pseudo-aleatorio basado en posición
# - Símbolos griegos ocasionales
```

**Características**:
- ✅ Baldosas pequeñas 4x4 (tessellae)
- ✅ Tres tonos de mosaico alternados
- ✅ Símbolos decorativos griegos cada 7 celdas
- ✅ Borde de separación entre baldosas
- ✅ Patrón único por posición (pseudo-aleatorio)

**Efecto visual**: Suelo de mosaico antiguo con patina del tiempo

### 3. Obsequios - Hilo de Ariadna

**Concepto**: Ovillo de hilo dorado que Ariadna dio a Teseo para escapar del laberinto

**Implementación**:
```python
# Ovillo pulsante
radio_base = 9
pulso_tamano = abs(sin(frame * 0.06)) * 2

# Aura dorada resplandeciente
# - 5 círculos concéntricos
# - Pulsación de brillo (sin(frame * 0.08))

# Líneas de hilo enrollado
# - 8 líneas rotatorias
# - Simulan textura del hilo
```

**Características**:
- ✅ Ovillo circular dorado (oro antiguo)
- ✅ Pulsación suave de tamaño y brillo
- ✅ Aura resplandeciente (5 capas concéntricas)
- ✅ Líneas de hilo enrollado (rotación lenta)
- ✅ Destello central brillante
- ✅ Borde dorado pulsante

**Efecto visual**: Hilo mágico resplandeciente de la mitología griega

## 🎭 Cambios vs. Estética Anterior

### Antes: Estilo Retro/Arcade Neón
```
Muros: Fondo oscuro + grid neón cyan
Pasillos: Negro con puntos pulsantes azules
Obsequios: Diamante giratorio amarillo
Paleta: Neón, cyan, negro, brillos
```

### Después: Estilo Mitológico Griego
```
Muros: Mármol beige + textura de bloques + bronce
Pasillos: Terracota + mosaico + símbolos griegos
Obsequios: Ovillo dorado + aura resplandeciente
Paleta: Terracota, mármol, bronce, oro
```

## 📐 Detalles Técnicos

### Texturas Procedurales

**Muros - Vetas de Mármol**:
```python
veta = ((i * 7 + j * 5 + fila * 3 + col * 2) % 15) - 7
color_piedra = (210 + veta, 195 + veta, 170 + veta)
```
- Rango: ±7 tonos
- Base: RGB(210, 195, 170)
- Resultado: Variación natural de mármol

**Pasillos - Patrón de Mosaico**:
```python
patron = (tx + ty + fila + col) % 3

if patron == 0:   # Crema oscuro
    (198, 156, 109)
elif patron == 1: # Beige
    (176, 141, 105)
else:            # Terracota claro
    (166, 123, 91)
```

### Animaciones

**Hilo de Ariadna**:
```python
# Pulsación de brillo
pulso_brillo = abs(sin(frame * 0.08)) * 0.3 + 0.7
# Rango: 0.7 a 1.0 (70% a 100% brillo)

# Pulsación de tamaño
pulso_tamano = abs(sin(frame * 0.06)) * 2
# Rango: ±2 píxeles

# Rotación de líneas
angulo = (frame * 0.03 + offset) % (2π)
# Velocidad: 0.03 radianes/frame
```

## 🎮 Inmersión Temática

### Narrativa Visual
El jugador (Teseo) navega por un laberinto de mármol griego, recogiendo el **Hilo de Ariadna** para encontrar su camino, mientras es perseguido por el Minotauro (computadora).

### Elementos Coherentes
- ✅ Arquitectura griega antigua
- ✅ Materiales auténticos (mármol, terracota, bronce, oro)
- ✅ Simbología mitológica (Hilo de Ariadna)
- ✅ Paleta de colores históricamente precisa
- ✅ Texturas que evocan antigüedad

## 🧪 Testing

### Script de Prueba
```bash
python test_estetica_griega.py
```

**Verificar**:
- Muros muestran textura de bloques de mármol
- Pasillos tienen patrón de mosaico terracota
- Hilo de Ariadna pulsa con brillo dorado
- Paleta general es cálida (beige/terracota/oro)
- No hay elementos neón o futuristas

## 📊 Comparación de Efectos

| Elemento | Estilo Neón | Estilo Griego |
|----------|-------------|---------------|
| **Muros** | Grid cyan brillante | Bloques de mármol |
| **Suelo** | Puntos azules | Mosaico terracota |
| **Items** | Diamante giratorio | Ovillo de hilo |
| **Borde** | Neón cyan (0,200,255) | Bronce (184,115,51) |
| **Fondo** | Negro (15,18,25) | Terracota (156,102,68) |
| **Atmósfera** | Futurista/Tron | Antigüedad/Mítica |

## 🎨 Referencias Visuales

### Inspiración Histórica
- **Mosaicos**: Villa romana del Casale, Sicilia
- **Arquitectura**: Partenón, Templo de Zeus
- **Materiales**: Mármol pentélico, terracota ática
- **Mito**: Historia de Teseo y el Minotauro (Ovidio, Plutarco)

### Símbolos Griegos Potenciales
- Meandro griego (greca)
- Cruz griega
- Espiral cretense
- Labrys (hacha doble minoica)

## 🔮 Mejoras Futuras

### Posibles Adiciones
1. **Columnas**: Pilares dóricos en esquinas
2. **Frescos**: Figuras negras en algunos muros
3. **Antorchas**: Luz parpadeante en pasillos
4. **Grietas**: Daño por antigüedad en piedras
5. **Inscripciones**: Letras griegas en muros
6. **Sombras**: Proyección de luz de antorchas

### Animaciones Adicionales
- Polvo cayendo de muros antiguos
- Llamas de antorchas oscilantes
- Brillo místico del hilo aumenta al acercarse

## 📚 Archivos Modificados

| Archivo | Cambios |
|---------|---------|
| `pantalla_juego.py` | `_dibujar_laberinto()` - Muros y pasillos |
| `laberinto.py` | `dibujar_obsequios()` - Hilo de Ariadna |
| `test_estetica_griega.py` | Script de visualización |

## 🎯 Resultado Final

La interfaz del laberinto ahora refleja completamente el **Mito de Teseo**, con:
- Arquitectura de templo griego (mármol y bronce)
- Suelo de mosaico antiguo (terracota)
- Hilo de Ariadna resplandeciente (oro místico)
- Atmósfera de antigüedad y mitología

**Sensación**: El jugador está dentro del legendario Laberinto de Creta, siguiendo el hilo dorado de Ariadna mientras escapa del Minotauro.

---

**Fecha**: Noviembre 2025  
**Tema**: Mitología Griega - Teseo y el Minotauro  
**Estilo**: Arquitectura clásica + Mosaico romano + Elementos míticos
