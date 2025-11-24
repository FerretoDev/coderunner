# 🎮 Theseus Runner

**Juego educativo de laberinto desarrollado en Python con Pygame**

Un juego donde el jugador debe navegar por un laberinto, recolectar obsequios y evitar ser capturado por la computadora enemiga. Incluye sistema de puntuación, vidas, sonidos y un Salón de la Fama persistente.

---

## 📂 Estructura del Proyecto

```
coderunner/
│── README.md
│── requirements.txt
│── .gitignore
│── pyproject.toml
│
├── src/                     # Código fuente en Python
│   ├── main.py              # Punto de entrada del juego
│   │
│   ├── mundo/               # Modelos del mundo del juego
│   │   ├── laberinto.py     # Gestión de laberintos y mapas
│   │   ├── obsequio.py      # Items coleccionables
│   │   ├── registro.py      # Registro de puntajes
│   │   └── salon_fama.py    # Persistencia de récords
│   │
│   ├── personajes/          # Entidades del juego
│   │   ├── personaje.py     # Clase base abstracta
│   │   ├── jugador.py       # Personaje controlado por el usuario
│   │   ├── computadora.py   # IA enemiga con pathfinding BFS
│   │   └── sprite_animado.py # Animaciones de sprites
│   │
│   ├── servicios/           # Servicios compartidos
│   │   ├── administrador.py # Gestión administrativa (carga laberintos, etc.)
│   │   └── sistema_sonido.py # Reproductor de audio (singleton)
│   │
│   ├── game/                # Lógica principal del juego
│   │   └── juego.py         # Controlador principal y coordinación
│   │
│   ├── interfaz/            # UI y componentes visuales
│   │   ├── gestor_fuentes.py     # Gestión de fuentes
│   │   ├── paleta_ui.py          # Colores del tema
│   │   ├── componentes/          # Componentes reutilizables
│   │   │   ├── boton_adaptable.py   # Botones con auto-sizing
│   │   │   ├── input_texto.py       # Input de texto
│   │   │   ├── titulo_arcade.py     # Títulos estilo arcade
│   │   │   └── overlay.py           # Overlays y modales
│   │   └── pantallas/            # Pantallas del juego
│   │       ├── menu_principal.py
│   │       ├── pantalla_juego.py
│   │       ├── pantalla_salon_fama.py
│   │       ├── pantalla_administracion.py
│   │       └── ...
│   │
│   ├── jugabilidad/         # Mecánicas de juego
│   │   └── gestores/
│   │       ├── gestor_movimiento.py  # Movimiento y colisiones
│   │       ├── gestor_obsequios.py   # Gestión de obsequios
│   │       └── gestor_dificultad.py  # Dificultad progresiva
│   │
│   ├── config/              # Configuración global
│   │   ├── config.py        # Constantes del juego
│   │   └── colores.py       # Paleta de colores
│   │
│   ├── utilidades/          # Funciones auxiliares
│   │   ├── helpers.py       # Utilidades generales
│   │   └── coordenadas.py   # Conversión píxeles/celdas
│   │
│   ├── data/                # Archivos JSON/TXT para laberintos y puntajes
│   │   ├── laberintos/      # Laberintos del juego
│   │   │   ├── laberinto1.json
│   │   │   ├── laberinto2.json
│   │   │   └── laberinto3.json
│   │   └── salon_fama.json  # Persistencia de puntajes
│   │
│   ├── assets/              # Recursos multimedia
│   │   ├── sonidos/
│   │   │   ├── mover.wav
│   │   │   ├── obsequio.wav
│   │   │   └── captura.wav
│   │   └── imagenes/
│   │       └── pasillos.jpg
│   │
│   └── tests/               # Casos de prueba
│       ├── test_carga_laberintos.py
│       ├── test_mapa_laberinto.py
│       ├── test_menu_navegacion.py
│       ├── test_movimiento_jugador.py
│       ├── test_persecucion_computadora.py
│       ├── test_puntajes_obsequios.py
│       ├── test_salon_fama.py
│       └── test_sistema_vidas.py
│
└── docs/                    # Documentación
    └── Historias de usuario.md
```

---

## ✨ Características

- 🎯 **Sistema de Puntaje**: Gana puntos por moverte y recolectar obsequios
- ❤️ **Sistema de Vidas**: 3 vidas para completar el laberinto
- 🤖 **IA Enemiga**: Pathfinding BFS para persecución inteligente
- 🎨 **Interfaz Arcade**: Estilo retro con componentes pixel art
- 🏆 **Salón de la Fama**: Persistencia de récords
- 🎵 **Efectos de Sonido**: Feedback auditivo inmersivo
- 🔧 **Panel de Administración**: Gestión de laberintos
- 📈 **Dificultad Progresiva**: El juego se vuelve más desafiante con el tiempo
- 🧪 **Tests Automatizados**: Suite completa de pruebas

---

## 🔧 Requisitos

- **Python 3.8+**
- **Pygame 2.0+**
- **pytest** (para testing)

---

## 📥 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/coderunner.git
cd coderunner
```

### 2. Crear entorno virtual (recomendado)

```bash
# En Windows
python -m venv .venv
.venv\Scripts\activate

# En Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 🚀 Ejecución

### Iniciar el juego

```bash
python src/main.py
```

---

## 🎮 Controles

| Tecla | Acción |
|-------|--------|
| `↑` | Mover arriba |
| `↓` | Mover abajo |
| `←` | Mover izquierda |
| `→` | Mover derecha |
| `ESC` | Salir |

---

## 🧪 Testing

### Ejecutar todos los tests

```bash
pytest src/tests/
```

### Ejecutar tests con cobertura

```bash
pytest --cov=src src/tests/
```

---

## 📚 Documentación

- **Historias de Usuario**: [`docs/HU.md`](docs/HU.md)
- **Diagrama UML**: [`docs/uml.pdf`](docs/uml.pdf)
- **Cronograma**: [`docs/cronograma.xlsx`](docs/cronograma.xlsx)
- **Casos de Prueba**: [`docs/casos_prueba.xlsx`](docs/casos_prueba.xlsx)

---

## 👥 Integrantes

- **Paulo Anchía** - C5C482

---

## 📄 Licencia

Este proyecto es de uso académico para el curso de Programación I.




