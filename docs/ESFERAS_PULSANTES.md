# Efectos de Esferas Pulsantes - Jugador vs Computadora

## 🎨 Esquema de Colores

### 🔵 Jugador (Azul/Cyan)
- **Color principal**: `(50, intensidad, intensidad)` - Cyan
- **Centro brillante**: `(150, 255, 255)` - Cyan brillante (efecto de "energía")
- **Borde**: Blanco
- **Ojos/Núcleo**: Blanco

### 🔴 Computadora (Rojo)
- **Color principal**: `(intensidad, 50, 50)` - Rojo
- **Centro oscuro**: `(180, 30, 30)` - Rojo oscuro (efecto de "profundidad")
- **Borde**: Blanco
- **Ojos**: Blanco

## ⚡ Características Compartidas

- **Pulsación**: ±3 píxeles usando `abs(sin(frame_count * 0.2))`
- **Variación de intensidad**: 200-255 usando `abs(sin(frame_count * 0.15))`
- **Animación sincronizada**: Mismo patrón de movimiento
- **FPS**: 60 frames por segundo

## 🎮 Diferencias Visuales

| Característica | Jugador | Computadora |
|----------------|---------|-------------|
| Color base | Cyan/Azul | Rojo |
| Centro | Brillante (energía) | Oscuro (profundidad) |
| Sensación | Amigable, heroico | Amenazante, peligroso |
| RGB | `(50, 200-255, 200-255)` | `(200-255, 50, 50)` |

## 🧪 Scripts de Prueba

### Probar Jugador y Computadora juntos
```bash
cd /home/marcus/Dev/coderunner
python test_esferas_ambas.py
```

### Probar solo Computadora
```bash
python test_esfera_pulsante.py
```

## 📝 Notas de Implementación

- Ambos usan el mismo algoritmo de animación
- Los colores fueron elegidos para contrastar visualmente
- El jugador tiene un centro brillante para parecer "bueno"
- La computadora tiene un centro oscuro para parecer "amenazante"
- Los efectos son completamente procedurales (sin imágenes)
- Rendimiento optimizado usando funciones matemáticas simples

## 🎯 Compatibilidad

- ✅ Compatible con el algoritmo BFS de la computadora
- ✅ Compatible con el sistema de movimiento del jugador
- ✅ Compatible con el sistema de colisiones
- ✅ Sin dependencia de archivos PNG/sprites externos
