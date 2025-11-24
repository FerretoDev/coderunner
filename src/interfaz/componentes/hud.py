"""
HUD (Heads-Up Display) completo para el juego.
Basado en layout de runners con elementos de Zelda, Dead Cells, HLD.
"""

import pygame
from interfaz.paleta_ui import PaletaUI
from interfaz.componentes.barra_vida import BarraVida
from interfaz.gestor_fuentes import GestorFuentes


class HUD:
    """
    HUD completo del juego con:
    - Barra de vida (arriba izquierda)
    - Contador de llaves (arriba derecha)
    - Puntaje/distancia (centro arriba)
    - Mini-mapa (esquina inferior derecha)
    """

    def __init__(self, screen_width, screen_height):
        """
        Inicializa el HUD.

        Args:
            screen_width: Ancho de la pantalla
            screen_height: Alto de la pantalla
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Componentes del HUD
        self.barra_vida = BarraVida(10, 10, max_vida=10, estilo="segmentada")

        # Fuentes
        gestor = GestorFuentes.obtener()
        self.fuente_grande = gestor.texto_grande
        self.fuente_pequena = gestor.texto_pequeño

        # Datos del juego
        self.llaves = 0
        self.puntaje = 0
        self.tiempo = 0

        # Posiciones de elementos
        self._calcular_posiciones()

    def _calcular_posiciones(self):
        """Calcula las posiciones de los elementos del HUD."""
        # Contador de llaves (arriba derecha)
        self.pos_llaves = (self.screen_width - 120, 10)

        # Puntaje (centro arriba)
        self.pos_puntaje = (self.screen_width // 2 - 100, 10)

        # Mini-mapa (abajo derecha)
        self.pos_minimapa = (self.screen_width - 90, self.screen_height - 90)

    def actualizar(self, vida, llaves, puntaje, tiempo=0):
        """
        Actualiza los datos del HUD.

        Args:
            vida: Vida actual del jugador
            llaves: Número de llaves recolectadas
            puntaje: Puntaje actual
            tiempo: Tiempo transcurrido (opcional)
        """
        self.barra_vida.actualizar(vida)
        self.llaves = llaves
        self.puntaje = puntaje
        self.tiempo = tiempo

    def dibujar(self, surface):
        """
        Dibuja todos los elementos del HUD.

        Args:
            surface: pygame.Surface donde dibujar
        """
        # 1. Barra de vida
        self.barra_vida.dibujar(surface)

        # 2. Contador de llaves
        self._dibujar_contador_llaves(surface)

        # 3. Puntaje
        self._dibujar_puntaje(surface)

        # 4. Opcional: Mini-mapa (si se implementa)
        # self._dibujar_minimapa(surface)

    def _dibujar_contador_llaves(self, surface):
        """Dibuja el contador de llaves."""
        x, y = self.pos_llaves

        # Fondo del panel
        panel_rect = pygame.Rect(x, y, 100, 24)
        pygame.draw.rect(surface, (*PaletaUI.DARK, 200), panel_rect)
        pygame.draw.rect(surface, PaletaUI.BLUE_LIGHT, panel_rect, 1)

        # Icono de llave (rectángulo dorado simple)
        self._dibujar_icono_llave(surface, x + 8, y + 4)

        # Símbolo × y número
        texto_x = self.fuente_pequena.render("×", True, PaletaUI.WHITE)
        numero = self.fuente_grande.render(str(self.llaves), True, PaletaUI.GOLD)

        surface.blit(texto_x, (x + 30, y + 6))
        surface.blit(numero, (x + 45, y + 4))

    def _dibujar_icono_llave(self, surface, x, y):
        """
        Dibuja un icono de llave pixel art simple.

        Args:
            surface: Superficie donde dibujar
            x, y: Posición
        """
        # Cabeza de la llave (círculo)
        pygame.draw.circle(surface, PaletaUI.GOLD, (x + 4, y + 4), 3)
        pygame.draw.circle(surface, PaletaUI.GOLD_DARK, (x + 4, y + 4), 3, 1)

        # Vástago
        pygame.draw.rect(surface, PaletaUI.GOLD, (x + 4, y + 7, 2, 8))

        # Dientes
        pygame.draw.rect(surface, PaletaUI.GOLD, (x + 2, y + 13, 2, 2))
        pygame.draw.rect(surface, PaletaUI.GOLD, (x + 6, y + 11, 2, 2))

    def _dibujar_puntaje(self, surface):
        """Dibuja el panel de puntaje/distancia."""
        x, y = self.pos_puntaje

        # Fondo del panel
        panel_rect = pygame.Rect(x, y, 200, 32)
        pygame.draw.rect(surface, (*PaletaUI.DARK, 220), panel_rect)
        pygame.draw.rect(surface, PaletaUI.BLUE_LIGHT, panel_rect, 2)

        # Texto "PUNTAJE"
        label = self.fuente_pequena.render("PUNTAJE:", True, PaletaUI.LIGHT)
        surface.blit(label, (x + 10, y + 8))

        # Valor del puntaje
        valor = self.fuente_grande.render(str(self.puntaje), True, PaletaUI.WHITE)
        surface.blit(valor, (x + 90, y + 8))

    def _dibujar_minimapa(self, surface):
        """
        Dibuja un mini-mapa simplificado.
        (Placeholder - se puede implementar después)
        """
        x, y = self.pos_minimapa

        # Marco del mapa
        mapa_rect = pygame.Rect(x, y, 80, 80)
        pygame.draw.rect(surface, (*PaletaUI.DARK, 230), mapa_rect)
        pygame.draw.rect(surface, PaletaUI.WHITE, mapa_rect, 2)

        # Indicador del jugador (punto rojo en el centro)
        centro_x = x + 40
        centro_y = y + 40
        pygame.draw.circle(surface, PaletaUI.RED, (centro_x, centro_y), 3)
