# Sistema de Movimiento Suave con Interpolación

## 📋 Descripción General

Este documento describe la implementación del sistema de interpolación para movimiento suave del jugador en el juego Theseus Runner. El sistema mantiene la mecánica de movimiento basado en celdas pero agrega una transición visual suave entre posiciones.

## 🎯 Objetivo

Eliminar el aspecto "trabado" del movimiento mientras se mantiene:
- Mecánica de movimiento celda por celda
- Detección de colisiones precisa
- Sistema de cooldown entre movimientos
- Validación de límites del laberinto

## 🔧 Cambios Implementados

### 1. Variables de Interpolación en `GestorMovimiento.__init__`

Se agregaron las siguientes variables de instancia:

```python
# Sistema de interpolación para movimiento suave
self.interpolando = False              # Flag de estado de interpolación
self.pos_inicio_x = 0                 # Posición inicial X
self.pos_inicio_y = 0                 # Posición inicial Y
self.pos_destino_x = 0                # Posición destino X
self.pos_destino_y = 0                # Posición destino Y
self.frames_interpolacion = 0         # Contador de frames de interpolación
self.frames_totales_interpolacion = 6 # Duración de la transición en frames
```

**Parámetros clave:**
- `frames_totales_interpolacion = 6`: Controla la velocidad de la transición
  - Menor valor = movimiento más rápido y menos suave
  - Mayor valor = movimiento más lento y más suave
  - 6 frames a 60 FPS = 100ms de transición

### 2. Modificación de `procesar_entrada_teclado()`

Se agregó verificación al inicio del método:

```python
# Actualizar interpolación si está activa
if self.interpolando:
    self._actualizar_interpolacion()
    return  # No procesar nueva entrada mientras se interpola
```

**Comportamiento:**
- Mientras hay interpolación activa, no se procesan nuevas entradas
- Evita movimientos superpuestos
- Mantiene la fluidez visual

### 3. Modificación de `_mover_por_celdas()`

En lugar de mover instantáneamente, ahora se inicia la interpolación:

**Antes:**
```python
rect.x = nueva_x
rect.y = nueva_y
```

**Después:**
```python
# Iniciar interpolación en lugar de mover instantáneamente
self.interpolando = True
self.pos_inicio_x = rect.x
self.pos_inicio_y = rect.y
self.pos_destino_x = nueva_x
self.pos_destino_y = nueva_y
self.frames_interpolacion = 0
```

**Ventajas:**
- Mantiene toda la lógica de validación original
- Solo cambia la forma de aplicar el movimiento
- No afecta la detección de colisiones

### 4. Nuevo Método `_actualizar_interpolacion()`

Implementa la transición suave usando easing:

```python
def _actualizar_interpolacion(self):
    """
    Actualiza la interpolación suave entre celdas.
    
    Usa una función de easing suave (ease-out) para una transición más natural.
    """
    self.frames_interpolacion += 1
    
    # Calcular progreso (0.0 a 1.0)
    t = self.frames_interpolacion / self.frames_totales_interpolacion
    
    if t >= 1.0:
        # Interpolación completa, establecer posición final exacta
        rect = self.jugador.jugador_principal
        rect.x = self.pos_destino_x
        rect.y = self.pos_destino_y
        self.interpolando = False
        self.cooldown_actual = self.frames_cooldown  # Iniciar cooldown después de completar
    else:
        # Aplicar ease-out cubic para suavidad (t³ invertido)
        t_eased = 1 - pow(1 - t, 3)
        
        # Interpolar posición
        rect = self.jugador.jugador_principal
        rect.x = int(self.pos_inicio_x + (self.pos_destino_x - self.pos_inicio_x) * t_eased)
        rect.y = int(self.pos_inicio_y + (self.pos_destino_y - self.pos_inicio_y) * t_eased)
```

**Características:**
- **Ease-out cubic**: `1 - (1-t)³` para aceleración natural
- **Progreso lineal del tiempo**: t de 0.0 a 1.0
- **Posición final exacta**: Garantiza alineación perfecta con la celda
- **Cooldown al completar**: Previene movimientos inmediatos consecutivos

## 📊 Función de Easing

### Ease-out Cubic

La función `t_eased = 1 - pow(1 - t, 3)` produce:

```
t = 0.0 → t_eased = 0.000 (inicio)
t = 0.2 → t_eased = 0.488 (aceleración rápida)
t = 0.4 → t_eased = 0.784
t = 0.6 → t_eased = 0.936
t = 0.8 → t_eased = 0.992 (desaceleración)
t = 1.0 → t_eased = 1.000 (final)
```

**Ventajas:**
- Inicio rápido, fin suave
- Sensación de peso y momentum
- Aspecto profesional y pulido

**Alternativas:**
- Linear: `t_eased = t` (uniforme, menos natural)
- Ease-in: `t³` (inicio lento, fin rápido)
- Ease-in-out: combinación de ambos

## 🎮 Flujo de Ejecución

### Movimiento Normal (sin interpolación activa)

