# Casos de Prueba - Juego del Laberinto

## Información del Proyecto

**Proyecto:** Sistema de Juego de Laberinto con IA  
**Fecha:** 29 de octubre de 2025  
**Responsable:** Equipo de Desarrollo  
**Basado en:** Historias de Usuario (HU-01 a HU-17)

---

## CP-01: Movimiento Básico del Jugador (HU-01)

**Historia de Usuario:** HU-01 - Movimiento básico del jugador

**Descripción:** Verificar que el jugador se mueve correctamente usando las teclas de flecha del teclado, desplazándose una casilla a la vez.

**Precondiciones:**

- El juego está en curso
- El jugador está en una posición válida del laberinto
- El jugador tiene al menos 1 vida

**Pasos:**

1. Iniciar una nueva partida
2. Presionar la tecla FLECHA ARRIBA (↑)
3. Observar que el jugador se desplaza hacia arriba una celda
4. Presionar la tecla FLECHA ABAJO (↓)
5. Observar que el jugador se desplaza hacia abajo una celda
6. Presionar la tecla FLECHA IZQUIERDA (←)
7. Observar que el jugador se desplaza hacia la izquierda una celda
8. Presionar la tecla FLECHA DERECHA (→)
9. Observar que el jugador se desplaza hacia la derecha una celda
10. Intentar moverse hacia una pared

**Resultado Esperado:**

- El jugador se mueve exactamente una celda en la dirección de la flecha presionada
- El movimiento tiene un cooldown de 8 frames (~0.13 segundos) entre movimientos
- El jugador NO atraviesa paredes
- El jugador permanece dentro de los límites del laberinto
- El movimiento es fluido y visualmente claro
- Las teclas WASD también funcionan (W=↑, A=←, S=↓, D=→)

**Estado:** ✅ Pasado

**Responsable Original:** Marcos  
**Complejidad:** Fácil

---

## TC-02: Ingreso de Nombre del Jugador

**Descripción:** Verificar que el sistema permite ingresar el nombre del jugador correctamente.

**Precondiciones:**
- El menú principal está visible
- Se seleccionó la opción "Jugar"

**Pasos:**
1. Desde el menú, seleccionar "Jugar"
2. Ingresar el nombre "TestPlayer" usando el teclado
3. Presionar ENTER para confirmar
4. Observar que se inicia el juego

**Resultado Esperado:**
- Aparece un campo de texto para ingresar el nombre
- Los caracteres ingresados se muestran en pantalla
- El nombre ingresado se usa durante la partida
- El nombre aparece en el HUD del juego
- Al finalizar, el nombre se guarda en el Salón de la Fama

**Estado:** ✅ Pasado

---

## TC-03: Escalado Dinámico del Laberinto

**Descripción:** Verificar que el laberinto se escala y centra correctamente en la pantalla de 1200×800 píxeles.

**Precondiciones:**
- El juego ha iniciado
- Se ha ingresado un nombre de jugador válido

**Pasos:**
1. Iniciar una nueva partida
2. Observar la disposición del laberinto en la pantalla
3. Verificar que el laberinto está centrado
4. Confirmar que todas las celdas son visibles

**Resultado Esperado:**
- El laberinto se muestra centrado en la pantalla
- El tamaño de celda se calcula como `min((1200-40)/16, (800-120)/9)` ≈ 73 píxeles
- Los offsets centran el laberinto: `offset_x` y `offset_y` calculados correctamente
- No hay celdas cortadas ni fuera de la pantalla
- El área de juego utiliza eficientemente el espacio disponible

**Estado:** ✅ Pasado

---

## TC-04: Movimiento del Jugador con Teclas de Dirección

**Descripción:** Verificar que el jugador se mueve correctamente usando las flechas del teclado.

**Precondiciones:**
- El juego está en curso
- El jugador está en una posición válida del laberinto

**Pasos:**
1. Presionar la tecla FLECHA ARRIBA
2. Presionar la tecla FLECHA ABAJO
3. Presionar la tecla FLECHA IZQUIERDA
4. Presionar la tecla FLECHA DERECHA
5. Intentar moverse hacia una pared

