# 📂 Estructura recomendada de GitHub

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

# 📌 Explicación de la estructura

### 1. **Carpeta `src/models/`**

Contiene las **clases del UML** que subiste:

* `Personaje` (abstracta, base de Jugador y Computadora).
* `Jugador` (nombre, vidas, puntaje).
* `Computadora` (velocidad 1.1, perseguir jugador).
* `Administrador` (clave, carga laberinto, reinicia salón).
* `Laberinto` (muros, pasillos, obsequios, cargar desde archivo).
* `Obsequio` (posición, valor=10, método recolectar).
* `SalonFama` (guardar puntajes en JSON).
* `Registro` (nombre, puntaje, laberinto).
* `SistemaSonido` (mover, obsequio, captura).

👉 Cada clase va en su archivo `.py` para mantener orden.

---

### 2. **Carpeta `src/game/`**

Contiene la **lógica del juego**:

* `juego.py`: clase `Juego` (inicia, actualizar, mostrar estado, terminar, salir).
* `motor.py`: ciclo principal de `pygame` (eventos, render, update).
* `interfaz.py`: menús y pantallas (Tkinter o Pygame).

---

### 3. **Carpeta `src/data/`**

* Archivos `.json` o `.txt` con mapas de laberinto.
* Archivo `salon_fama.json` para puntajes guardados.

---

### 4. **Carpeta `src/tests/`**

* Archivos de **unittest o pytest** para probar cada módulo.
* Ejemplo: `test_jugador.py` prueba `mover`, `perder_vida`, `sumar_puntos`.

---

### 5. **Carpeta `docs/`**

* Las **Historias de Usuario** (HU.md).
* **UML** (el PDF que ya hiciste).
* **Cronograma** en Excel.
* **Casos de prueba** documentados.
* **Prototipo UI** (captura de Canva, Figma o Paint).

---

### 6. **Carpeta `assets/`**

* Sonidos (wav, mp3).
* Imágenes (íconos, fondos, prototipos).

---

# 📑 Archivos raíz

### `README.md`

Explica el proyecto (ya te lo armé antes, lo podés reutilizar).

### `requirements.txt`

Dependencias del proyecto (mínimo):

```
pygame
pytest
```

### `.gitignore`

Ignorar carpetas innecesarias:

```
__pycache__/
*.pyc
.venv/
.env
```


### `Integrantes`