# 🎮 Sistema de Pausa con Confirmación y Guardado de Progreso

## ✨ Funcionalidad Implementada

Al presionar **ESC** durante el juego, ahora se muestra un menú de confirmación con estética mitológica griega que permite:
- ✅ Salir y guardar progreso automáticamente
- ✅ Continuar jugando sin perder el estado
- ✅ Visualizar estadísticas actuales antes de decidir

## 🎯 Controles

### Durante el Juego
- **ESC**: Abrir menú de confirmación de salida
- **P**: Pausar/reanudar (pausa simple sin menú)

### En el Menú de Confirmación
- **S**: Salir y guardar progreso
- **N** o **ESC**: Cancelar y continuar jugando

## 📋 Cambios Implementados

### 1. Estado del Menú (`pantalla_juego.py`)

**Nueva variable de estado**:
```python
self.menu_pausa_salir = False  # True cuando se muestra confirmación
```

### 2. Método `_guardar_progreso()`

Guarda automáticamente en `src/data/progreso_guardado.json`:

**Datos guardados**:
```json
{
  "nombre_jugador": "Teseo",
  "puntaje": 1250,
  "vidas": 3,
  "tiempo_jugado": 145,
  "laberinto": "Laberinto 1",
  "dificultad": 2.5,
  "obsequios_restantes": 12,
  "fecha_guardado": "2025-11-25 14:30:45",
  "posicion_jugador": {"x": 320, "y": 256},
  "posicion_computadora": {"x": 160, "y": 128}
}
```

**Propósito**:
- Permitir continuar la partida más tarde
- Estadísticas para análisis
- Checkpoint automático al salir

### 3. Método `_dibujar_menu_confirmacion_salida()`

**Diseño mitológico griego**:
- Caja de diálogo con fondo de mármol beige
- Doble borde de bronce oxidado
- Título: "¿ABANDONAR EL LABERINTO?"
- Subtítulo: "Teseo desea escapar..."

**Información mostrada**:
- Puntaje actual
- Vidas restantes
- Tiempo jugado (en segundos)

**Opciones visuales**:
- Botón verde: `[S] Salir y Guardar Progreso`
- Botón rojo: `[N / ESC] Continuar Jugando`
- Nota al pie sobre el guardado automático

### 4. Lógica de Eventos Actualizada

**Flujo de control**:
```
Usuario presiona ESC
↓
¿Está en menú de confirmación?
├─ SÍ → Cancelar menú, volver al juego
└─ NO → Abrir menú de confirmación

En el menú:
├─ Presiona S → Guardar progreso + Salir
└─ Presiona N/ESC → Cerrar menú, continuar
```

**Código clave**:
```python
if self.menu_pausa_salir:
    if evento.key == pygame.K_s:
        self._guardar_progreso()
        return "salir"
    elif evento.key == pygame.K_n or evento.key == pygame.K_ESCAPE:
        self.menu_pausa_salir = False
```

## 🎨 Estética del Menú

### Paleta de Colores (Tema Griego)
- **Fondo overlay**: (20, 15, 10) - Pergamino oscuro
- **Caja principal**: (210, 195, 170) - Mármol beige
- **Bordes**: (184, 115, 51) - Bronce oxidado
- **Título**: (139, 69, 19) - Marrón antiguo
- **Subtítulo**: (101, 67, 33) - Marrón oscuro
- **Texto info**: (80, 60, 40) - Sepia

### Elementos Visuales
✅ Overlay oscuro semitransparente (alpha 200)  
✅ Caja con bordes redondeados (radius 10)  
✅ Doble borde de bronce (4px + 3px)  
✅ Sombras interiores para profundidad  
✅ Separador horizontal decorativo  
✅ Fondos sutiles para cada opción  
✅ Nota explicativa al pie  

## 📁 Archivos Modificados

