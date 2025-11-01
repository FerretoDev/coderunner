# Tests del Proyecto - Juego del Laberinto

## Descripción

Este directorio contiene los tests automatizados del proyecto, organizados según las Historias de Usuario (HU-01 a HU-17).

## Estructura de Tests

### Tests de Gameplay
- **test_movimiento_jugador.py** (HU-01): Movimiento básico con teclas de dirección
- **test_persecucion_computadora.py** (HU-02): Algoritmo BFS y persecución
- **test_sistema_vidas.py** (HU-03, HU-04, HU-05): Sistema de vidas y colisiones

### Tests de Mapa
- **test_mapa_laberinto.py** (HU-06, HU-07): Muros y pasillos del laberinto

### Tests de Puntajes
- **test_puntajes_obsequios.py** (HU-08, HU-09, HU-10): Obsequios y sistema de puntos

### Tests de Persistencia
- **test_salon_fama.py** (HU-11, HU-12, HU-13): Guardado y ranking de puntajes

### Tests de Laberintos
- **test_carga_laberintos.py** (HU-14, HU-15): Carga y validación de JSON

### Tests de Interfaz
- **test_menu_navegacion.py** (HU-16, HU-17): Menú principal y navegación

## Ejecutar Tests

### Ejecutar todos los tests:
```bash
cd /home/marcosferreto/Dev/coderunner/src
pytest tests/ -v
```

### Ejecutar un archivo específico:
```bash
pytest tests/test_movimiento_jugador.py -v
```

### Ejecutar tests por categoría:
```bash
# Tests unitarios
pytest tests/ -m unit -v

# Tests de integración
pytest tests/ -m integration -v

# Tests lentos
pytest tests/ -m slow -v
```

### Ver cobertura de código:
```bash
pytest tests/ --cov=models --cov=game --cov-report=html
```

### Ejecutar tests con salida detallada:
```bash
pytest tests/ -vv --tb=short
```
