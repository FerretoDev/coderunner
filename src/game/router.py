import pygame


class Router:
    """

    Uso:
        router = Router(screen)
        router.registrar("menu", MenuPrincipal)
        router.registrar("juego", PantallaJuego)
        router.ir_a("menu")
        router.ejecutar()
    """

    def __init__(self, screen):
        self.screen = screen
        self.pantallas = {}
        self.pantalla_actual = None
        self.nombre_actual = None
        self.ejecutando = True
        self.state = AppState()  # Estado global compartido

    def registrar(self, nombre: str, clase_pantalla):
        """Registra una pantalla (como rx.page)"""
        self.pantallas[nombre] = clase_pantalla

    def ir_a(self, nombre: str, **kwargs):
        """Navega a una pantalla (como rx.redirect)"""
        if nombre in self.pantallas:
            self.nombre_actual = nombre
            # Pasar screen, router y state a la pantalla
            self.pantalla_actual = self.pantallas[nombre](
                screen=self.screen, router=self, state=self.state, **kwargs
            )
            return True
        else:
            print(f"⚠️ Pantalla '{nombre}' no existe")
            return False

    def volver(self):
        """Vuelve a la pantalla anterior (como navegador)"""
        # TODO: Implementar historial de navegación
        self.ir_a("menu")

    def salir(self):
        """Cierra la aplicación"""
        self.ejecutando = False

    def ejecutar(self):
        """Loop principal de la aplicación"""
        clock = pygame.time.Clock()

        while self.ejecutando:
            clock.tick(60)

            if self.pantalla_actual:
                # Cada pantalla maneja sus propios eventos y dibuja
                resultado = self.pantalla_actual.actualizar()

                # Las pantallas pueden retornar acciones de navegación
                if resultado:
                    self._manejar_resultado(resultado)

            pygame.display.flip()

        pygame.quit()

    def _manejar_resultado(self, resultado):
        """Maneja las acciones de navegación retornadas por pantallas"""
        if isinstance(resultado, dict):
            accion = resultado.get("accion")

            if accion == "ir_a":
                destino = resultado.get("destino")
                params = resultado.get("params", {})
                self.ir_a(destino, **params)

            elif accion == "volver":
                self.volver()

            elif accion == "salir":
                self.salir()


class AppState:
    """
    Estado global de la aplicación (como rx.State en Reflex)
    Todas las pantallas comparten esta información
    """

    def __init__(self):
        self.usuario = None
        self.puntaje_actual = 0
        self.laberinto_actual = None
        self.salon_fama = None
        self.administrador = None

        # Cargar servicios
        self._inicializar_servicios()

    def _inicializar_servicios(self):
        """Inicializa servicios compartidos"""
        from models.administrador import Administrador
        from models.salon_fama import SalonFama

        # from models.sistema_sonido import SistemaSonido

        self.salon_fama = SalonFama()
        self.administrador = Administrador("casa")

    def iniciar_sesion(self, nombre: str):
        """Registra el usuario actual"""
        self.usuario = nombre

    def cerrar_sesion(self):
        """Limpia el usuario actual"""
        self.usuario = None
        self.puntaje_actual = 0


class PantallaBase:
    """
    Clase base para todas las pantallas (como Component en React)
    Todas las pantallas heredan de esta
    """

    def __init__(self, screen, router, state):
        self.screen = screen
        self.router = router
        self.state = state
        self.ancho = screen.get_width()
        self.alto = screen.get_height()

    def actualizar(self):
        """
        Método principal que llama el router
        Retorna: dict con acción de navegación o None
        """
        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return {"accion": "salir"}

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return {"accion": "volver"}

            # Cada pantalla puede manejar sus eventos
            resultado = self.manejar_evento(evento)
            if resultado:
                return resultado

        # Dibujar
        self.dibujar()

        return None

    def manejar_evento(self, evento):
        """Override en cada pantalla"""
        pass

    def dibujar(self):
        """Override en cada pantalla"""
        pass
