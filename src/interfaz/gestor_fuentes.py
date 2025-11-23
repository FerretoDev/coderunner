"""
Gestor centralizado de fuentes para evitar recreación innecesaria.

Singleton que mantiene todas las fuentes pre-creadas y listas para usar
en cualquier pantalla, mejorando el rendimiento y uso de memoria.
"""

import pygame


class GestorFuentes:
    """
    Singleton que gestiona todas las fuentes del juego.

    Evita crear múltiples instancias de la misma fuente,
    lo cual es costoso en memoria y rendimiento.
    """

    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializado = False
        return cls._instancia

    def __init__(self):
        # Solo inicializar una vez
        if self._inicializado:
            return

        # Fuentes para títulos
        self.titulo_grande = pygame.font.Font(None, 72)  # MenuPrincipal
        self.titulo_normal = pygame.font.Font(None, 56)  # Pantallas comunes
        self.titulo_mediano = pygame.font.Font(None, 52)  # Carga laberinto
        self.titulo_pequeño = pygame.font.Font(None, 48)  # Modales
        self.titulo_mini = pygame.font.Font(None, 44)  # Modal confirmación

        # Fuentes para texto normal
        self.texto_grande = pygame.font.Font(None, 32)  # Texto importante
        self.texto_normal = pygame.font.Font(None, 28)  # Texto común
        self.texto_pequeño = pygame.font.Font(None, 24)  # Texto secundario
        self.texto_mini = pygame.font.Font(None, 22)  # Estadísticas
        self.texto_info = pygame.font.Font(None, 20)  # Info adicional

        # Fuentes específicas del juego
        self.hud_titulo = pygame.font.Font(None, 48)  # Títulos en juego
        self.hud_normal = pygame.font.Font(None, 32)  # HUD principal
        self.hud_pequeño = pygame.font.Font(None, 24)  # HUD secundario

        # Fuente monoespaciada para datos tabulares (si se necesita)
        try:
            self.monoespaciada = pygame.font.SysFont("courier", 24)
        except Exception:
            self.monoespaciada = pygame.font.Font(None, 24)

        self._inicializado = True

    @classmethod
    def obtener(cls):
        """Método alternativo para obtener la instancia."""
        return cls()

    def renderizar_texto(self, texto, fuente_nombre, color, antialias=True):
        """
        Renderiza texto usando una fuente del gestor.

        Args:
            texto: Texto a renderizar
            fuente_nombre: Nombre del atributo de fuente ('titulo_grande', 'texto_normal', etc.)
            color: Color del texto (tuple RGB)
            antialias: Si usar antialiasing (default True)

        Returns:
            Surface con el texto renderizado
        """
        fuente = getattr(self, fuente_nombre, self.texto_normal)
        return fuente.render(texto, antialias, color)