**Resultado Esperado:**
- El jugador se mueve una celda en la dirección presionada
- El movimiento tiene un cooldown de 8 frames (0.13 segundos a 60 FPS)
- El jugador NO atraviesa paredes
- El jugador permanece dentro de los límites del laberinto
- El movimiento es fluido y por celdas completas

**Estado:** ✅ Pasado

---

## TC-05: Movimiento del Jugador con Teclas WASD

**Descripción:** Verificar que el jugador se mueve correctamente usando las teclas WASD.

**Precondiciones:**
- El juego está en curso
- El jugador está en una posición válida del laberinto

**Pasos:**
1. Presionar la tecla W (arriba)
2. Presionar la tecla S (abajo)
3. Presionar la tecla A (izquierda)
4. Presionar la tecla D (derecha)
5. Verificar que funciona igual que las flechas

**Resultado Esperado:**
- Las teclas WASD producen el mismo comportamiento que las flechas
- W = Arriba, S = Abajo, A = Izquierda, D = Derecha
- El cooldown de movimiento se aplica igualmente
- No se permiten movimientos diagonales

**Estado:** ✅ Pasado

---

## TC-06: Inteligencia Artificial del Enemigo (BFS)

**Descripción:** Verificar que el enemigo persigue al jugador usando el algoritmo BFS correctamente.

**Precondiciones:**
- El juego está en curso
- El enemigo y el jugador están en posiciones diferentes

**Pasos:**
1. Observar la posición inicial del enemigo
2. Mover al jugador a diferentes posiciones
3. Observar el comportamiento del enemigo
4. Verificar que el enemigo calcula rutas óptimas
5. Confirmar que el enemigo no atraviesa paredes

**Resultado Esperado:**
- El enemigo calcula la ruta más corta usando BFS (Breadth-First Search)
- El enemigo se mueve hacia el jugador siguiendo la ruta calculada
- El enemigo respeta las paredes del laberinto
- La velocidad inicial del enemigo es 1.5 píxeles/frame
- El enemigo actualiza su ruta cuando el jugador se mueve

**Estado:** ✅ Pasado

---

## TC-07: Recolección de Obsequios

**Descripción:** Verificar que el jugador puede recolectar obsequios y recibir los puntos correspondientes.

**Precondiciones:**
- El juego está en curso
- Hay un obsequio visible en el laberinto

**Pasos:**
1. Localizar un obsequio en el laberinto
2. Mover al jugador hacia la posición del obsequio
3. Verificar que el obsequio desaparece al hacer contacto
4. Observar el incremento del puntaje
5. Confirmar que aparece un nuevo obsequio

**Resultado Esperado:**
- Al acercarse al obsequio (distancia < radio * 1.8), se recolecta
- El puntaje aumenta en 10 puntos
- El obsequio desaparece del laberinto
- Inmediatamente aparece un nuevo obsequio en una posición aleatoria válida
- El nuevo obsequio no aparece en paredes ni en la posición del jugador/enemigo

**Estado:** ✅ Pasado

---

## TC-08: Temporizador de Obsequios

**Descripción:** Verificar que los obsequios tienen un tiempo de vida limitado y se reposicionan automáticamente.

**Precondiciones:**
- El juego está en curso
- Hay un obsequio visible en el laberinto

**Pasos:**
1. Observar la posición de un obsequio
2. Esperar sin recogerlo durante 10 segundos
3. Verificar que el obsequio desaparece
4. Confirmar que aparece un nuevo obsequio en otra posición
5. Repetir el proceso para verificar consistencia

**Resultado Esperado:**
- Cada obsequio tiene una vida de 600 frames (10 segundos a 60 FPS)
- Al cumplirse el tiempo, el obsequio desaparece
- Inmediatamente aparece uno nuevo en posición aleatoria válida
- El temporizador se reinicia para el nuevo obsequio
- El sistema mantiene siempre un obsequio activo en el juego

**Estado:** ✅ Pasado

---

## TC-09: Dificultad Progresiva

**Descripción:** Verificar que la velocidad del enemigo aumenta progresivamente cada 10 segundos.

**Precondiciones:**
- El juego está en curso
- El enemigo tiene velocidad inicial de 1.5

