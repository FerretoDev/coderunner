"""
Gestor de dificultad progresiva para el juego.

Maneja el aumento gradual de dificultad mediante:
- Incremento de velocidad del enemigo
- Estrategias configurables (lineal, exponencial, por niveles)
"""

from abc import ABC, abstractmethod


class EstrategiaDificultad(ABC):
    """Interfaz para estrategias de dificultad progresiva."""

    @abstractmethod
    def calcular_velocidad(
        self, velocidad_base: float, tiempo_transcurrido: int, **kwargs
    ) -> float:
        """
        Calcula la velocidad actual basándose en el tiempo transcurrido.

        Args:
            velocidad_base: Velocidad inicial del enemigo
            tiempo_transcurrido: Frames desde el inicio del juego
            **kwargs: Parámetros adicionales específicos de la estrategia

        Returns:
            Nueva velocidad calculada
        """
        pass


class DificultadLineal(EstrategiaDificultad):
    """Incrementa la velocidad de forma lineal cada cierto intervalo."""

    def calcular_velocidad(
        self,
        velocidad_base: float,
        tiempo_transcurrido: int,
        intervalo_frames: int = 300,
        incremento: float = 0.5,
        **kwargs,
    ) -> float:
        """
        Incremento lineal: velocidad_base + (incremento * número_de_intervalos).

        Args:
            velocidad_base: Velocidad inicial
            tiempo_transcurrido: Frames transcurridos
            intervalo_frames: Frames entre cada incremento (default: 300)
            incremento: Cantidad a sumar cada intervalo (default: 0.5)

        Returns:
            Nueva velocidad
        """
        if tiempo_transcurrido == 0:
            return velocidad_base

        num_incrementos = tiempo_transcurrido // intervalo_frames
        return velocidad_base + (incremento * num_incrementos)


class DificultadExponencial(EstrategiaDificultad):
    """Incrementa la velocidad de forma exponencial."""

    def calcular_velocidad(
        self,
        velocidad_base: float,
        tiempo_transcurrido: int,
        intervalo_frames: int = 300,
        factor: float = 1.2,
        **kwargs,
    ) -> float:
        """
        Incremento exponencial: velocidad_base * (factor ^ número_de_intervalos).

        Args:
            velocidad_base: Velocidad inicial
            tiempo_transcurrido: Frames transcurridos
            intervalo_frames: Frames entre cada incremento (default: 300)
            factor: Factor multiplicativo (default: 1.2 = +20% cada intervalo)

        Returns:
            Nueva velocidad
        """
        if tiempo_transcurrido == 0:
            return velocidad_base

        num_incrementos = tiempo_transcurrido // intervalo_frames
        return velocidad_base * (factor**num_incrementos)


class DificultadPorNiveles(EstrategiaDificultad):
    """Incrementa la velocidad en niveles discretos."""

    def calcular_velocidad(
        self,
        velocidad_base: float,
        tiempo_transcurrido: int,
        niveles: dict[int, float] | None = None,
        **kwargs,
    ) -> float:
        """
        Incremento por niveles: velocidad cambia al alcanzar ciertos umbrales.

        Args:
            velocidad_base: Velocidad inicial
            tiempo_transcurrido: Frames transcurridos
            niveles: Dict {frames_minimos: velocidad} (default: niveles predefinidos)

        Returns:
            Nueva velocidad según el nivel actual

        Example:
            niveles = {
                0: 3.0,      # Nivel 1: 0-600 frames
                600: 4.0,    # Nivel 2: 600-1200 frames
                1200: 5.5,   # Nivel 3: 1200+ frames
            }
        """
        if niveles is None:
            # Niveles por defecto
            niveles = {
                0: velocidad_base,
                300: velocidad_base + 0.5,
                600: velocidad_base + 1.0,
                900: velocidad_base + 1.5,
                1200: velocidad_base + 2.0,
            }

        # Encontrar el nivel actual
        velocidad_actual = velocidad_base
        for umbral, velocidad in sorted(niveles.items()):
            if tiempo_transcurrido >= umbral:
                velocidad_actual = velocidad
            else:
                break

        return velocidad_actual


class GestorDificultad:
    """
    Gestiona el aumento progresivo de dificultad del juego.

    Permite cambiar entre diferentes estrategias de dificultad y
    proporciona métodos para actualizar la velocidad del enemigo.
    """

    def __init__(
        self,
        estrategia: EstrategiaDificultad | None = None,
        intervalo_frames: int = 300,
        incremento: float = 0.5,
    ):
        """
        Inicializa el gestor de dificultad.

        Args:
            estrategia: Estrategia a usar (default: DificultadLineal)
            intervalo_frames: Frames entre incrementos
            incremento: Cantidad de incremento (para estrategia lineal)
        """
        self.estrategia = estrategia or DificultadLineal()
        self.intervalo_frames = intervalo_frames
        self.incremento = incremento
        self.velocidad_inicial: float | None = None

    def establecer_estrategia(self, estrategia: EstrategiaDificultad):
        """Cambia la estrategia de dificultad."""
        self.estrategia = estrategia

    def actualizar_velocidad(
        self, enemigo, tiempo_transcurrido: int, velocidad_inicial: float | None = None
    ):
        """
        Actualiza la velocidad del enemigo según la estrategia actual.

        Args:
            enemigo: Objeto Computadora con atributo velocidad
            tiempo_transcurrido: Frames desde el inicio
            velocidad_inicial: Velocidad base (se guarda en primera llamada)
        """
        # Guardar velocidad inicial en la primera actualización
        if self.velocidad_inicial is None and velocidad_inicial is not None:
            self.velocidad_inicial = velocidad_inicial

        if self.velocidad_inicial is None:
            return

        nueva_velocidad = self.estrategia.calcular_velocidad(
            self.velocidad_inicial,
            tiempo_transcurrido,
            intervalo_frames=self.intervalo_frames,
            incremento=self.incremento,
        )

        enemigo.velocidad = nueva_velocidad

    def obtener_nivel_actual(self, tiempo_transcurrido: int) -> int:
        """
        Retorna el nivel de dificultad actual (basado en intervalos).

        Args:
            tiempo_transcurrido: Frames desde el inicio

        Returns:
            Número de nivel (1, 2, 3, ...)
        """
        if tiempo_transcurrido == 0:
            return 1
        return (tiempo_transcurrido // self.intervalo_frames) + 1
