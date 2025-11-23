"""
Pantalla de demostración de componentes UI pixel art.
Muestra todos los elementos visuales del nuevo sistema de interfaz.
"""

import pygame
from interfaz.pantallas.pantalla_base import PantallaBase
from interfaz.paleta_ui import PaletaUI
from interfaz.componentes import Boton, Panel, BarraVida, HUD
from interfaz.gestor_fuentes import GestorFuentes


class PantallaDemoUI(PantallaBase):
    """
    Pantalla de demostración de componentes UI.

    Características:
    - Muestra todos los tipos de botones
    - Demuestra diferentes estilos de paneles
    - Presenta el sistema de vida (corazones y barra)
    - Muestra el HUD completo
    """

    def __init__(self, screen):
        """
        Inicializa la pantalla de demo.

        Args:
            screen: pygame.Surface principal
        """
        super().__init__(screen)

        # Dimensiones
        self.width = screen.get_width()
        self.height = screen.get_height()

        # Estado de la demo (inicializar ANTES de crear componentes)
        self.vida_demo = 75  # Para demostración
        self.llaves_demo = 3
        self.puntaje_demo = 1250
        self.resultado = None

        # Inicializar componentes
        self._crear_botones()
        self._crear_paneles()
        self._crear_barras_vida()
        self._crear_hud()

    def _crear_botones(self):
        """Crea botones de demostración en diferentes tamaños."""
        self.botones = []

        # Botón pequeño
        btn_pequeño = Boton(
            50,
            50,
            120,
            30,
            "PEQUEÑO",
            lambda: print("Botón pequeño clickeado"),
        )
        self.botones.append(("Botón pequeño (120×30)", btn_pequeño))

        # Botón mediano
        btn_mediano = Boton(
            50,
            100,
            160,
            40,
            "MEDIANO",
            lambda: self._cambiar_vida(-10),
        )
        self.botones.append(("Botón mediano (160×40)", btn_mediano))

        # Botón grande
        btn_grande = Boton(
            50,
            160,
            200,
            50,
            "GRANDE",
            lambda: self._cambiar_vida(10),
        )
        self.botones.append(("Botón grande (200×50)", btn_grande))

        # Botón deshabilitado
        btn_disabled = Boton(50, 230, 160, 40, "DESHABILITADO")
        btn_disabled.set_habilitado(False)
        self.botones.append(("Botón deshabilitado", btn_disabled))

        # Botón de salir (esquina)
        btn_salir = Boton(
            self.width - 170,
            self.height - 60,
            150,
            40,
            "VOLVER",
            lambda: self._marcar_salida(),
        )
        self.botones.append(("Botón de acción", btn_salir))

    def _crear_paneles(self):
        """Crea paneles de demostración en diferentes estilos."""
        self.paneles = []

        # Panel simple
        panel_simple = Panel(300, 50, 220, 100, tipo="simple")
        self.paneles.append(("Panel simple", panel_simple))

        # Panel GBA
        panel_gba = Panel(300, 170, 220, 100, tipo="gba")
        self.paneles.append(("Panel GBA (Zelda)", panel_gba))

        # Panel translúcido
        panel_trans = Panel(540, 50, 220, 100, tipo="translucido", alpha=200)
        self.paneles.append(("Panel translúcido (HLD)", panel_trans))

        # Panel decorado
        panel_deco = Panel(540, 170, 220, 100, tipo="decorado")
        self.paneles.append(("Panel decorado (Shovel Knight)", panel_deco))

    def _crear_barras_vida(self):
        """Crea barras de vida en diferentes estilos."""
        self.barras_vida = []

        # Barra segmentada (Dead Cells)
        barra_seg = BarraVida(300, 300, max_vida=100, estilo="segmentada")
        barra_seg.actualizar(self.vida_demo)
        self.barras_vida.append(("Barra segmentada (Dead Cells)", barra_seg))

        # Sistema de corazones (Zelda)
        barra_corazones = BarraVida(300, 350, max_vida=10, estilo="corazones")
        barra_corazones.actualizar(7)  # 7 de 10 (3.5 corazones llenos)
        self.barras_vida.append(("Sistema de corazones (Zelda)", barra_corazones))

    def _crear_hud(self):
        """Crea el HUD completo."""
        self.hud = HUD(self.width, self.height)
        self.hud.actualizar(self.vida_demo, self.llaves_demo, self.puntaje_demo)

    def _cambiar_vida(self, delta):
        """
        Cambia la vida de demostración.

        Args:
            delta: Cambio en la vida
        """
        self.vida_demo = max(0, min(100, self.vida_demo + delta))
        self.barras_vida[0][1].actualizar(self.vida_demo)
        self.hud.actualizar(self.vida_demo, self.llaves_demo, self.puntaje_demo)

    def _marcar_salida(self):
        """Marca la pantalla para salir."""
        self.resultado = "volver"

    def manejar_escape(self):
        """Maneja la tecla ESC para salir de la demo."""
        return "volver"

    def manejar_evento_especifico(self, evento, mouse_pos):
        """
        Maneja eventos específicos de la pantalla de demo.

        Args:
            evento: pygame.Event
            mouse_pos: Tupla con posición del mouse

        Returns:
            str o None: Resultado si se debe salir
        """
        # Controles de teclado
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                self._cambiar_vida(5)
            elif evento.key == pygame.K_DOWN:
                self._cambiar_vida(-5)
            elif evento.key == pygame.K_RIGHT:
                self.llaves_demo = min(10, self.llaves_demo + 1)
                self.hud.actualizar(self.vida_demo, self.llaves_demo, self.puntaje_demo)
            elif evento.key == pygame.K_LEFT:
                self.llaves_demo = max(0, self.llaves_demo - 1)
                self.hud.actualizar(self.vida_demo, self.llaves_demo, self.puntaje_demo)

        # Manejar eventos de botones
        for _, boton in self.botones:
            boton.manejar_evento(evento)

        return None

    def manejar_eventos(self, eventos):
        """
        Maneja eventos de la pantalla.

        Args:
            eventos: Lista de pygame.Event
        """
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.resultado = "salir"

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.resultado = "volver"

                # Controles de demo
                elif evento.key == pygame.K_UP:
                    self._cambiar_vida(5)
                elif evento.key == pygame.K_DOWN:
                    self._cambiar_vida(-5)
                elif evento.key == pygame.K_RIGHT:
                    self.llaves_demo = min(10, self.llaves_demo + 1)
                    self.hud.actualizar(
                        self.vida_demo, self.llaves_demo, self.puntaje_demo
                    )
                elif evento.key == pygame.K_LEFT:
                    self.llaves_demo = max(0, self.llaves_demo - 1)
                    self.hud.actualizar(
                        self.vida_demo, self.llaves_demo, self.puntaje_demo
                    )

            # Manejar eventos de botones
            for _, boton in self.botones:
                boton.manejar_evento(evento)

    def actualizar(self):
        """Actualiza el estado de la pantalla (LEGACY - mantener por compatibilidad)."""
        self._actualizar_interno()

    def _actualizar_interno(self):
        """Método interno para actualizar estado."""
        # Actualizar estado de botones según posición del mouse
        pos_mouse = pygame.mouse.get_pos()
        for _, boton in self.botones:
            boton.actualizar(pos_mouse)

        # Incrementar puntaje de demo
        self.puntaje_demo += 1
        self.hud.actualizar(self.vida_demo, self.llaves_demo, self.puntaje_demo)

    def dibujar(self):
        """Dibuja todos los elementos de la pantalla."""
        # Actualizar primero
        self._actualizar_interno()

        # Fondo oscuro
        self.screen.fill(PaletaUI.DARK)

        # Título
        gestor = GestorFuentes.obtener()
        fuente_titulo = gestor.titulo_normal
        titulo = fuente_titulo.render(
            "DEMO DE COMPONENTES UI", True, PaletaUI.BLUE_LIGHT
        )
        titulo_rect = titulo.get_rect(center=(self.width // 2, 20))

        # Sombra del título
        titulo_sombra = fuente_titulo.render(
            "DEMO DE COMPONENTES UI", True, PaletaUI.DARK
        )
        sombra_rect = titulo_rect.copy()
        sombra_rect.x += 2
        sombra_rect.y += 2

        self.screen.blit(titulo_sombra, sombra_rect)
        self.screen.blit(titulo, titulo_rect)

        # Dibujar botones
        gestor = GestorFuentes.obtener()
        fuente_label = gestor.texto_pequeño
        for label, boton in self.botones:
            boton.dibujar(self.screen)

            # Label descriptivo
            texto_label = fuente_label.render(label, True, PaletaUI.LIGHT)
            self.screen.blit(texto_label, (boton.rect.x, boton.rect.y - 18))

        # Dibujar paneles
        for label, panel in self.paneles:
            panel.dibujar(self.screen)

            # Label descriptivo
            texto_label = fuente_label.render(label, True, PaletaUI.LIGHT)
            self.screen.blit(texto_label, (panel.rect.x, panel.rect.y - 18))

        # Dibujar barras de vida
        for label, barra in self.barras_vida:
            barra.dibujar(self.screen)

            # Label descriptivo
            texto_label = fuente_label.render(label, True, PaletaUI.LIGHT)
            self.screen.blit(texto_label, (barra.x, barra.y - 18))

        # Dibujar HUD
        self.hud.dibujar(self.screen)

        # Instrucciones
        fuente_inst = gestor.texto_pequeño
        instrucciones = [
            "CONTROLES:",
            "↑↓ : Cambiar vida",
            "←→ : Cambiar llaves",
            "Click: Botones",
            "ESC: Volver",
        ]

        y_inst = self.height - 150
        for instruccion in instrucciones:
            texto = fuente_inst.render(instruccion, True, PaletaUI.LIGHT)
            self.screen.blit(texto, (50, y_inst))
            y_inst += 20

        # Actualizar pantalla
        pygame.display.flip()

    def obtener_resultado(self):
        """
        Retorna el resultado de la pantalla.

        Returns:
            str o None: Resultado de la pantalla
        """
        return self.resultado