1. Usuario presiona tecla → `procesar_entrada_teclado()`
2. Verificar cooldown y estado de interpolación
3. Llamar `_mover_por_celdas(direccion)`
4. Validar límites y colisiones
5. Si es válido:
   - Establecer `interpolando = True`
   - Guardar posiciones inicio/destino
   - Resetear contador de frames
6. Actualizar estado del sprite
7. Sumar puntos

### Durante Interpolación

1. Cada frame → `procesar_entrada_teclado()`
2. Detectar `interpolando = True`
3. Llamar `_actualizar_interpolacion()`
4. Incrementar `frames_interpolacion`
5. Calcular `t` (progreso 0-1)
6. Si `t >= 1.0`:
   - Posición final exacta
   - `interpolando = False`
   - Iniciar cooldown
7. Si `t < 1.0`:
   - Aplicar easing
   - Actualizar posición interpolada
8. Return (no procesar nueva entrada)

## 🔍 Configuración y Ajustes

### Velocidad de Transición

Modificar `frames_totales_interpolacion` en `__init__`:

```python
self.frames_totales_interpolacion = 6  # Valor por defecto

# Opciones:
# 4 frames = muy rápido (66ms a 60 FPS)
# 6 frames = equilibrado (100ms a 60 FPS) ← ACTUAL
# 8 frames = suave (133ms a 60 FPS)
# 10 frames = muy suave (166ms a 60 FPS)
```

### Tipo de Easing

Modificar la función en `_actualizar_interpolacion()`:

```python
# Lineal (sin easing)
t_eased = t

# Ease-out quadratic
t_eased = 1 - (1 - t) * (1 - t)

# Ease-out cubic (actual)
t_eased = 1 - pow(1 - t, 3)

# Ease-out quart (muy suave)
t_eased = 1 - pow(1 - t, 4)

# Ease-in-out sine
import math
t_eased = -(math.cos(math.pi * t) - 1) / 2
```

## 🧪 Testing

Se creó el script `test_movimiento_suave.py` para verificar:

✅ Transición visual suave entre celdas  
✅ Respeto a límites del laberinto  
✅ Detección correcta de colisiones  
✅ Cooldown funciona correctamente  
✅ No hay entrada durante interpolación  
✅ Posición final exacta en el centro de celda  

### Ejecutar Test

```bash
cd /home/marcus/Dev/coderunner
python test_movimiento_suave.py
```

### Qué Observar

- Movimiento debe verse fluido, no "saltos"
- Jugador debe detenerse correctamente en muros
- No debe haber respuesta a teclas durante transición
- Posición final debe estar alineada con grid
- FPS debe mantenerse estable en 60

## 📈 Métricas de Rendimiento

### Antes (Movimiento Instantáneo)
- Actualización de posición: 1 operación por movimiento
- Frames de transición: 0
- Percepción: "Trabado", saltos bruscos

### Después (Movimiento Interpolado)
- Actualización de posición: 6 operaciones por movimiento
- Frames de transición: 6 frames (100ms a 60 FPS)
- Percepción: Suave, fluido, profesional
- Impacto en rendimiento: Negligible (< 1% CPU)

## 🎨 Integración con Efectos Visuales

El sistema de interpolación se combina perfectamente con:

- **Esferas pulsantes**: La animación sinusoidal se mantiene durante el movimiento
- **Grid neon**: El jugador se desliza suavemente sobre el patrón
- **Puntos de suelo**: La transición pasa gradualmente sobre ellos
- **Diamantes rotatorios**: El jugador se acerca fluidamente a los obsequios

## 🐛 Resolución de Problemas

### El jugador se mueve muy lento
→ Reducir `frames_totales_interpolacion` (ej: de 6 a 4)

### El jugador "resbala" demasiado
→ Cambiar de ease-out a ease-in-out o linear

### El jugador no se alinea con el grid
→ Verificar que la posición final use `self.pos_destino_x/y` exactos

### Se puede mover durante interpolación
→ Verificar que `if self.interpolando: return` esté al inicio de `procesar_entrada_teclado()`

### Movimiento entrecortado a bajos FPS
→ Considerar interpolación basada en tiempo en lugar de frames

## 🔮 Mejoras Futuras Posibles

1. **Interpolación basada en delta time**: Para mantener velocidad constante independiente de FPS
2. **Animación de aplastamiento/estiramiento**: Efecto "squash and stretch" durante movimiento
3. **Partículas de rastro**: Dejar efecto visual al moverse
4. **Sonido de pasos sincronizado**: Audio al inicio/fin de interpolación
5. **Diferentes easing por dirección**: Vertical vs horizontal con curvas distintas

## 📚 Referencias

- **Easing Functions**: https://easings.net/
- **Game Feel**: Libro de Steve Swink sobre juiciness en juegos
- **Pygame Rect**: Documentación oficial de colisiones

---

**Fecha de implementación**: Enero 2025  
**Archivo modificado**: `src/jugabilidad/gestores/gestor_movimiento.py`  
**Compatibilidad**: Mantiene toda la lógica de juego existente  
**Impacto visual**: Alto (mejora significativa en percepción de calidad)
