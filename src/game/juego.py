"""
Punto de entrada de la app: crea la ventana, muestra menús y navega entre pantallas.

Responsabilidades:
- Preparar el entorno de importación (sys.path) para ejecutar desde distintos contextos.
- Inicializar Pygame y crear la ventana principal.
- Mostrar el menú principal y, según la opción, abrir las pantallas correspondientes.
- Salir de forma limpia al terminar.
"""

import os  # Manejo de rutas para construir paths portables al sistema operativo [web:21]
import sys  # Permite modificar sys.path y cerrar la app con sys.exit() [web:21]

import pygame  # Motor de eventos, ventana y tiempo para el loop principal [web:47]

# Agregar el directorio 'src' al path para las importaciones relativas absolutas de paquetes internos.
# Esto permite ejecutar el archivo desde distintos lugares sin errores de importación.
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)  # Ajuste de ruta robusto y portátil [web:21]

from game.interfaz import (
    MensajeModal,  # Modal reutilizable para mostrar mensajes (éxito/error) [web:21]
    MenuPrincipal,  # Menú principal que devuelve la opción elegida [web:21]
    PantallaAdministracion,  # Pantalla que solicita clave para administración [web:21]
    PantallaIniciarJuego,  # Pantalla para capturar el nombre del jugador antes de iniciar [web:21]
    PantallaSalonFama,  # Pantalla que muestra los mejores puntajes [web:21]
)
from game.pantalla_juego import (
    PantallaJuego,
)  # Pantalla que corre el juego principal (loop propio) [web:47]
from models.administrador import (
    Administrador,
)  # Lógica de autenticación de administrador [web:21]
from models.salon_fama import (
    SalonFama,
)  # Modelo para gestionar puntuaciones y récords [web:21]
from models.sistema_sonido import (
    SistemaSonido,
)  # Sistema centralizado de sonidos [web:47]