**Pasos:**
1. Observar la velocidad inicial del enemigo
2. Esperar 10 segundos de juego
3. Verificar que la velocidad ha aumentado
4. Continuar jugando y verificar incrementos cada 10 segundos
5. Observar el valor de velocidad en el HUD

**Resultado Esperado:**
- Velocidad inicial: 1.5 píxeles/frame
- Cada 600 frames (10 segundos), la velocidad aumenta en 0.2
- Después de 10s: velocidad = 1.7
- Después de 20s: velocidad = 1.9
- Después de 30s: velocidad = 2.1
- El incremento es continuo sin límite superior
- La velocidad se muestra correctamente en el HUD

**Estado:** ✅ Pasado

---

## TC-10: Sistema de Vidas

**Descripción:** Verificar que el sistema de vidas funciona correctamente y termina el juego al llegar a cero.

**Precondiciones:**
- El juego está en curso
- El jugador tiene 3 vidas al inicio

**Pasos:**
1. Verificar que el HUD muestra 3 corazones al iniciar
2. Permitir que el enemigo alcance al jugador
3. Observar que se pierde una vida
4. Verificar que el HUD muestra 2 corazones
5. Repetir hasta perder todas las vidas

**Resultado Esperado:**
- El jugador inicia con 3 vidas (3 corazones en el HUD)
- Al ser alcanzado por el enemigo, se pierde 1 vida
- El HUD actualiza el número de corazones visualmente
- Cuando las vidas llegan a 0, el juego termina
- Se muestra la pantalla de "Game Over"

**Estado:** ✅ Pasado

---

## TC-11: Interfaz Gráfica del HUD

**Descripción:** Verificar que el HUD muestra correctamente todos los elementos: vidas, puntaje y velocidad.

**Precondiciones:**
- El juego está en curso

**Pasos:**
1. Observar la parte superior de la pantalla
2. Verificar los iconos de corazones (vidas)
3. Verificar el icono de estrella y puntaje
4. Verificar el texto de velocidad del enemigo
5. Recolectar obsequios y perder vidas para ver actualizaciones

**Resultado Esperado:**
- Se muestran corazones gráficos (círculos rojos + triángulo) en lugar de "❤"
- Se muestra una estrella gráfica (polígono de 10 puntas amarillo) en lugar de "★"
- El puntaje se muestra junto a la estrella
- La velocidad se muestra con formato: "Velocidad: X.X"
- Todos los elementos se actualizan en tiempo real
- Los gráficos pulsan con animación matemática (sin)

**Estado:** ✅ Pasado

---

## TC-12: Pantalla de Game Over

**Descripción:** Verificar que la pantalla de Game Over se muestra correctamente con toda la información.

**Precondiciones:**
- El jugador ha perdido todas sus vidas

**Pasos:**
1. Perder todas las vidas en el juego
2. Observar la pantalla de Game Over
3. Verificar la información mostrada
4. Esperar 5 segundos
5. Intentar presionar ESC antes y después de los 5 segundos

**Resultado Esperado:**
- Se muestra "GAME OVER" en grande
- Se muestra el nombre del jugador
- Se muestra el puntaje final
- Se muestra la velocidad alcanzada del enemigo (formato: velocidad / 1.5)
- Aparece un contador regresivo de 5 segundos
- Durante el conteo, no se puede salir con ESC
- Después de 5 segundos, se puede presionar ESC para volver al menú
- Los datos se guardan automáticamente en el Salón de la Fama

**Estado:** ✅ Pasado

---

## TC-13: Salón de la Fama - Guardado

**Descripción:** Verificar que los registros se guardan correctamente en el Salón de la Fama.

**Precondiciones:**
- Se ha completado al menos una partida

**Pasos:**
1. Completar una partida con nombre "TestPlayer1" y puntaje 50
2. Llegar a Game Over
3. Esperar 5 segundos y presionar ESC
4. Desde el menú, seleccionar "Salón de la Fama"
5. Verificar que aparece el registro

**Resultado Esperado:**
- El registro se crea con: nombre del jugador, puntaje y laberinto jugado
- El registro se guarda automáticamente al terminar la partida
- El registro persiste entre ejecuciones del juego
- Los registros se ordenan por puntaje (mayor a menor)
- Se pueden almacenar múltiples registros de diferentes jugadores

**Estado:** ✅ Pasado

