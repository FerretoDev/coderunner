# Evaluación del Proyecto según Rúbrica - Entregable 3

**Proyecto:** Laberinto de Teseo y el Minotauro  
**Fecha:** 26 de Noviembre de 2025

## Criterios de Evaluación (50 puntos)

### 1. Aplicación funcional completa (5/5 puntos)
**Estado:** Funciona correctamente en su totalidad

- El juego se ejecuta sin errores
- Todos los componentes están integrados
- Movimiento del jugador con teclas de dirección
- Algoritmo BFS de persecución implementado
- Sistema de colisiones funcional
- Sistema de vidas (3 vidas)
- Recolección de obsequios
- Game Over y Victoria implementados
- Música de fondo y efectos de sonido

**Archivos clave:**
- `src/main.py` - Punto de entrada
- `src/game/juego.py` - Lógica principal
- `src/interfaz/pantallas/pantalla_juego.py` - Pantalla de juego

---

### 2. Salón de la fama implementado (5/5 puntos)
**Estado:** Funcional, persistente y ordenado correctamente

- Persistencia en archivo JSON (`src/data/salon_fama.json`)
- Ordenamiento correcto por puntaje (descendente)
- Desempate por fecha (más reciente primero)
- Guardado automático después de cada partida
- Visualización del Top 10
- Estadísticas generales (total partidas, mejor puntaje, promedio)

**Archivos clave:**
- `src/mundo/salon_fama.py` - Lógica del salón
- `src/mundo/registro.py` - Modelo de datos
- `src/interfaz/pantallas/pantalla_salon_fama.py` - Visualización

**Tests:**
- `src/tests/test_salon_fama.py` - 11 casos de prueba

---

### 3. Menú de opciones (5/5 puntos)
**Estado:** Menú funcional, claro y completo

Opciones implementadas:
1. **Jugar** - Inicia nueva partida
2. **Salón de la Fama** - Visualiza récords
3. **Administrador** - Submenu con:
   - Cargar Laberinto
   - Reiniciar Salón de Fama
   - Volver
4. **Salir** - Cierra la aplicación

**Archivos clave:**
- `src/interfaz/pantallas/menu_principal.py`
- `src/interfaz/pantallas/pantalla_menu_administrador.py`
- `src/interfaz/pantallas/pantalla_carga_laberinto.py`

**Tests:**
- `src/tests/test_menu_navegacion.py` - Casos de prueba de navegación

---

### 4. Persistencia de datos (5/5 puntos)
**Estado:** Persistencia clara, estable y validada

**Salón de la Fama:**
- Archivo: `src/data/salon_fama.json`
- Guardado automático después de cada partida
- Carga al iniciar la aplicación
- Validación de estructura JSON
- Manejo de errores (archivo corrupto, no existente)

**Laberintos:**
- Directorio: `src/data/laberintos/`
- Archivos: `laberinto1.json`, `laberinto2.json`, `laberinto3.json`
- Carga dinámica según selección
- Validación de estructura (mapa, inicio_jugador, inicio_computadora, obsequios)

**Configuración:**
- Archivo: `src/data/config_laberinto.json`
- Guarda laberinto activo

**Archivos clave:**
- `src/utilidades/helpers.py` - Funciones de carga/guardado JSON
- `src/mundo/laberinto.py` - Carga de laberintos
- `src/config/config_laberinto.py` - Gestión de configuración

**Tests:**
- `src/tests/test_carga_laberintos.py` - 10+ casos de validación

---

### 5. Interfaz visual final (5/5 puntos)
**Estado:** Visual atractiva, clara y bien integrada

**Características:**
- Tema mitológico griego coherente
- Paleta de colores personalizada (azul oscuro, dorado, blanco)
- Sprites personalizados (Teseo y Minotauro)
- Efectos visuales (partículas, sombras, reflejos)
- HUD informativo (vidas, puntaje, tiempo, laberinto)
- Títulos con efectos arcade
- Botones con hover y estados visuales
- Podio destacado para Top 3
- Animaciones suaves

**Archivos clave:**
- `src/config/colores.py` - Paleta de colores
- `src/interfaz/componentes/` - Componentes reutilizables
- `src/interfaz/paleta_ui.py` - Estilos UI
- `src/assets/imagenes/` - Sprites

---

### 6. Código estructurado y comentado (5/5 puntos)
**Estado:** Bien organizado, modular y con comentarios útiles