class Juego:
    """
    Clase que maneja la lógica principal del juego.

    - Orquesta la navegación entre pantallas.
    - Inicializa Pygame y administra el ciclo de vida de la app.
    - Gestiona recursos globales como sonido y salón de la fama.
    """

    def __init__(self):
        # Estado general y servicios del juego
        self._jugador = None  # Datos del jugador activo (nombre, puntaje, vidas), si aplica [web:21]
        self._computadora = (
            None  # Placeholder para IA/enemigos si se necesita a futuro [web:21]
        )
        self._laberinto = None  # Placeholder para el mapa/escenario [web:21]
        self.sonido = (
            SistemaSonido()
        )  # Gestor de sonidos (cargar/reproducir efectos) [web:47]
        self.salon_fama = (
            SalonFama()
        )  # Gestor de puntajes para mostrar/guardar récords [web:21]
        self._estado = "en curso"  # Bandera simple del estado del juego [web:21]

        # Objetos de Pygame que se inicializan en iniciar()
        self.screen = None  # Se crea la Surface de la ventana al iniciar [web:47]
        self.clock = (
            pygame.time.Clock()
        )  # Reloj para controlar FPS si se usa un loop aquí [web:47]

    def iniciar(self):
        """Inicializa Pygame, muestra el menú principal y navega hasta salir."""
        # Inicializar Pygame una sola vez antes de usar display, eventos o fuentes
        pygame.init()  # Prepara módulos internos de Pygame para su uso correcto [web:47]

        # Crear ventana principal con tamaño fijo de 800x600 y título
        screen = pygame.display.set_mode(
            (800, 600)
        )  # Crea la Surface principal donde se dibuja [web:47]
        pygame.display.set_caption(
            "CodeRunner"
        )  # Título visible en la barra de la ventana [web:47]

        # Instancias de servicios que se comparten entre pantallas
        salon_fama = (
            SalonFama()
        )  # Mantiene los récords accesibles desde el menú y su pantalla [web:21]
        admin = Administrador(
            "casa"
        )  # Admin con clave por defecto “casa” para pruebas [web:21]

        # Loop principal de navegación de menús
        ejecutando = True  # Mientras esté en True, se seguirá mostrando el menú principal [web:47]

        while ejecutando:
            # Asegura las dimensiones y el título del menú cada vez
            screen = pygame.display.set_mode(
                (800, 600)
            )  # Útil si otras pantallas modifican la ventana [web:47]
            pygame.display.set_caption(
                "CodeRunner"
            )  # Restituye el título principal si cambió [web:47]

            # Mostrar menú principal y esperar a que el usuario elija
            menu = MenuPrincipal(
                screen
            )  # Crea el menú con la Surface de la ventana actual [web:47]
            opcion = (
                menu.ejecutar()
            )  # Devuelve un número de opción elegido por el usuario [web:21]

            if opcion == 1:  # Iniciar Juego
                pantalla_inicio = PantallaIniciarJuego(
                    screen
                )  # Pantalla para pedir el nombre del jugador [web:21]
                nombre = (
                    pantalla_inicio.ejecutar()
                )  # Devuelve el nombre o None si canceló [web:21]

                if nombre:
                    # Inicia el juego principal con el nombre ingresado
                    pantalla = PantallaJuego(
                        nombre
                    )  # Pantalla del juego con su propio loop interno [web:47]
                    pantalla.ejecutar()  # Corre hasta que termine esa pantalla (regresa al menú) [web:47]

            elif opcion == 2:  # Salón de la Fama
                pantalla_salon = PantallaSalonFama(
                    screen, salon_fama
                )  # Pasamos el gestor para leer datos [web:21]
                pantalla_salon.ejecutar()  # Muestra la tabla de récords y vuelve al menú al cerrar [web:21]

            elif opcion == 3:  # Administración
                pantalla_admin = PantallaAdministracion(
                    screen
                )  # Pantalla que pide la clave al usuario [web:21]
                clave = (
                    pantalla_admin.ejecutar()
                )  # Devuelve la clave ingresada o None si canceló [web:21]

                if clave and admin.autenticar(
                    clave
                ):  # Verifica credenciales de admin [web:21]
                    modal = MensajeModal(
                        screen,
                        "✅ Acceso Concedido",
                        "Bienvenido Administrador",
                        "success",
                    )  # Muestra confirmación de acceso [web:21]
                    modal.ejecutar()  # Espera a que el usuario cierre el modal [web:21]
                    # TODO: Aquí irá el panel de administración cuando esté listo [web:21]
                elif clave:
                    modal = MensajeModal(
                        screen, "Error", "Clave incorrecta", "error"
                    )  # Muestra error por clave inválida [web:21]
                    modal.ejecutar()  # Espera a que el usuario cierre el modal [web:21]

            elif opcion == 4:  # Salir
                ejecutando = (
                    False  # Sale del loop principal y cierra la aplicación [web:47]
                )

        # Al salir del loop, cerrar Pygame y terminar el proceso de forma limpia
        pygame.quit()  # Libera recursos de Pygame (ventana, audio, etc.) [web:47]
        sys.exit()  # Termina el proceso del programa explícitamente [web:21]

        # Código de finalización adicional si se necesitara en el futuro
        self.terminar()  # Llamado no alcanzable tras sys.exit, se deja por claridad de intención [web:21]

    def actualizar(self):
        """Cada ciclo: mover enemigo, colisiones y puntaje (pendiente de implementar)."""
        pass  # La lógica de juego frame a frame se delega a PantallaJuego en este diseño [web:47]

    def mostrar_estado(self):
        """Muestra en consola el estado del jugador si existe (diagnóstico rápido)."""
        if self._jugador:  # Evita errores si aún no hay jugador activo [web:21]
            print(
                f"Jugador: {self._jugador['nombre']}"
            )  # Nombre del jugador para seguimiento [web:21]
            print(f"Puntaje: {self._jugador['puntaje']}")  # Puntos actuales [web:21]
            print(f"Vidas: {self._jugador['vidas']}")  # Vidas restantes [web:21]

    def terminar(self):
        """Cierra el juego y, si existe jugador, muestra su puntaje final en consola."""
        print(
            "🎮 Juego terminado"
        )  # Mensaje de cierre para indicar final del ciclo [web:21]
        if self._jugador:  # Muestra puntaje final si corresponde [web:21]
            print(
                f"Puntaje final: {self._jugador['puntaje']}"
            )  # Diagnóstico final [web:21]
        pygame.quit()  # Garantiza liberación de recursos si se llama fuera del flujo normal [web:47]

    def salir(self):
        """Cierre ordenado de la aplicación usando la misma ruta de 'terminar'."""
        self.terminar()  # Punto único para centralizar la lógica de salida [web:21]
