Historias de usuario 

Sección 1: Gameplay 

HU-01: Movimiento básico del jugador 

    Historia: Como jugador, quiero moverme con las flechas, para recorrer el laberinto. 

    Descripción: El jugador se mueve una casilla por vez usando las teclas ↑ ↓ ← →.  

    Complejidad: Fácil 

    Esfuerzo estimado: 2 horas 

    Responsable: Marcos 

    Caso de prueba: CP-01: Al presionar ↑ el jugador deberá desplazarse hacia arriba, al presionar ↓ el jugador deberá desplazarse hacia abajo, al presionar ← el jugador deberá desplazarse hacia la izquierda y al presionar → el jugador deberá desplazarse hacia la derecha. 

    Estado: Pendiente 

HU-02: Persecución de la computadora 

    Historia: Como jugador, quiero que la computadora me persiga, para que el juego sea desafiante. 

    Descripción: La computadora persigue al jugador moviéndose, 10% más rápido. 

    Complejidad: No compleja 

    Esfuerzo estimado: 6 horas 

    Responsable: Paulo 

    Caso de prueba: CP-02: La computadora sigue correctamente al jugador, recorriendo la misma distancia en menor tiempo que el jugador. 

    Estado: Pendiente 

 
HU-03: Mostrar vidas restantes 

    Historia: Como jugador, quiero ver cuántas vidas me quedan, para saber cuánto me falta para perder. 

    Descripción: Mostrar en pantalla el número de vidas que le quedan al jugador. 

    Complejidad: Fácil 

    Esfuerzo estimado: 1 hora 

    Responsable: Marcos 

    Caso de prueba: CP-03: Se muestran “Vidas: 3” en pantalla. 

    Estado: Pendiente 

HU-04: Pérdida de vida al ser atrapado 

    Historia: Como jugador, quiero perder una vida si me atrapan, para que el juego tenga un límite. 

    Descripción: Si la computadora toca al jugador, este pierde una vida. 

    Complejidad: No compleja 

    Esfuerzo estimado: 3 horas 

    Responsable: Juan 

    Caso de prueba: CP-04: Si hay colisión entre la computadora y el jugador, se resta una vida al jugador. 

    Estado: Pendiente 

HU-05: Fin de partida al perder todas las vidas 

    Historia: Como jugador, quiero que el juego termine al perder todas las vidas, para cerrar la partida. 

    Descripción: Si las vidas llegan a 0, mostrar mensaje de derrota. 

    Complejidad: Fácil 

    Esfuerzo estimado: 2 horas 

    Responsable: Sebastián  

    Caso de prueba: CP-05: Con vidas = 0, el juego termina automáticamente. 

    Estado: Pendiente 

Sección 2: Mapa 

HU - 06: Muros para el mapa 

    Estructura: Como jugador, quiero que el laberinto tenga muros, para limitar los movimientos. 

    Descripción: Deben existir muros que restringen movimiento del jugador y de la computadora. 

    Complejidad: No compleja 

    Esfuerzo: 4 horas 

    Responsable: Marcos 

    Caso de prueba: CP-06: El jugador o la computadora no podrá traspasar ningún muro establecido. 

    Estado: Pendiente 

HU – 07: Pasillos para el mapa 

    Estructura: Como jugador, quiero que existan pasillos en el labertino, para que tanto la computadora como el jugador puedan desplazarse. 

    Descripción: Deben existir pasillos por los cuales el jugador y la computadora se puedan desplazar. 

    Complejidad: Fácil 

    Esfuerzo: 3 horas 

    Responsable: Juan 

    Caso de prueba: CP-07: El jugador o la computadora solamente podrán desplazarse por los pasillos. 

    Estado: Pendiente 

Sección 3: Puntajes y obsequios 

HU-08: Sumar puntos por movimiento 

    Historia: Como jugador, quiero sumar puntos por cada paso, para medir mi avance. 

    Descripción: Cada movimiento válido suma +1 punto al puntaje total. 

    Complejidad: Fácil 

    Esfuerzo estimado: 1 hora 

    Responsable: Paulo 

    Caso de prueba: CP-08: Al moverse, mi puntaje aumenta en 1. 

    Estado: Pendiente 

