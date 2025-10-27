import pygame


class Router:
    """
    Enrutador de pantallas: administra navegación y ciclo principal.

    Uso:
        router = Router(screen)                  # Crea el enrutador con la pantalla principal
        router.registrar("menu", MenuPrincipal)  # Registra una pantalla con un nombre
        router.registrar("juego", PantallaJuego) # Registra otra pantalla
        router.ir_a("menu")                      # Va a la pantalla inicial
        router.ejecutar()                        # Inicia el loop que delega a la pantalla actual
    """

    def __init__(self, screen):
        self.screen = screen  # Superficie principal donde dibujan las pantallas
        self.pantallas = {}  # Mapa nombre -> clase de pantalla (constructor)
        self.pantalla_actual = None  # Instancia de la pantalla en uso
        self.nombre_actual = None  # Nombre de la pantalla actual (para diagnóstico)
        self.ejecutando = True  # Controla si el loop principal sigue corriendo
        self.state = AppState()  # Estado global compartido entre pantallas

    def registrar(self, nombre: str, clase_pantalla):
        """Registra una pantalla por nombre para poder navegar luego."""
        self.pantallas[nombre] = clase_pantalla  # Guarda la clase asociada a ese nombre

    def ir_a(self, nombre: str, **kwargs):
        """Cambia a otra pantalla instanciándola con screen, router, state y parámetros opcionales."""
        if nombre in self.pantallas:  # Verifica que exista la pantalla
            self.nombre_actual = nombre  # Actualiza el nombre actual
            # Crea la pantalla y le pasa dependencias comunes + parámetros específicos
            self.pantalla_actual = self.pantallas[nombre](
                screen=self.screen, router=self, state=self.state, **kwargs
            )
            return True  # Navegación exitosa
        else:
            print(f"⚠️ Pantalla '{nombre}' no existe")  # Ayuda a detectar errores de nombre
            return False  # Navegación fallida

    def volver(self):
        """Vuelve a la pantalla anterior (simple: por ahora envía al 'menu')."""
        # TODO: Implementar historial real para múltiples pasos atrás
        self.ir_a("menu")  # Solución temporal sencilla

    def salir(self):
        """Solicita el cierre del loop principal y de la app."""
        self.ejecutando = False  # El loop principal terminará

    def ejecutar(self):
        """Loop principal: delega eventos y dibujo a la pantalla actual y maneja resultados de navegación."""
        clock = pygame.time.Clock()  # Controla FPS del ciclo principal

        while self.ejecutando:  # Corre hasta que se llame a salir()
            clock.tick(60)  # Limita a 60 FPS para fluidez y menor consumo

            if self.pantalla_actual:
                # Cada pantalla se actualiza: maneja eventos, lógica y dibuja
                resultado = self.pantalla_actual.actualizar()

                # Si la pantalla devuelve una acción, se procesa aquí (navegación/salida)
                if resultado:
                    self._manejar_resultado(resultado)

            pygame.display.flip()  # Presenta en pantalla lo dibujado en este frame

        pygame.quit()  # Libera recursos de Pygame cuando termina el loop

    def _manejar_resultado(self, resultado):
        """Interpreta el dict devuelto por una pantalla y ejecuta la acción de navegación correspondiente."""
        if isinstance(resultado, dict):  # Se espera un dict con la clave 'accion'
            accion = resultado.get("accion")

            if accion == "ir_a":
                destino = resultado.get("destino")  # Nombre de la pantalla destino
                params = resultado.get("params", {})  # Parámetros extra para construirla
                self.ir_a(destino, **params)  # Navega a la pantalla solicitada

            elif accion == "volver":
                self.volver()  # Vuelve a 'menu' (temporal)

            elif accion == "salir":
                self.salir()  # Señal de terminar la app


class AppState:
    """
    Estado global de la aplicación (compartido por todas las pantallas).

    Sirve para:
    - Conservar usuario actual, puntaje, laberinto, etc.
    - Exponer servicios compartidos como salón de la fama o administrador.
    """

    def __init__(self):
        self.usuario = None  # Nombre del usuario autenticado (o None)
        self.puntaje_actual = 0  # Puntaje en curso (se puede mostrar en HUD)
        self.laberinto_actual = None  # Nombre/ID del laberinto actual si aplica
        self.salon_fama = None  # Servicio para leer/guardar puntajes
        self.administrador = None  # Servicio para autenticación de admin

        # Cargar servicios compartidos una sola vez
        self._inicializar_servicios()

    def _inicializar_servicios(self):
        """Crea instancias de servicios globales para uso de todas las pantallas."""
        from models.administrador import Administrador
        from models.salon_fama import SalonFama
        # from models.sistema_sonido import SistemaSonido  # Si se integra sonido global

        self.salon_fama = SalonFama()  # Manejo de récords
        self.administrador = Administrador("casa")  # Admin con clave por defecto para pruebas

    def iniciar_sesion(self, nombre: str):
        """Guarda el usuario actual (por ejemplo, tras ingresar nombre en una pantalla)."""
        self.usuario = nombre  # Ahora hay usuario activo

    def cerrar_sesion(self):
        """Limpia usuario y puntaje (por ejemplo, al volver al menú principal)."""
        self.usuario = None  # Cierra sesión
        self.puntaje_actual = 0  # Reinicia puntaje


class PantallaBase:
    """
    Clase base para todas las pantallas.

    Proporciona:
    - Referencias a screen, router y state.
    - Un método actualizar que maneja eventos comunes (cerrar/volver) y dibuja.
    - Ganchos manejar_evento y dibujar para que cada pantalla implemente su lógica.
    """

    def __init__(self, screen, router, state):
        self.screen = screen  # Superficie de dibujo de la app
        self.router = router  # Acceso a navegación (ir_a, volver, salir)
        self.state = state  # Estado global compartido (usuario, puntaje, servicios)
        self.ancho = screen.get_width()  # Útil para centrar elementos
        self.alto = screen.get_height()  # Útil para posicionar UI

    def actualizar(self):
        """
        Método de ciclo por frame.
        Retorna:
            - dict con 'accion' para navegación (ir_a/volver/salir), o
            - None si no hay acción pendiente.
        """
        # Manejo genérico de eventos comunes a todas las pantallas
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return {"accion": "salir"}  # Cierra la app

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return {"accion": "volver"}  # Retrocede (por defecto al menú)

            # Delegar a la pantalla concreta para manejar sus propios eventos
            resultado = self.manejar_evento(evento)
            if resultado:
                return resultado  # La pantalla pidió una navegación específica

        # Dibujo de la pantalla concreta
        self.dibujar()

        return None  # No hay acción de navegación este frame

    def manejar_evento(self, evento):
        """Para sobreescribir: manejar eventos específicos de la pantalla."""
        pass  # Cada pantalla define su propio manejo

    def dibujar(self):
        """Para sobreescribir: dibujo específico de la pantalla."""
        pass  # Cada pantalla define su propio render
