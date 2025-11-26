"""
Punto de entrada de la app: crea la ventana, muestra menús y navega entre pantallas.

Responsabilidades:
- Preparar el entorno de importación (sys.path) para ejecutar desde distintos contextos.
- Inicializar Pygame y crear la ventana principal.
- Mostrar el menú principal y, según la opción, abrir las pantallas correspondientes.
- Salir de forma limpia al terminar.
"""

import os  # Manejo de rutas para construir paths portables al sistema operativo
import sys  # Permite modificar sys.path y cerrar la app con sys.exit()

import pygame

from config.constants import (  # Motor de eventos, ventana y tiempo para el loop principal
    PASSWORD,
)

# Agregar el directorio 'src' al path para las importaciones relativas absolutas de paquetes internos.
# Esto permite ejecutar el archivo desde distintos lugares sin errores de importación.
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)  # Ajuste de ruta robusto y portátil

from interfaz.pantallas import (
    MensajeModal,  # Modal reutilizable para mostrar mensajes (éxito/error)
)
from interfaz.pantallas import (
    MenuPrincipal,  # Menú principal que devuelve la opción elegida
)
from interfaz.pantallas import (
    ModalConfirmacion,  # Modal de confirmación para acciones críticas
)
from interfaz.pantallas import (
    PantallaAdministracion,  # Pantalla que solicita clave para administración
)
from interfaz.pantallas import (
    PantallaCargaLaberinto,  # Pantalla para cargar archivos de laberinto
)
from interfaz.pantallas import (
    PantallaIniciarJuego,  # Pantalla para capturar el nombre del jugador antes de iniciar
)
from interfaz.pantallas import (
    PantallaMenuAdministrador,  # Menú de opciones administrativas
)
from interfaz.pantallas import (
    PantallaSalonFama,  # Pantalla que muestra los mejores puntajes
)
from interfaz.pantallas.pantalla_juego import (  # Pantalla que corre el juego principal (loop propio)
    PantallaJuego,
)
from mundo.salon_fama import SalonFama  # Modelo para gestionar puntuaciones y récords
from servicios.administrador import (  # Lógica de autenticación de administrador
    Administrador,
)
from servicios.sistema_sonido import SistemaSonido  # Sistema centralizado de sonidos


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
            )  # Restituye el título principal si cambió

            # Mostrar menú principal y esperar a que el usuario elija
            menu = MenuPrincipal(
                screen
            )  # Crea el menú con la Surface de la ventana actual
            opcion = (
                menu.ejecutar()
            )  # Devuelve un número de opción elegido por el usuario

            if opcion == 1:  # Iniciar Juego
                self._manejar_iniciar_juego(screen, salon_fama)
            elif opcion == 2:  # Salón de la Fama
                self._manejar_salon_fama(screen, salon_fama)
            elif opcion == 3:  # Administración
                self._manejar_administracion(screen, admin, salon_fama)
            elif opcion == 4:  # Salir
                ejecutando = self._manejar_salir(screen)

        # Al salir del loop, cerrar Pygame y terminar el proceso de forma limpia
        pygame.quit()  # Libera recursos de Pygame (ventana, audio, etc.)
        sys.exit()  # Termina el proceso del programa explícitamente

    def _manejar_iniciar_juego(self, screen, salon_fama):
        """Maneja la opción de iniciar juego y guarda el puntaje si termina."""
        pantalla_inicio = PantallaIniciarJuego(screen)
        nombre = pantalla_inicio.ejecutar()

        if nombre:
            pantalla = PantallaJuego(nombre)
            datos_puntaje = pantalla.ejecutar()

            # Si hay datos de puntaje, guardar en el salón de la fama
            if datos_puntaje:
                from mundo.registro import Registro

                registro = Registro(
                    nombre_jugador=datos_puntaje["nombre"],
                    puntaje=datos_puntaje["puntaje"],
                    laberinto=datos_puntaje["laberinto"],
                    tiempo_juego=datos_puntaje.get("tiempo_juego", 0),
                )
                salon_fama.guardar_puntaje(registro)

    def _manejar_salon_fama(self, screen, salon_fama):
        """Maneja la opción de Salón de la Fama."""
        # Recargar datos para mostrar los puntajes más recientes
        salon_fama.cargar_datos()
        pantalla_salon = PantallaSalonFama(screen, salon_fama)
        pantalla_salon.ejecutar()

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