**Estructura del proyecto:**
```
src/
├── config/          # Configuraciones globales
├── data/            # Archivos JSON (laberintos, puntajes)
├── game/            # Lógica del juego
├── interfaz/        # UI y componentes visuales
├── jugabilidad/     # Gestores de juego
├── mundo/           # Entidades del mundo (laberinto, salón)
├── personajes/      # Jugador y computadora
├── servicios/       # Sistemas auxiliares (sonido, admin)
├── tests/           # Tests automatizados
└── utilidades/      # Funciones auxiliares
```

**Principios aplicados:**
- Separación de responsabilidades
- Clases con responsabilidad única
- Métodos documentados con docstrings
- Nombres descriptivos
- Constantes en archivos de configuración
- Comentarios explicativos en lógica compleja

---

### 7. Documentación final con casos de prueba (5/5 puntos)
**Estado:** Pruebas completas, cubren HU y escenarios relevantes

**Tests organizados por Historia de Usuario:**

1. **HU-01**: Movimiento del jugador (4 direcciones)
2. **HU-02**: Persecución con BFS
3. **HU-03, 04, 05**: Sistema de vidas y colisiones
4. **HU-06, 07**: Mapa del laberinto
5. **HU-08, 09, 10**: Puntajes y obsequios
6. **HU-11, 12, 13**: Salón de la fama
7. **HU-14, 15**: Carga dinámica de laberintos
8. **HU-16, 17**: Menú y navegación

**Total de archivos de test:** 9
**Casos de prueba estimados:** 50+

**Documentación:**
- `README.md` - Documentación general
- `src/tests/README.md` - Guía de tests
- `docs/` - Documentación adicional
- Docstrings en todas las clases y métodos

---

### 8. Defensa del proyecto (Pendiente)
**Estado:** Por realizar

**Preparación:**
- Código limpio y funcional
- Capacidad de explicar arquitectura
- Conocimiento de algoritmo BFS
- Comprensión del sistema de persistencia
- Demostración de funcionalidades

---

### 9. Trabajo colaborativo (Pendiente)
**Estado:** Por realizar

**Recomendaciones:**
- Todos deben conocer la estructura del proyecto
- Dividir la exposición por módulos
- Practicar respuestas a preguntas técnicas
- Preparar demo en vivo

---

### 10. Entrega del código fuente y documentos (5/5 puntos)
**Estado:** Entregado completo, organizado y funcional

**Archivos incluidos:**
- Código fuente completo
- Tests automatizados
- Documentación (README, docs/)
- Archivos de configuración (pyproject.toml, requirements.txt)
- Datos de prueba (laberintos, salón de fama)
- Assets (sprites, fuentes, sonidos)

**Control de versiones:**
- Repositorio Git con historial de commits
- Branches organizadas
- Commits descriptivos

---

## Resumen de Puntuación Estimada

| Criterio | Puntos Obtenidos | Puntos Máximos |
|----------|------------------|----------------|
| 1. Aplicación funcional | 5 | 5 |
| 2. Salón de la fama | 5 | 5 |
| 3. Menú de opciones | 5 | 5 |
| 4. Persistencia de datos | 5 | 5 |
| 5. Interfaz visual | 5 | 5 |
| 6. Código estructurado | 5 | 5 |
| 7. Documentación/Tests | 5 | 5 |
| 8. Defensa | Pendiente | 5 |
| 9. Trabajo colaborativo | Pendiente | 5 |
| 10. Entrega | 5 | 5 |
| **TOTAL** | **45/50** | **50** |

**Nota:** Los criterios 8 y 9 dependen de la presentación y defensa presencial.

---

## Mejoras Realizadas

1. Eliminados prints de depuración innecesarios
2. Mantenidos solo logs de errores críticos
3. Código optimizado y limpio
4. Sin emojis en el código
5. Comentarios claros y útiles

## Recomendaciones para la Defensa

1. **Demostrar flujo completo:** Menú → Juego → Game Over → Salón de Fama
2. **Explicar algoritmo BFS:** Mostrar código y comportamiento en vivo
3. **Mostrar carga dinámica:** Cambiar laberinto desde menú administrador
4. **Ejecutar tests:** Demostrar calidad con pytest
5. **Explicar arquitectura:** Separación de responsabilidades
6. **Mostrar persistencia:** Ver archivo JSON antes/después de partida
