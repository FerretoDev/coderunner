# 📖 Manual de Usuario - Theseus Runner

## Índice

1. [Introducción](#introducción)
2. [Requisitos del Sistema](#requisitos-del-sistema)
3. [Instalación](#instalación)
4. [Inicio Rápido](#inicio-rápido)
5. [Menú Principal](#menú-principal)
6. [Jugabilidad](#jugabilidad)
7. [Controles](#controles)
8. [Sistema de Puntuación](#sistema-de-puntuación)
9. [Salón de la Fama](#salón-de-la-fama)
10. [Panel de Administración](#panel-de-administración)
11. [Consejos y Estrategias](#consejos-y-estrategias)
12. [Solución de Problemas](#solución-de-problemas)
13. [Historial de Versiones](#historial-de-versiones)

---

## Introducción

### ¿Qué es Theseus Runner?

**Theseus Runner** es un emocionante juego de laberinto inspirado en la mitología griega, donde el jugador toma el rol de Teseo navegando a través de laberintos peligrosos. Tu objetivo es recolectar obsequios mientras evitas ser capturado por el Minotauro (la computadora enemiga).

### Historia del Juego

El juego está basado en el mito griego de Teseo y el Minotauro. En la antigua Grecia, el héroe Teseo entró al laberinto del rey Minos para enfrentar al temible Minotauro. En este juego, tú eres Teseo, pero en lugar de derrotar al Minotauro, debes escapar de él mientras recolectas valiosos tesoros.

### Características Principales

- 🎮 **Estilo Arcade Retro**: Interfaz visual inspirada en juegos clásicos de consola
- 🧠 **IA Inteligente**: El enemigo utiliza algoritmo BFS para perseguirte de manera inteligente
- 📈 **Dificultad Progresiva**: El juego se vuelve más desafiante con el tiempo
- 🏆 **Salón de la Fama**: Guarda y compara tus mejores puntuaciones
- 🎵 **Efectos de Sonido**: Feedback auditivo inmersivo
- 🔧 **Personalizable**: Carga tus propios laberintos

---

## Requisitos del Sistema

### Mínimos

- **Sistema Operativo**: Windows 10, macOS 10.14+, o Linux (Ubuntu 20.04+)
- **Python**: Versión 3.8 o superior
- **RAM**: 512 MB
- **Espacio en Disco**: 50 MB
- **Pantalla**: Resolución mínima de 800x600 píxeles

### Recomendados

- **Python**: Versión 3.10 o superior
- **RAM**: 1 GB
- **Pantalla**: Resolución de 1920x1080 o superior

---

## Instalación

### Paso 1: Clonar el Repositorio

Abre una terminal o línea de comandos y ejecuta:

```bash
git clone https://github.com/FerretoDev/coderunner.git
cd coderunner
```

### Paso 2: Crear un Entorno Virtual (Recomendado)

#### En Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

#### En Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Verificar la Instalación

```bash
python src/main.py
```

Si todo está correctamente instalado, verás el menú principal del juego.

---

## Inicio Rápido

1. **Abre el juego** ejecutando `python src/main.py`
2. **Selecciona "Iniciar Juego"** en el menú principal
3. **Ingresa tu nombre** de jugador
4. **Usa las flechas o WASD** para moverte por el laberinto
5. **Recolecta los obsequios** (puntos dorados brillantes)
6. **¡Evita al enemigo rojo!** Si te atrapa, pierdes una vida
7. **Intenta conseguir el mayor puntaje posible**

---

## Menú Principal

Al iniciar el juego, verás el menú principal con las siguientes opciones:

```
┌─────────────────────────────────┐
│       THESEUS RUNNER            │
├─────────────────────────────────┤
│    [1] Iniciar Juego           │
│    [2] Salón de la Fama        │
│    [3] Administración          │
│    [4] Salir                   │
└─────────────────────────────────┘
```

### Opciones del Menú

| Opción | Descripción |
|--------|-------------|
| **Iniciar Juego** | Comienza una nueva partida |
| **Salón de la Fama** | Muestra los mejores puntajes |
| **Administración** | Acceso a funciones administrativas |
| **Salir** | Cierra el juego |

### Navegación

- **Mouse**: Haz clic en los botones para seleccionar
- **Teclado**: Presiona `ESC` para salir

---

## Jugabilidad

### Objetivo del Juego

Tu objetivo es sobrevivir el mayor tiempo posible mientras recolectas obsequios para aumentar tu puntuación. El juego termina cuando pierdes todas tus vidas.

### Elementos del Juego

#### El Jugador (Teseo)
- Representado por un círculo **cyan brillante**
- Puedes moverte en 4 direcciones: arriba, abajo, izquierda, derecha
- Comienzas con **3 vidas**

#### El Enemigo (Minotauro/Computadora)
- Representado por un círculo **rojo neón**
- Te persigue usando un algoritmo inteligente (BFS)
- Su velocidad aumenta con el tiempo

#### Los Obsequios
- Representados por **puntos dorados brillantes** con animación
- Aparecen en posiciones aleatorias del laberinto
- Desaparecen después de un tiempo y reaparecen en otro lugar
- Cada uno vale puntos (valor configurable, típicamente 10-50 puntos)

#### El Laberinto
- Paredes en **azul oscuro** con efecto 3D
- Pasillos con textura de piedra
- No puedes atravesar las paredes

### Sistema de Vidas

- Comienzas con **3 vidas** (representadas como corazones en el HUD)
- Pierdes una vida cada vez que el enemigo te captura
- Al perder una vida, tanto tú como el enemigo reaparecen en sus posiciones iniciales
- El juego termina cuando pierdes todas las vidas

### Dificultad Progresiva

El juego aumenta su dificultad automáticamente:

| Nivel | Velocidad | Descripción |
|-------|-----------|-------------|
| 1.0x | Inicial | Velocidad base del enemigo |
| 1.5x | Media | Enemigo moderadamente rápido |
| 2.0x+ | Alta | Enemigo muy rápido |

La velocidad del enemigo aumenta cada **10 segundos** de juego.

---

## Controles

### Durante el Juego

| Tecla | Acción |
|-------|--------|
| `↑` o `W` | Mover arriba |
| `↓` o `S` | Mover abajo |
| `←` o `A` | Mover izquierda |
| `→` o `D` | Mover derecha |
| `P` | Pausar/Reanudar juego |
| `U` | Activar/Desactivar música |
| `ESC` | Salir al menú principal |

### En Menús

| Tecla | Acción |
|-------|--------|
| Click izquierdo | Seleccionar opción |
| `ESC` | Volver/Salir |
| `Enter` | Confirmar (en campos de texto) |

---

## Sistema de Puntuación

### Cómo Ganar Puntos

1. **Recolectar Obsequios**: Cada obsequio recolectado suma puntos a tu puntaje
2. **Sobrevivir**: Mientras más tiempo sobrevivas, más oportunidades de recolectar obsequios

### HUD (Heads-Up Display)

El HUD muestra información importante en tiempo real:

```
┌─────────────────────────────────────────────────────┐
│ Nombre     ★ 000150     00:45                       │
│ ♥♥♥        Nivel 1.2x   WASD: Mover  P: Pausa      │
└─────────────────────────────────────────────────────┘
```

| Elemento | Descripción |
|----------|-------------|
| **Nombre** | Tu nombre de jugador |
| **★ Puntos** | Puntaje actual (6 dígitos) |
| **Tiempo** | Tiempo transcurrido (MM:SS) |
| **♥ Vidas** | Corazones restantes |
| **Nivel** | Multiplicador de dificultad actual |
| **Controles** | Recordatorio de teclas |

---

## Salón de la Fama

### Acceso

Desde el menú principal, selecciona **"Salón de la Fama"**.

### Contenido

El Salón de la Fama muestra:

1. **Estadísticas Generales**:
   - Total de partidas jugadas
   - Mejor puntaje histórico
   - Promedio de puntos

2. **Podio (Top 3)**:
   - 🥇 **1er Lugar**: Marco dorado
   - 🥈 **2do Lugar**: Marco plateado
   - 🥉 **3er Lugar**: Marco bronce

3. **Tabla de Récords**:
   - Posiciones del 4° al 10° lugar
   - Muestra: Posición, Nombre, Puntaje, Laberinto

### Guardado Automático

Tu puntaje se guarda automáticamente al terminar cada partida (cuando llegas a Game Over).

---

## Panel de Administración

### Acceso

1. Desde el menú principal, selecciona **"Administración"**
2. Ingresa la clave de administrador (por defecto: `admin123`)
3. Presiona "Ingresar" o `Enter`

### Funciones Administrativas

#### 1. Cargar Laberinto

Permite cargar un archivo de laberinto personalizado en formato JSON.

**Pasos:**
1. Selecciona "Cargar Laberinto"
2. Ingresa la ruta del archivo JSON o selecciona uno de los laberintos predefinidos:
   - `laberinto1.json` - Laberinto básico
   - `laberinto2.json` - Laberinto intermedio
   - `laberinto3.json` - Laberinto avanzado
3. Confirma la carga

**Formato del archivo de laberinto:**
```json
{
  "nombre": "Mi Laberinto",
  "laberinto": [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1]
  ],
  "jugador_inicio": {"x": 1, "y": 1},
  "computadora_inicio": {"x": 3, "y": 3},
  "obsequios": [
    {"x": 2, "y": 1, "valor": 10},
    {"x": 1, "y": 3, "valor": 20}
  ]
}
```

Donde:
- `1` = Pared
- `0` = Pasillo (espacio libre)

#### 2. Reiniciar Salón de Fama

Elimina todos los registros del Salón de la Fama.

**⚠️ Advertencia**: Esta acción es irreversible. Se te pedirá confirmación antes de proceder.

#### 3. Volver al Menú

Regresa al menú principal.

---

## Consejos y Estrategias

### Para Principiantes

1. **Conoce el laberinto**: Antes de moverte rápidamente, observa la estructura del laberinto
2. **Mantén la calma**: El enemigo es inteligente pero predecible
3. **Usa los pasillos largos**: Son más fáciles para esquivar al enemigo
4. **Prioriza la supervivencia**: Es mejor perder un obsequio que una vida

### Para Jugadores Avanzados

1. **Anticipa el pathfinding**: El enemigo siempre toma la ruta más corta hacia ti
2. **Usa las esquinas**: Puedes confundir brevemente al enemigo en las intersecciones
3. **Gestiona el tiempo**: Recuerda que la dificultad aumenta cada 10 segundos
4. **Memoriza los spawns**: Los obsequios reaparecen en posiciones aleatorias válidas

### Estrategias de Puntuación

1. **Recolección eficiente**: Planea una ruta que pase por varios obsequios
2. **Timing de obsequios**: Los obsequios desaparecen después de ~10 segundos
3. **Arriesga sabiamente**: A veces vale la pena arriesgar una vida por un obsequio de alto valor

---

## Solución de Problemas

### El juego no inicia

**Problema**: Error al ejecutar `python src/main.py`

**Soluciones**:
1. Verifica que Python 3.8+ está instalado: `python --version`
2. Asegúrate de que Pygame está instalado: `pip install pygame`
3. Verifica que estás en el directorio correcto del proyecto

### La pantalla está en blanco

**Problema**: El juego inicia pero la pantalla está vacía

**Soluciones**:
1. Actualiza los drivers de tu tarjeta gráfica
2. Prueba redimensionar la ventana
3. Verifica que tienes una resolución de pantalla de al menos 800x600

### El sonido no funciona

**Problema**: No se escuchan efectos de sonido o música

**Soluciones**:
1. Verifica que los archivos de sonido existen en `src/assets/sonidos/`
2. Ajusta el volumen de tu sistema
3. Presiona `U` para activar/desactivar la música

### El juego está lento

**Problema**: FPS bajos o lag

**Soluciones**:
1. Cierra otras aplicaciones
2. Verifica los requisitos mínimos del sistema
3. Prueba con una resolución de pantalla menor

### Error de carga de laberinto

**Problema**: "Error al cargar laberinto"

**Soluciones**:
1. Verifica que el archivo JSON tiene el formato correcto
2. Asegúrate de que la ruta del archivo es correcta
3. Verifica que el laberinto tiene al menos una posición válida para el jugador y el enemigo

---

## Historial de Versiones

Este historial está basado en el análisis de los commits del repositorio.

### Versión Actual (Noviembre 2024)

#### Características Principales
- ✅ Sistema de juego completo con laberintos
- ✅ IA enemiga con pathfinding BFS
- ✅ Sistema de puntajes y Salón de la Fama
- ✅ Interfaz estilo arcade retro
- ✅ Dificultad progresiva
- ✅ Sistema de sonido
- ✅ Panel de administración

#### Evolución del Desarrollo

**Fase 1 - Estructura Base**
- Implementación de la estructura del proyecto
- Sistema de menú principal con botones
- Modelo básico de laberinto
- Sistema de movimiento del jugador

**Fase 2 - Mecánicas del Juego**
- Sistema de puntajes y vidas
- IA enemiga con persecución inteligente
- Obsequios coleccionables con temporizador
- Sistema de colisiones

**Fase 3 - Interfaz y UX**
- Interfaz estilo arcade/pixel art
- Gestión centralizada de fuentes
- Componentes reutilizables (botones, títulos)
- HUD mejorado con información en tiempo real

**Fase 4 - Características Avanzadas**
- Dificultad progresiva
- Salón de la Fama con estadísticas
- Carga de laberintos externos (JSON)
- Sistema de sonido con música de fondo

**Fase 5 - Optimización**
- Refactorización del código
- Eliminación de código obsoleto
- Mejoras de rendimiento
- Configuración centralizada

---

## Créditos

### Equipo de Desarrollo
- **Paulo Anchía** - C5C482

### Tecnologías Utilizadas
- **Python** - Lenguaje de programación
- **Pygame** - Motor de juego
- **JSON** - Formato de datos para laberintos

### Recursos
- Fuente: **Press Start 2P** - Estilo retro arcade
- Inspiración: Juegos clásicos de laberinto

---

## Licencia

Este proyecto es de uso académico para el curso de Programación I.

---

## Contacto y Soporte

Para reportar errores o sugerencias, por favor abre un issue en el repositorio de GitHub:

🔗 **GitHub**: [FerretoDev/coderunner](https://github.com/FerretoDev/coderunner)

---

*Última actualización: Noviembre 2024*