---

## TC-14: Salón de la Fama - Visualización

**Descripción:** Verificar que el Salón de la Fama muestra correctamente los mejores puntajes.

**Precondiciones:**
- Existen al menos 3 registros guardados en el Salón de la Fama

**Pasos:**
1. Desde el menú principal, seleccionar "Salón de la Fama"
2. Observar la lista de registros
3. Verificar el orden de los puntajes
4. Verificar la información mostrada para cada registro
5. Presionar ESC para volver al menú

**Resultado Esperado:**
- Se muestra la lista de registros ordenados de mayor a menor puntaje
- Cada registro muestra: posición, nombre del jugador y puntaje
- La interfaz es clara y legible
- Se pueden visualizar múltiples registros (scroll si hay muchos)
- Presionar ESC regresa al menú principal

**Estado:** ✅ Pasado

---

## TC-15: Funcionalidad de Pausa con ESC

**Descripción:** Verificar que el juego se puede pausar y reanudar correctamente con la tecla ESC.

**Precondiciones:**
- El juego está en curso
- El jugador está jugando activamente

**Pasos:**
1. Durante el juego, presionar la tecla ESC
2. Observar que el juego regresa al menú principal
3. Verificar que la partida no se guarda
4. Iniciar una nueva partida desde el menú
5. Confirmar que es una partida nueva

**Resultado Esperado:**
- Al presionar ESC durante el juego, se regresa inmediatamente al menú
- No se ejecuta pygame.quit() que causaría un cierre del programa
- La pantalla cambia de 1200×800 a 800×600 (tamaño del menú)
- La partida actual se descarta (no se guarda)
- El jugador puede iniciar una nueva partida desde el menú
- Durante Game Over, ESC solo funciona después de 5 segundos

**Estado:** ✅ Pasado

---

## Resumen de Resultados

| Estado | Cantidad | Porcentaje |
|--------|----------|------------|
| ✅ Pasado | 15 | 100% |
| ❌ Fallado | 0 | 0% |
| ⏸️ Pendiente | 0 | 0% |

**Total de Casos de Prueba:** 15  
**Cobertura Funcional:** 100%

---

## Observaciones Generales

1. **Escalado y Centrado:** El sistema de offsets dinámicos funciona perfectamente para adaptar el laberinto a la pantalla.

2. **Inteligencia Artificial:** El algoritmo BFS proporciona un comportamiento inteligente y desafiante para el enemigo.

3. **Dificultad Progresiva:** El sistema de incremento de velocidad mantiene el juego interesante a medida que avanza el tiempo.

4. **Interfaz Gráfica:** Los elementos gráficos (corazones y estrella) mejoran significativamente la presentación visual comparado con símbolos Unicode.

5. **Controles:** La implementación de controles duales (flechas + WASD) mejora la accesibilidad del juego.

6. **Persistencia:** El Salón de la Fama guarda correctamente los registros permitiendo competencia entre jugadores.

7. **Experiencia de Usuario:** El temporizador de 5 segundos en Game Over da tiempo suficiente para leer los resultados.

8. **Robustez:** El juego maneja correctamente transiciones entre pantallas sin crashes.

---

## Anexo: Características Técnicas Implementadas

### Sistema de Coordenadas
- **Píxeles a Celdas:** `col = int((x - offset_x) // tam_celda)`
- **Celdas a Píxeles:** `x_center = (col * tam_celda) + offset_x + (tam_celda // 2)`

### Algoritmo BFS
```python
def _calcular_camino_bfs(mapa, start, goal):
    # Usa deque para cola FIFO
    # Explora vecinos en 4 direcciones
    # Retorna camino más corto
```

### Temporizadores (60 FPS)
- Cooldown movimiento: 8 frames (≈ 0.13s)
- Vida obsequio: 600 frames (10s)
- Incremento velocidad: 600 frames (10s)
- Espera Game Over: 300 frames (5s)

### Fórmula de Velocidad Mostrada
```python
velocidad_relativa = velocidad_actual / velocidad_inicial_enemigo
```

---

**Fecha de Creación:** 29 de octubre de 2025  
**Última Actualización:** 29 de octubre de 2025  
**Responsable de Testing:** Equipo de QA
