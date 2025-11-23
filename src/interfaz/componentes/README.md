# Componentes Arcade Reutilizables

Sistema de componentes UI para crear interfaces estilo pixel art / arcade retro con Pygame.

## 📦 Componentes Disponibles

### 1. `BotonAdaptable` - Botones que se ajustan al texto

Botones que calculan automáticamente su tamaño según el contenido, perfectos para fuentes pixel art como Press Start 2P.

#### Uso Básico

```python
from interfaz.componentes.boton_adaptable import BotonAdaptable, BotonGrande, BotonPequeño

# Botón adaptable personalizado
boton = BotonAdaptable(
    x=100, 
    y=200, 
    texto="Salón de la Fama",
    accion="salon_fama",
    padding_horizontal=30,
    padding_vertical=15,
    ancho_minimo=120,
    ancho_maximo=300
)

# Botón grande (preset para acciones principales)
boton_grande = BotonGrande(0, 350, "Iniciar Juego", accion=1)
boton_grande.centrar_horizontalmente(screen.get_width())

# Botón pequeño (preset para acciones secundarias)
boton_pequeno = BotonPequeño(10, 10, "Volver", accion="back")

# Dibujar
boton.dibujar(screen)

# Manejar eventos
if boton.manejar_evento(evento, pygame.mouse.get_pos()):
    print(f"Acción: {boton.accion}")
```

#### Características

- ✅ **Auto-dimensionamiento**: Calcula ancho y alto según el texto
- ✅ **Padding configurable**: Espacio horizontal y vertical personalizable
- ✅ **Límites de tamaño**: Ancho mínimo/máximo opcionales
- ✅ **Efectos 3D**: Bordes iluminados en hover estilo pixel art
- ✅ **Cambio de texto dinámico**: `boton.cambiar_texto("Nuevo texto")`
- ✅ **Centrado fácil**: `boton.centrar_horizontalmente(ancho_pantalla)`

#### Variantes Predefinidas

| Clase | Font Size | Padding H/V | Tamaño Mínimo | Alto Fijo |
|-------|-----------|-------------|---------------|-----------|
| `BotonAdaptable` | 14px (texto_pequeño) | 30/15 | 120px | Automático |
| `BotonGrande` | 16px (texto_normal) | 40/20 | 180px | 60px |
| `BotonPequeño` | 12px (texto_info) | 20/10 | 100px | 40px |

---

### 2. `TituloArcade` - Títulos con sombras múltiples

Títulos con efectos de sombra triple estilo arcade retro (dorado + cyan + sombra oscura).

#### Uso Básico

```python
from interfaz.componentes.titulo_arcade import TituloArcade

# Título grande
titulo = TituloArcade("LABERINTO RETRO", y=150, estilo='grande')
titulo.dibujar(screen)

# Título mediano
titulo_mediano = TituloArcade("Nivel 1", y=100, estilo='mediano')

# Título pequeño
titulo_pequeno = TituloArcade("¡Victoria!", y=300, estilo='pequeño')
```

#### Estilos Disponibles

- **`'grande'`**: 48px - Para títulos principales
- **`'mediano'`**: 36px - Para secciones
- **`'pequeño'`**: 20px - Para subtítulos destacados

#### Efecto Visual

```
Capa 3 (sombra oscura): +4px offset
Capa 2 (cyan): +2px offset  
Capa 1 (dorado): Posición original
```

---

### 3. `SubtituloArcade` - Subtítulos centrados

Texto centrado simple con color personalizable.

#### Uso Básico

```python
from interfaz.componentes.titulo_arcade import SubtituloArcade
from config.colores import PaletaColores

# Subtítulo con color por defecto (cyan)
subtitulo = SubtituloArcade("El laberinto retro", y=220)

# Subtítulo con color personalizado
subtitulo_oro = SubtituloArcade("¡Nuevo récord!", y=400, color=PaletaColores.ORO)

subtitulo.dibujar(screen)
```

---

### 4. `LineaDecorativa` - Líneas horizontales arcade

Líneas decorativas horizontales con colores vibrantes.

#### Uso Básico

```python
from interfaz.componentes.titulo_arcade import LineaDecorativa

# Línea doble (cyan + verde)
linea_doble = LineaDecorativa(y=250, ancho_porcentaje=50, doble=True)

# Línea simple
linea_simple = LineaDecorativa(y=300, ancho_porcentaje=70, doble=False)

linea_doble.dibujar(screen)
```

#### Parámetros

- **`y`**: Posición vertical
- **`ancho_porcentaje`**: Porcentaje del ancho de pantalla (1-100)
- **`doble`**: `True` = dos líneas paralelas, `False` = línea simple

---

### 5. `FooterArcade` - Footer con iconos

Footer centrado en la parte inferior con soporte para emojis.

#### Uso Básico

```python
from interfaz.componentes.titulo_arcade import FooterArcade

# Footer con icono
footer = FooterArcade("Usa el mouse para seleccionar", icono="🖱️")

# Footer sin icono
footer_simple = FooterArcade("Presiona ESC para salir")

footer.dibujar(screen)
```

---

