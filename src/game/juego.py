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

import pygame

from config.constants import (
    PASSWORD,
)  # Motor de eventos, ventana y tiempo para el loop principal [web:47]

# Agregar el directorio 'src' al path para las importaciones relativas absolutas de paquetes internos.
# Esto permite ejecutar el archivo desde distintos lugares sin errores de importación.
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)  # Ajuste de ruta robusto y portátil [web:21]

from interfaz.pantallas import (
    MensajeModal,  # Modal reutilizable para mostrar mensajes (éxito/error)
    MenuPrincipal,  # Menú principal que devuelve la opción elegida
    ModalConfirmacion,  # Modal de confirmación para acciones críticas
    PantallaAdministracion,  # Pantalla que solicita clave para administración
    PantallaCargaLaberinto,  # Pantalla para cargar archivos de laberinto
    PantallaIniciarJuego,  # Pantalla para capturar el nombre del jugador antes de iniciar
    PantallaMenuAdministrador,  # Menú de opciones administrativas
    PantallaSalonFama,  # Pantalla que muestra los mejores puntajes
    PantallaDemoUI,  # Pantalla de demostración de componentes UI pixel art
)
from interfaz.pantallas.pantalla_juego import (
    PantallaJuego,
)  # Pantalla que corre el juego principal (loop propio) [web:47]
from mundo.salon_fama import (
    SalonFama,
)  # Modelo para gestionar puntuaciones y récords [web:21]
from servicios.administrador import (
    Administrador,
)  # Lógica de autenticación de administrador [web:21]
from servicios.sistema_sonido import (
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
        self._jugador = None  # Datos del jugador activo (nombre, puntaje, vidas)
        self._computadora = None  # Placeholder para IA/enemigos si se necesita a futuro
        self._laberinto = None  # Placeholder para el mapa/escenario
        self.sonido = SistemaSonido()  # Gestor de sonidos (cargar/reproducir efectos)
        self.salon_fama = SalonFama()  # Gestor de puntajes para mostrar/guardar récords
        self._estado = "en curso"  # Bandera simple del estado del juego

        # Objetos de Pygame que se inicializan en iniciar()
        self.screen = None  # Se crea la Surface de la ventana al iniciar
        self.clock = (
            pygame.time.Clock()
        )  # Reloj para controlar FPS si se usa un loop aquí

    def iniciar(self):
        """Inicializa Pygame, muestra el menú principal y navega hasta salir."""
        # Inicializar Pygame una sola vez antes de usar display, eventos o fuentes
        pygame.init()  # Prepara módulos internos de Pygame para su uso correcto

        # Obtener información de la pantalla
        info_pantalla = pygame.display.Info()
        ancho_monitor = info_pantalla.current_w
        alto_monitor = info_pantalla.current_h

        # Usar 90% del tamaño del monitor para dejar espacio para barras del sistema
        ancho_ventana = int(ancho_monitor * 0.9)
        alto_ventana = int(alto_monitor * 0.85)

        # Mínimo 800x600 para asegurar usabilidad
        ancho_ventana = max(800, ancho_ventana)
        alto_ventana = max(600, alto_ventana)

        # Crear ventana principal con tamaño adaptable
        screen = pygame.display.set_mode(
            (ancho_ventana, alto_ventana)
        )  # Crea la Surface principal donde se dibuja
        pygame.display.set_caption(
            "Theseus Runner"
        )  # Título visible en la barra de la ventana

        # Instancias de servicios que se comparten entre pantallas
        salon_fama = (
            SalonFama()
        )  # Mantiene los récords accesibles desde el menú y su pantalla
        admin = Administrador(
            PASSWORD
        )  # Admin con clave por defecto “casa” para pruebas|

        # Loop principal de navegación de menús
        ejecutando = (
            True  # Mientras esté en True, se seguirá mostrando el menú principal
        )

        while ejecutando:
            # Asegura las dimensiones y el título del menú cada vez
            # Mantener el tamaño actual de la ventana
            pygame.display.set_caption(
                "Theseus Runner"
            )  # Restituye el título principal si cambió [web:47]

            # Mostrar menú principal y esperar a que el usuario elija
            menu = MenuPrincipal(
                screen
            )  # Crea el menú con la Surface de la ventana actual [web:47]
            opcion = (
                menu.ejecutar()
            )  # Devuelve un número de opción elegido por el usuario [web:21]

            if opcion == 1:  # Iniciar Juego
                self._manejar_iniciar_juego(screen)
            elif opcion == 2:  # Salón de la Fama
                self._manejar_salon_fama(screen, salon_fama)
            elif opcion == 3:  # Administración
                self._manejar_administracion(screen, admin, salon_fama)
            elif opcion == 4:  # Demo UI (Nueva opción)
                self._manejar_demo_ui(screen)
            elif opcion == 5:  # Salir
                ejecutando = self._manejar_salir(screen)

        # Al salir del loop, cerrar Pygame y terminar el proceso de forma limpia
        pygame.quit()  # Libera recursos de Pygame (ventana, audio, etc.) [web:47]
        sys.exit()  # Termina el proceso del programa explícitamente [web:21]

    def _manejar_iniciar_juego(self, screen):
        """Maneja la opción de iniciar juego."""
        pantalla_inicio = PantallaIniciarJuego(screen)
        nombre = pantalla_inicio.ejecutar()

        if nombre:
            pantalla = PantallaJuego(nombre)
            pantalla.ejecutar()

    def _manejar_salon_fama(self, screen, salon_fama):
        """Maneja la opción de Salón de la Fama."""
        # Recargar datos para mostrar los puntajes más recientes
        salon_fama.cargar_datos()
        pantalla_salon = PantallaSalonFama(screen, salon_fama)
        pantalla_salon.ejecutar()

    def _manejar_demo_ui(self, screen):
        """Maneja la opción de Demo UI."""
        from interfaz.pantallas.pantalla_demo_ui import PantallaDemoUI

        pantalla_demo = PantallaDemoUI(screen)
        # Ejecutar loop de la demo
        clock = pygame.time.Clock()
        ejecutando = True

        while ejecutando:
            # Eventos
            eventos = pygame.event.get()
            pantalla_demo.manejar_eventos(eventos)

            # Actualizar
            pantalla_demo.actualizar()

            # Dibujar
            pantalla_demo.dibujar()
            pygame.display.flip()
            clock.tick(60)

            # Verificar salida
            resultado = pantalla_demo.obtener_resultado()
            if resultado:
                ejecutando = False

    def _manejar_administracion(self, screen, admin, salon_fama):
        """Maneja la opción de Administración."""
        pantalla_admin = PantallaAdministracion(screen)
        clave = pantalla_admin.ejecutar()

        if clave and admin.autenticar(clave):
            self._mostrar_menu_administrador(screen, admin, salon_fama)
        elif clave:
            modal = MensajeModal(screen, "Error", "Clave incorrecta", "error")
            modal.ejecutar()

    def _mostrar_menu_administrador(self, screen, admin, salon_fama):
        """Muestra el menú de administrador y maneja sus opciones."""
        en_menu_admin = True
        while en_menu_admin:
            menu_admin = PantallaMenuAdministrador(screen)
            opcion_admin = menu_admin.ejecutar()

            if opcion_admin == 1:  # Cargar Laberinto
                self._manejar_cargar_laberinto(screen, admin)
            elif opcion_admin == 2:  # Reiniciar Salón de Fama
                self._manejar_reiniciar_salon(screen, admin, salon_fama)
            elif opcion_admin == 3:  # Volver
                en_menu_admin = False

    def _manejar_cargar_laberinto(self, screen, admin):
        """Maneja la carga de un laberinto."""
        pantalla_carga = PantallaCargaLaberinto(screen, admin)
        laberinto, mensaje = pantalla_carga.ejecutar()

        if laberinto:
            modal = MensajeModal(screen, "Laberinto Cargado", mensaje, "success")
            modal.ejecutar()
        elif mensaje:
            modal = MensajeModal(screen, "Error", mensaje, "error")
            modal.ejecutar()

    def _manejar_reiniciar_salon(self, screen, admin, salon_fama):
        """Maneja el reinicio del salón de la fama."""
        confirmar = ModalConfirmacion(
            screen,
            "Confirmar Acción",
            "¿Está seguro de que desea\neliminar todos los registros?",
        )
        if confirmar.ejecutar():
            mensaje = admin.reiniciar_salon_fama(salon_fama)
            modal = MensajeModal(screen, "Salón Reiniciado", mensaje, "success")
            modal.ejecutar()

    def _manejar_salir(self, screen):
        """Maneja la confirmación de salida del juego.

        Returns:
            False para salir del loop, True para continuar
        """
        confirmar = ModalConfirmacion(
            screen,
            "Confirmar Salida",
            "¿Está seguro de que desea\nsalir del juego?",
        )
        return not confirmar.ejecutar()
