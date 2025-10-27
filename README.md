# 🎮 CodeRunner

**Juego educativo de laberinto desarrollado en Python con Pygame**

Un juego donde el jugador debe navegar por un laberinto, recolectar obsequios y evitar ser capturado por la computadora enemiga. Incluye sistema de puntuación, vidas, sonidos y un Salón de la Fama persistente.

---

## 📂 Estructura del Proyecto

```
coderunner/
│── README.md
│── requirements.txt
│── .gitignore
│
├── src/                     # Código fuente en Python
│   ├── main.py              # Punto de entrada del juego
│   │
│   ├── models/              # Clases del UML
│   │   ├── personaje.py
│   │   ├── jugador.py
│   │   ├── computadora.py
│   │   ├── administrador.py
│   │   ├── laberinto.py
│   │   ├── obsequio.py
│   │   ├── salon_fama.py
│   │   ├── registro.py
│   │   └── sistema_sonido.py
│   │
│   ├── game/                # Lógica principal del juego
│   │   ├── juego.py
│   │   ├── motor.py         # ciclo principal (pygame loop)
│   │   └── interfaz.py      # menús, pantallas, interacción
│   │
│   ├── data/                # Archivos JSON/TXT para laberintos y puntajes
│   │   ├── laberinto1.json
│   │   ├── laberinto_demo.txt
│   │   └── salon_fama.json
│   │
│   └── tests/               # Casos de prueba
│       ├── test_jugador.py
│       ├── test_computadora.py
│       ├── test_laberinto.py
│       ├── test_salon_fama.py
│       └── test_integration.py
│
├── docs/                    # Documentación
│   ├── HU.md                # Historias de Usuario (las 15 que hicimos)
│   ├── uml.pdf              # Diagrama UML
│   ├── cronograma.xlsx
│   ├── casos_prueba.xlsx
│   └── prototipo_ui.png
│
└── assets/                  # Recursos multimedia
    ├── sonidos/
    │   ├── mover.wav
    │   ├── obsequio.wav
    │   └── captura.wav
    └── imagenes/
        ├── menu.png
        └── icono.png
```

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