HU-09: Puntos extra por obsequios 

    Historia: Como jugador, quiero recoger obsequios y ganar puntos extra, para tener incentivos. 

    Descripción: Al tocar un obsequio, sumar +10 puntos y reproducir sonido especial. 

    Complejidad: No compleja 

    Esfuerzo estimado: 3 horas 

    Responsable: Juan 

    Caso de prueba: CP-09: Recoger obsequio aumenta puntaje en 10. 

    Estado: Pendiente 

HU-10: Mostrar puntaje actual 

    Historia: Como jugador, quiero ver mi puntaje actual, para saber cómo voy. 

    Descripción: Mostrar el puntaje actual en pantalla en tiempo real. 

    Complejidad: Fácil 

    Esfuerzo estimado: 1 hora 

    Responsable: Sebastián 

    Caso de prueba: CP-10: El puntaje se actualiza en tiempo real mientras juego. 

    Estado: Pendiente 

 

Sección 4: Persistencia 

HU-11: Guardar puntaje en el salón de la fama 

    Historia: Como jugador, quiero guardar mi puntaje en el salón de la fama, para competir con otros. 

    Descripción: Al terminar una partida, guardar nombre y puntaje en archivo JSON persistente. 

    Complejidad: No compleja 

    Esfuerzo estimado: 4 horas 

    Responsable: Paulo 

    Caso de prueba: CP-11: Tras partida, puntaje aparece en archivo. 

    Estado: Pendiente 

HU-12: Ver ranking del salón de la fama 

    Historia: Como jugador, quiero ver el ranking del salón de la fama, para comparar mis resultados. 

    Descripción: Mostrar puntajes guardados en orden descendente desde archivo JSON. 

    Complejidad: No compleja 

    Esfuerzo estimado: 3 horas 

    Responsable: Juan 

    Caso de prueba: CP-12: Ranking ordenado por puntaje correctamente. 

    Estado: Pendiente 

HU-13: Reiniciar el salón de la fama 

    Historia: Como administrador, quiero reiniciar el salón de la fama, para empezar desde cero. 

    Descripción: Opción de borrar todos los puntajes guardados con confirmación. 

    Complejidad: Fácil 

    Esfuerzo estimado: 2 horas 

    Responsable: Sebastián 

    Caso de prueba: CP-13: Tras confirmar, ranking queda vacío. 

    Estado: Pendiente 

 

 

 

Sección 5: Laberinto 

HU-14: Cargar laberinto desde archivo JSON 

    Historia: Como administrador, quiero cargar laberintos desde un archivo JSON, para cambiar el mapa. 

    Descripción: Permitir seleccionar archivo desde explorador e importar datos del laberinto. 

    Complejidad: Compleja 

    Esfuerzo estimado: 3 horas 

    Responsable: Marcos 

    Caso de prueba: CP-14: Archivo cargado y mapa generado correctamente. 

    Estado: Pendiente 

HU-15: Validar archivo de laberinto 

    Historia: Como administrador, quiero validar que el archivo tenga la estructura correcta, para evitar errores. 

    Descripción: Revisar que el JSON incluya posición inicial del jugador, computadora, muros y obsequios. 

    Complejidad: No compleja 

    Esfuerzo estimado: 4 horas 

    Responsable: Paulo 

    Caso de prueba: CP-15: Archivo incorrecto → mensaje de error. 

    Estado: Pendiente 

Sección 6: Interfaz y navegación 

HU-16: Menú principal del juego 

    Historia: Como jugador, quiero un menú principal claro, para navegar fácilmente. 

    Descripción: Pantalla inicial con botones: Iniciar, Salón de la Fama, Administración, Salir. 

    Complejidad: No compleja 

    Esfuerzo estimado: 5 horas 

    Responsable: Marcos 

    Caso de prueba: CP-16: Menú carga correctamente al iniciar. 

    Estado: Pendiente 

 

HU-17: Confirmación al salir 

    Historia: Como jugador, quiero confirmar antes de salir, para no cerrar por accidente. 

    Descripción: Mostrar mensaje “¿Seguro que desea salir?” al presionar salir. 

    Complejidad: Fácil 

    Esfuerzo estimado: 1 hora 

    Responsable: Sebastián 

    Caso de prueba: CP-17: Al intentar salir, aparece confirmación. 

    Estado: Pendiente 

 

 

 

 

 

 

 

 

 

 

 

 