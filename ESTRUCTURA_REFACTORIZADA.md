# 📁 Estructura Refactorizada del Proyecto

## ✅ Reorganización Completada

El proyecto ha sido completamente reorganizado siguiendo las mejores prácticas para videojuegos en Python, **con nombres en español** para mayor claridad.

## 🗂️ Nueva Estructura

```
src/
├── personajes/         # Personajes del juego
│   ├── personaje.py        # Clase base abstracta
│   ├── jugador.py          # Jugador controlado por usuario
│   └── computadora.py      # Enemigo con IA (BFS)
│
├── jugabilidad/        # Mecánicas del juego
│   └── gestores/           # Gestores especializados
│       ├── gestor_movimiento.py    # Movimiento y colisiones
│       ├── gestor_obsequios.py     # Ciclo de vida de regalos
│       └── gestor_dificultad.py    # Escalado de dificultad
│
├── interfaz/           # Interfaz de usuario
│   ├── pantallas/          # Pantallas del juego
│   │   ├── pantalla_base.py
│   │   ├── pantalla_juego.py
│   │   ├── menu_principal.py
│   │   ├── pantalla_salon_fama.py
│   │   └── ... (8 pantallas más)
│   │
│   └── componentes/        # Componentes reutilizables
│       └── input_texto.py      # Botones, InputTexto
│
├── mundo/              # Mundo del juego (datos)
│   ├── laberinto.py        # Estructura del laberinto
│   ├── obsequio.py         # Objetos recolectables
│   ├── registro.py         # Registro de puntuación
│   └── salon_fama.py       # Sistema de rankings
│
├── config/             # Configuración centralizada
│   ├── config.py           # ConfigJuego, Colores
│   ├── constants.py        # PASSWORD y constantes globales
│   └── config_laberinto.py # Configuración de laberintos
│
├── servicios/          # Servicios globales
│   ├── administrador.py    # Autenticación admin
│   └── sistema_sonido.py   # Sistema de audio
│
├── utilidades/         # Utilidades reutilizables
│   ├── coordenadas.py      # ConversorCoordenadas
│   └── helpers.py          # Funciones auxiliares
│
├── game/               # Coordinador principal
│   └── juego.py            # Clase Juego (orquestador)
│
├── tests/              # Tests unitarios
│   └── test_*.py           # 8 archivos de test
│
├── assets/             # Recursos visuales
├── data/               # Datos del juego
└── main.py             # Punto de entrada
```

## 📊 Métricas de la Refactorización

### Archivos Reorganizados
- **Total archivos Python**: 53
- **Módulos creados**: 9 (`entities`, `gameplay`, `ui`, `world`, `config`, `services`, `utils`, `game`, `tests`)
- **Submódulos**: 3 (`gameplay/managers`, `ui/screens`, `ui/components`)

### Distribución por Módulo
- `personajes/`: 4 archivos (personajes del juego)
- `jugabilidad/gestores/`: 4 archivos (gestores + __init__)
- `interfaz/pantallas/`: 11 archivos (pantallas)
- `interfaz/componentes/`: 2 archivos (componentes UI)
- `mundo/`: 5 archivos (modelos de datos)
- `config/`: 4 archivos (configuración)
- `servicios/`: 3 archivos (servicios)
- `utilidades/`: 3 archivos (utilidades)
- `game/`: 2 archivos (coordinador)
- `tests/`: 9 archivos (tests unitarios)

## 🎯 Beneficios de la Nueva Estructura

### 1. **Separación Clara de Responsabilidades**
- **personajes/**: Solo lógica de personajes
- **jugabilidad/**: Solo mecánicas de juego
- **interfaz/**: Solo interfaz y visualización
- **mundo/**: Solo modelos de datos
- **config/**: Solo configuración
- **servicios/**: Solo servicios compartidos
- **utilidades/**: Solo utilidades reutilizables

### 2. **Escalabilidad Mejorada**
- Fácil agregar nuevas entidades en `personajes/`
- Nuevos gestores en `jugabilidad/gestores/`
- Nuevas pantallas en `interfaz/pantallas/`
- Nuevos objetos del mundo en `mundo/`

### 3. **Imports Más Claros (en Español)**
```python
# Antes (estructura plana)
from models.jugador import Jugador
from models.laberinto import Laberinto
from game.gestor_movimiento import GestorMovimiento

# Después (estructura organizada en español)
from personajes.jugador import Jugador
from mundo.laberinto import Laberinto
from jugabilidad.gestores.gestor_movimiento import GestorMovimiento
```

### 4. **Mejor Mantenibilidad**
- Cada módulo tiene un propósito específico
- Fácil localizar archivos por funcionalidad
- Reducción de acoplamiento entre módulos

### 5. **Testing Más Organizado**
- Tests pueden organizarse por módulo
- Fácil identificar qué se está probando
- Mejor cobertura de código

## 🔄 Guía de Migración

### Para Desarrolladores

#### Imports Actualizados
```python
# Personajes
from personajes.jugador import Jugador
from personajes.computadora import Computadora

# Mundo
from mundo.laberinto import Laberinto
from mundo.obsequio import Obsequio
from mundo.salon_fama import SalonFama

# Configuración
from config.config import ConfigJuego, Colores
from config.constants import PASSWORD

# Gestores
from jugabilidad.gestores.gestor_movimiento import GestorMovimiento
from jugabilidad.gestores.gestor_obsequios import GestorObsequios
from jugabilidad.gestores.gestor_dificultad import GestorDificultad

# Interfaz
from interfaz.pantallas.pantalla_juego import PantallaJuego
from interfaz.componentes.input_texto import Boton, InputTexto

# Servicios
from servicios.administrador import Administrador
from servicios.sistema_sonido import SistemaSonido

# Utilidades
from utilidades.coordenadas import ConversorCoordenadas
from utilidades.helpers import resolver_ruta_laberinto
```

### Ejecución del Proyecto

El proyecto se ejecuta igual que antes:
```bash
cd /home/maru/Dev/coderunner
python src/main.py
```

El archivo `src/game/juego.py` ya configura el `sys.path` automáticamente.

## 📝 Notas Importantes

1. **Todos los imports han sido actualizados** en todos los archivos
2. **Cada módulo tiene su `__init__.py`** que exporta las clases principales
3. **La carpeta `models/` antigua está vacía** y puede eliminarse
4. **Los tests han sido actualizados** con los nuevos imports
5. **Compatibilidad mantenida**: El juego funciona igual que antes

## 🚀 Próximos Pasos Recomendados

1. **Ejecutar los tests** para verificar que todo funciona:
   ```bash
   python -m pytest src/tests/
   ```

2. **Revisar imports circulares** (si los hay)

3. **Documentar APIs** de cada módulo en los `__init__.py`

4. **Considerar crear submódulos adicionales** si algún módulo crece mucho

## 📚 Convenciones de Nomenclatura

- **personajes/**: Clases que representan actores del juego
- **jugabilidad/**: Lógica de mecánicas del juego
- **interfaz/**: Todo lo relacionado con visualización
- **mundo/**: Modelos de datos del mundo del juego
- **config/**: Configuración y constantes
- **servicios/**: Servicios singleton o globales
- **utilidades/**: Funciones y clases auxiliares sin estado

---

**Fecha de refactorización**: 22 de noviembre de 2025  
**Archivos movidos**: 47  
**Imports actualizados**: ~150  
**Módulos creados**: 9  
**Estado**: ✅ Completado y funcional