## 🎨 Ejemplo Completo: Menú con Componentes

```python
import pygame
from interfaz.componentes.boton_adaptable import BotonGrande
from interfaz.componentes.titulo_arcade import (
    TituloArcade, SubtituloArcade, LineaDecorativa, FooterArcade
)
from config.colores import PaletaColores

class MenuPrincipal:
    def __init__(self, screen):
        self.screen = screen
        self.ancho = screen.get_width()
        
        # Crear componentes visuales
        self.titulo = TituloArcade("MI JUEGO RETRO", 150, 'grande')
        self.subtitulo = SubtituloArcade("La aventura comienza", 220)
        self.linea = LineaDecorativa(250, ancho_porcentaje=50, doble=True)
        self.footer = FooterArcade("Usa el mouse para jugar", "🎮")
        
        # Crear botones adaptativos
        self.botones = []
        opciones = [
            ("Jugar", 1),
            ("Opciones", 2),
            ("Salir", 3)
        ]
        
        y_inicial = 350
        for i, (texto, accion) in enumerate(opciones):
            y = y_inicial + i * 82  # 60px alto + 22px espacio
            boton = BotonGrande(0, y, texto, accion)
            boton.centrar_horizontalmente(self.ancho)
            self.botones.append(boton)
    
    def dibujar(self):
        self.screen.fill(PaletaColores.FONDO_PRINCIPAL)
        
        # Dibujar componentes
        self.titulo.dibujar(self.screen)
        self.linea.dibujar(self.screen)
        self.subtitulo.dibujar(self.screen)
        self.footer.dibujar(self.screen)
        
        for boton in self.botones:
            boton.dibujar(self.screen)
        
        pygame.display.flip()
    
    def manejar_evento(self, evento):
        mouse_pos = pygame.mouse.get_pos()
        for boton in self.botones:
            if boton.manejar_evento(evento, mouse_pos):
                return boton.accion
        return None
```

---

## 🎯 Ventajas del Sistema

### Antes (código manual)

```python
# 60+ líneas de código repetitivo para cada pantalla
ancho_boton = min(240, self.ancho // 5)
alto_boton = 60
espacio = 22
# ... cálculos de posición ...
# ... renderizado manual de sombras ...
# ... dibujo de líneas decorativas ...
# ... footer con posicionamiento manual ...
```

### Después (componentes)

```python
# 10 líneas - declarativo y reutilizable
self.titulo = TituloArcade("JUEGO", 150, 'grande')
self.footer = FooterArcade("Instrucciones", "🎮")
boton = BotonGrande(0, 350, "Jugar", accion=1)
boton.centrar_horizontalmente(self.ancho)
```

### Beneficios

- ✅ **90% menos código** en cada pantalla
- ✅ **Consistencia visual** automática
- ✅ **Fácil mantenimiento** - cambios en un solo lugar
- ✅ **Auto-adaptación** al tamaño del texto
- ✅ **Reusabilidad** total entre pantallas
- ✅ **Lectura clara** del código

---

## 🔧 Personalización

### Cambiar Colores de Botones

```python
class BotonPersonalizado(BotonAdaptable):
    def __init__(self, x, y, texto, accion=None):
        super().__init__(x, y, texto, accion)
        # Cambiar colores
        self.COLOR_NORMAL = (100, 50, 150)  # Morado
        self.COLOR_HOVER = (150, 80, 200)   # Morado claro
        self.COLOR_TEXTO_HOVER = (255, 255, 0)  # Amarillo
```

### Crear Variante de Título

```python
class TituloEspecial(TituloArcade):
    def __init__(self, texto, y):
        super().__init__(texto, y, 'grande')
        # Cambiar colores del efecto
        self.COLOR_SOMBRA_1 = (255, 0, 0)  # Rojo
        self.COLOR_SOMBRA_2 = (255, 128, 0)  # Naranja
        self.COLOR_PRINCIPAL = (255, 255, 0)  # Amarillo
```

---

## 📊 Compatibilidad

- ✅ **Fuentes Pixel Art**: Press Start 2P, VT323, etc.
- ✅ **Pantallas Adaptativas**: Funciona con cualquier resolución
- ✅ **Pygame 2.x**: Compatible con versiones modernas
- ✅ **Python 3.8+**: Type hints opcionales

---

## 🚀 Próximos Componentes (Roadmap)

- [ ] `CuadroDialogo` - Diálogos con bordes retro
- [ ] `BarraProgreso` - Barras de carga estilo pixel
- [ ] `MenuDropdown` - Menús desplegables
- [ ] `ToastNotification` - Notificaciones temporales
- [ ] `InputTextoArcade` - Campos de entrada con estilo retro

---

## 📝 Notas Técnicas

### Performance

- Renderizado de texto cacheado internamente por Pygame
- No hay generación dinámica de superficies en cada frame
- Suitable para juegos a 60 FPS

### Dependencias

```python
# Requeridas
from interfaz.gestor_fuentes import GestorFuentes
from config.colores import PaletaColores

# Pygame
import pygame
```

---

¡Disfruta creando UIs retro con estos componentes! 🎮✨