| Archivo | Cambios |
|---------|---------|
| `pantalla_juego.py` | + `menu_pausa_salir` estado<br>+ `_guardar_progreso()` método<br>+ `_dibujar_menu_confirmacion_salida()` método<br>~ `manejar_eventos()` lógica ESC |
| `progreso_guardado.json` | Nuevo archivo de datos |
| `test_menu_pausa.py` | Script de prueba |

## 🧪 Testing

### Script de Prueba
```bash
python test_menu_pausa.py
```

**Verificar**:
- ESC abre menú de confirmación
- Menú muestra estadísticas simuladas
- S cierra el programa con mensaje de guardado
- N/ESC cierra el menú y continúa
- Estética griega coherente con el laberinto

### En el Juego Real
```bash
python src/main.py
```

1. Jugar normalmente
2. Presionar ESC
3. Ver menú con estadísticas reales
4. Probar ambas opciones (S y N)
5. Verificar `src/data/progreso_guardado.json`

## 📊 Comparación: Antes vs. Después

### ANTES
```
Presiona ESC → Sale inmediatamente
- Sin confirmación
- Sin guardado
- Pérdida de progreso
```

### DESPUÉS
```
Presiona ESC → Menú de confirmación
├─ Muestra estadísticas actuales
├─ Opción de guardar progreso
├─ Opción de continuar
└─ Estética coherente (tema griego)
```

## 🔮 Posibles Mejoras Futuras

### Sistema de Guardado
1. **Múltiples slots**: 3 partidas guardadas
2. **Auto-guardado**: Cada N minutos
3. **Cargar partida**: Menú principal con lista de guardados
4. **Checkpoint visual**: Icono que indique "Progreso guardado"

### Menú de Pausa
1. **Más opciones**:
   - Reiniciar nivel
   - Configuración rápida
   - Ver controles
2. **Animaciones**:
   - Transición fade in/out
   - Iconos animados
3. **Sonidos**:
   - Efecto al abrir menú
   - Confirmación al guardar

### Estadísticas Extendidas
```json
{
  "obsequios_recolectados": 25,
  "distancia_recorrida": 450,
  "veces_capturado": 2,
  "racha_maxima": 180,
  "nivel_mas_alto": 5
}
```

## 💾 Formato del Archivo de Guardado

### Estructura JSON
```json
{
  "nombre_jugador": "string",
  "puntaje": int,
  "vidas": int,
  "tiempo_jugado": int (segundos),
  "laberinto": "string",
  "dificultad": float,
  "obsequios_restantes": int,
  "fecha_guardado": "YYYY-MM-DD HH:MM:SS",
  "posicion_jugador": {
    "x": int (píxeles),
    "y": int (píxeles)
  },
  "posicion_computadora": {
    "x": int,
    "y": int
  }
}
```

### Ubicación
```
src/data/progreso_guardado.json
```

## 🎭 Narrativa Mitológica

El menú integra el tema del mito de Teseo:

**Título**: "¿ABANDONAR EL LABERINTO?"  
**Subtítulo**: "Teseo desea escapar..."  
**Contexto**: El jugador (Teseo) decide si abandonar su búsqueda o continuar enfrentando al Minotauro

**Simbolismo**:
- Mármol griego → Templo de Creta
- Bronce → Armas antiguas
- Hilo dorado (implícito) → Hilo de Ariadna como "guardado"

## ✅ Beneficios del Sistema

### Para el Jugador
- ✨ No pierde progreso al salir
- 🎯 Decisión informada (ve estadísticas)
- 🔄 Puede reanudar más tarde
- 🛡️ Protección contra salidas accidentales

### Para el Desarrollador
- 📊 Datos de partidas para análisis
- 🐛 Debugging mejorado (estados guardados)
- 🎮 UX profesional y pulida
- 🏛️ Coherencia temática

---

**Estado**: ✅ Implementado y funcional  
**Compatibilidad**: Total con sistema existente  
**Tema**: Mitología griega coherente  
**Testing**: Script incluido (test_menu_pausa.py)
