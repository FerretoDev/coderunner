import math

import pygame

from models.computadora import Computadora
from models.jugador import Jugador


class PantallaJuego:
    """Pantalla principal del juego con interfaz mejorada"""

    ANCHO = 1200
    ALTO = 800
    TAM_CELDA = 32

    COLORES = {
        "fondo": (20, 20, 30),
        "hud_fondo": (30, 30, 50),
        "texto": (255, 255, 255),
        "vidas": (255, 100, 100),
        "puntaje": (255, 215, 0),
        "acento": (0, 150, 255),
        "pared": (50, 50, 70),
        "piso": (180, 180, 200),
        "jugador": (0, 150, 255),
        "enemigo": (255, 50, 50),
        "obsequio": (255, 215, 0),
    }

    def __init__(self, nombre_jugador="Jugador"):
        """Inicializa la pantalla de juego"""
        # Configuración de pantalla
        self.ANCHO = 1200
        self.ALTO = 800
        self.screen = None
        self.reloj = pygame.time.Clock()

        # Configuración de colores
        self.COLORES = {
            "fondo": (20, 25, 40),
            "pared": (60, 70, 90),
            "piso": (35, 40, 55),
            "jugador": (50, 150, 255),
            "computadora": (255, 50, 50),
            "hud_fondo": (15, 20, 35),
            "texto": (220, 220, 220),
            "acento": (100, 150, 255),
            "vidas": (255, 100, 100),
            "puntaje": (255, 200, 50),
        }

        # Estados del juego
        self.pausado = False
        self.game_over = False
        self.frame_count = 0
        self.tiempo_transcurrido = 0
        self.mostrar_distancia = False
        self.nombre_jugador = nombre_jugador

        # Cargar mapa y configuración
        from .laberinto_uno import TAM_CELDA, laberinto

        self.mapa = laberinto
        self.tam_celda = TAM_CELDA

        # Sistema de movimiento por celdas
        self.movimiento_por_celdas = True
        self.teclas_presionadas = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
        }
        self.ultima_tecla_presionada = None

        # Crear muros
        self.muros = self._generar_muros()

        # Crear personajes
        # Radio visual más pequeño que el tamaño del rect para mejor colisión
        self.jugador = Jugador(3 * self.tam_celda, 3 * self.tam_celda, 12)
        self.computadora = Computadora(
            18 * self.tam_celda,
            12 * self.tam_celda,
            12,
            1.5,  # Velocidad reducida para mejor balance
        )

        # Guardar posiciones iniciales para respawn
        self.jugador_spawn_x = 3 * self.tam_celda
        self.jugador_spawn_y = 3 * self.tam_celda
        self.computadora_spawn_x = 18 * self.tam_celda
        self.computadora_spawn_y = 12 * self.tam_celda

        # Posiciones anteriores para revertir movimientos
        self.pos_anterior_x = self.jugador.jugador_principal.x
        self.pos_anterior_y = self.jugador.jugador_principal.y

    def _generar_muros(self):
        """Genera rectángulos de colisión desde el mapa"""
        muros = []
        for fila in range(len(self.mapa)):
            for col in range(len(self.mapa[0])):
                if self.mapa[fila][col] == 1:
                    x = col * self.tam_celda
                    y = fila * self.tam_celda
                    rect = pygame.Rect(x, y, self.tam_celda, self.tam_celda)
                    muros.append(rect)
        return muros

    def _guardar_posicion_anterior(self):
        """Guarda la posición anterior del jugador"""
        self.pos_anterior_x = self.jugador.jugador_principal.x
        self.pos_anterior_y = self.jugador.jugador_principal.y

    def _revertir_posicion(self):
        """Revierte el jugador a la posición anterior"""
        self.jugador.jugador_principal.x = self.pos_anterior_x
        self.jugador.jugador_principal.y = self.pos_anterior_y

    def _detectar_colisiones(self):
        """Detecta colisiones del jugador con muros"""
        for muro in self.muros:
            if self.jugador.jugador_principal.colliderect(muro):
                return False
        return True

    def _mover_jugador_por_celdas(self, direccion):
        """Mueve al jugador una celda completa en la dirección especificada"""
        if direccion == "up":
            nueva_y = self.jugador.jugador_principal.y - self.tam_celda
            if nueva_y >= 0:
                temp_rect = pygame.Rect(
                    self.jugador.jugador_principal.x,
                    nueva_y,
                    self.jugador.jugador_principal.width,
                    self.jugador.jugador_principal.height,
                )
                if not any(temp_rect.colliderect(muro) for muro in self.muros):
                    self.jugador.jugador_principal.y = nueva_y

        elif direccion == "down":
            nueva_y = self.jugador.jugador_principal.y + self.tam_celda
            if (
                nueva_y + self.jugador.jugador_principal.height
                <= len(self.mapa) * self.tam_celda
            ):
                temp_rect = pygame.Rect(
                    self.jugador.jugador_principal.x,
                    nueva_y,
                    self.jugador.jugador_principal.width,
                    self.jugador.jugador_principal.height,
                )
                if not any(temp_rect.colliderect(muro) for muro in self.muros):
                    self.jugador.jugador_principal.y = nueva_y

        elif direccion == "left":
            nueva_x = self.jugador.jugador_principal.x - self.tam_celda
            if nueva_x >= 0:
                temp_rect = pygame.Rect(
                    nueva_x,
                    self.jugador.jugador_principal.y,
                    self.jugador.jugador_principal.width,
                    self.jugador.jugador_principal.height,
                )
                if not any(temp_rect.colliderect(muro) for muro in self.muros):
                    self.jugador.jugador_principal.x = nueva_x

        elif direccion == "right":
            nueva_x = self.jugador.jugador_principal.x + self.tam_celda
            if (
                nueva_x + self.jugador.jugador_principal.width
                <= len(self.mapa[0]) * self.tam_celda
            ):
                temp_rect = pygame.Rect(
                    nueva_x,
                    self.jugador.jugador_principal.y,
                    self.jugador.jugador_principal.width,
                    self.jugador.jugador_principal.height,
                )
                if not any(temp_rect.colliderect(muro) for muro in self.muros):
                    self.jugador.jugador_principal.x = nueva_x

    def _procesar_eventos_teclado(self):
        """Procesa los eventos de teclado para movimiento por celdas"""
        keys = pygame.key.get_pressed()

        # Detectar nuevas pulsaciones
        tecla_actual = None
        if keys[pygame.K_UP]:
            tecla_actual = "up"
        elif keys[pygame.K_DOWN]:
            tecla_actual = "down"
        elif keys[pygame.K_LEFT]:
            tecla_actual = "left"
        elif keys[pygame.K_RIGHT]:
            tecla_actual = "right"

        # Solo mover si es una nueva pulsación (no mantener presionada)
        if tecla_actual and tecla_actual != self.ultima_tecla_presionada:
            self._mover_jugador_por_celdas(tecla_actual)

        self.ultima_tecla_presionada = tecla_actual

    def _verificar_captura(self):
        """Verifica si la computadora captura al jugador"""
        dx = (
            self.jugador.jugador_principal.centerx
            - self.computadora.computadora_principal.centerx
        )
        dy = (
            self.jugador.jugador_principal.centery
            - self.computadora.computadora_principal.centery
        )
        distancia = math.sqrt(dx**2 + dy**2)

        # Radio de captura
        if distancia < self.jugador.radio + self.computadora.radio + 5:
            self.jugador.perder_vida()

            if not self.jugador.esta_vivo():
                self.game_over = True
                return True

            # Reiniciar posiciones a las posiciones iniciales de spawn
            self.jugador.jugador_principal.x = self.jugador_spawn_x
            self.jugador.jugador_principal.y = self.jugador_spawn_y
            self.computadora.computadora_principal.x = self.computadora_spawn_x
            self.computadora.computadora_principal.y = self.computadora_spawn_y

            # Limpiar el camino BFS de la computadora para recalcular
            self.computadora._bfs_camino = None

        return False

    def _actualizar(self):
        """Actualiza la lógica del juego"""
        if self.pausado or self.game_over:
            return

        self.frame_count += 1

        # Procesar movimiento del jugador por celdas
        if self.movimiento_por_celdas:
            self._procesar_eventos_teclado()
        else:
            # Movimiento pixel a pixel (modo legacy)
            self._guardar_posicion_anterior()
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT]:
                self.jugador.jugador_principal.x -= self.jugador.velocidad
            if teclas[pygame.K_RIGHT]:
                self.jugador.jugador_principal.x += self.jugador.velocidad
            if teclas[pygame.K_UP]:
                self.jugador.jugador_principal.y -= self.jugador.velocidad
            if teclas[pygame.K_DOWN]:
                self.jugador.jugador_principal.y += self.jugador.velocidad

            # Verificar colisiones del jugador
            if not self._detectar_colisiones():
                self._revertir_posicion()

        # Perseguir al jugador usando BFS sobre el grid
        self.computadora.perseguir_bfs(self.jugador, self.mapa, self.tam_celda)

        # Verificar captura
        self._verificar_captura()

        # Actualizar tiempo
        self.tiempo_transcurrido += 1

    def _renderizar(self):
        """Renderiza todo el juego"""
        self.screen.fill(self.COLORES["fondo"])

        # Dibujar laberinto
        self._dibujar_laberinto()

        # Dibujar personajes
        self.jugador.dibujar_jugador_principal(self.screen)
        self.computadora.dibujar_computadora_principal(self.screen)

        # Debug: dibujar distancia
        if self.mostrar_distancia:
            self._dibujar_linea_distancia()

        # Dibujar HUD
        self._dibujar_hud()

        # Overlays
        if self.pausado:
            self._dibujar_pausa()

        if self.game_over:
            self._dibujar_game_over()

        pygame.display.flip()

    def _dibujar_linea_distancia(self):
        """Dibuja una línea entre jugador y enemigo (debug)"""
        pos_jugador = self.jugador.jugador_principal.center
        pos_enemigo = self.computadora.computadora_principal.center

        pygame.draw.line(self.screen, (255, 100, 100), pos_jugador, pos_enemigo, 1)

        # Distancia
        dx = pos_enemigo[0] - pos_jugador[0]
        dy = pos_enemigo[1] - pos_jugador[1]
        distancia = math.sqrt(dx**2 + dy**2)

        dist_texto = self.fuente_pequena.render(
            f"Dist: {int(distancia)}", True, (255, 255, 255)
        )
        self.screen.blit(dist_texto, (pos_jugador[0] + 20, pos_jugador[1] - 20))

    def _dibujar_laberinto(self):
        """Dibuja el mapa del laberinto"""
        for fila in range(len(self.mapa)):
            for col in range(len(self.mapa[0])):
                x = col * self.tam_celda
                y = fila * self.tam_celda

                if self.mapa[fila][col] == 1:
                    pygame.draw.rect(
                        self.screen,
                        self.COLORES["pared"],
                        (x, y, self.tam_celda, self.tam_celda),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        self.COLORES["piso"],
                        (x, y, self.tam_celda, self.tam_celda),
                    )
                    pygame.draw.rect(
                        self.screen,
                        (100, 100, 120),
                        (x, y, self.tam_celda, self.tam_celda),
                        1,
                    )

    def _dibujar_hud(self):
        """Dibuja el HUD superior"""
        # Panel superior
        panel_rect = pygame.Rect(0, 0, self.ANCHO, 80)
        pygame.draw.rect(self.screen, self.COLORES["hud_fondo"], panel_rect)
        pygame.draw.line(
            self.screen, self.COLORES["acento"], (0, 80), (self.ANCHO, 80), 2
        )

        # Nombre
        nombre_surf = self.fuente_pequena.render(
            f"Jugador: {self.nombre_jugador}", True, self.COLORES["texto"]
        )
        self.screen.blit(nombre_surf, (20, 15))

        # Vidas
        vidas_surf = self.fuente_hud.render(
            f"❤ × {self.jugador._vidas}", True, self.COLORES["vidas"]
        )
        self.screen.blit(vidas_surf, (20, 45))

        # Puntaje
        puntaje_surf = self.fuente_hud.render(
            f"★ {self.jugador._puntaje}", True, self.COLORES["puntaje"]
        )
        self.screen.blit(puntaje_surf, (200, 45))

        # Tiempo
        tiempo_min = self.tiempo_transcurrido // 3600
        tiempo_seg = (self.tiempo_transcurrido % 3600) // 60
        tiempo_surf = self.fuente_pequena.render(
            f"Tiempo: {tiempo_min:02d}:{tiempo_seg:02d}", True, self.COLORES["texto"]
        )
        self.screen.blit(tiempo_surf, (400, 30))

        # Controles
        controles_surf = self.fuente_pequena.render(
            "Flechas: Mover | P: Pausa | ESC: Salir | D: Debug", True, (150, 150, 150)
        )
        controles_rect = controles_surf.get_rect(right=self.ANCHO - 20, centery=40)
        self.screen.blit(controles_surf, controles_rect)

    def _dibujar_pausa(self):
        """Dibuja overlay de pausa"""
        overlay = pygame.Surface((self.ANCHO, self.ALTO))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        titulo = self.fuente_titulo.render("PAUSA", True, self.COLORES["texto"])
        titulo_rect = titulo.get_rect(center=(self.ANCHO // 2, self.ALTO // 2 - 50))
        self.screen.blit(titulo, titulo_rect)

        instruccion = self.fuente_hud.render(
            "Presiona P para continuar", True, (200, 200, 200)
        )
        instruccion_rect = instruccion.get_rect(
            center=(self.ANCHO // 2, self.ALTO // 2 + 30)
        )
        self.screen.blit(instruccion, instruccion_rect)

    def _dibujar_game_over(self):
        """Dibuja overlay de game over"""
        overlay = pygame.Surface((self.ANCHO, self.ALTO))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        caja_rect = pygame.Rect(self.ANCHO // 2 - 300, self.ALTO // 2 - 150, 600, 300)
        pygame.draw.rect(self.screen, (40, 40, 60), caja_rect, border_radius=15)
        pygame.draw.rect(
            self.screen, self.COLORES["vidas"], caja_rect, 3, border_radius=15
        )

        titulo = self.fuente_titulo.render("GAME OVER", True, self.COLORES["vidas"])
        titulo_rect = titulo.get_rect(center=(self.ANCHO // 2, self.ALTO // 2 - 80))
        self.screen.blit(titulo, titulo_rect)

        puntaje = self.fuente_hud.render(
            f"Puntaje Final: {self.jugador._puntaje}", True, self.COLORES["puntaje"]
        )
        puntaje_rect = puntaje.get_rect(center=(self.ANCHO // 2, self.ALTO // 2 - 10))
        self.screen.blit(puntaje, puntaje_rect)

        instruccion = self.fuente_pequena.render(
            "Presiona cualquier tecla para volver", True, (150, 150, 150)
        )
        instruccion_rect = instruccion.get_rect(
            center=(self.ANCHO // 2, self.ALTO // 2 + 80)
        )
        self.screen.blit(instruccion, instruccion_rect)

    def manejar_eventos(self):
        """Maneja eventos del juego"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return "salir"

                if evento.key == pygame.K_p:
                    self.pausado = not self.pausado

                if evento.key == pygame.K_d:
                    self.mostrar_distancia = not self.mostrar_distancia

                if evento.key == pygame.K_m:
                    self.movimiento_por_celdas = not self.movimiento_por_celdas
                    modo = "Celdas" if self.movimiento_por_celdas else "Píxeles"
                    print(f"Modo de movimiento cambiado a: {modo}")

                if self.game_over and evento.key != pygame.K_p:
                    return "salir"

        return None

    def ejecutar(self):
        """Loop principal del juego"""
        # Inicializar pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.ANCHO, self.ALTO))
        pygame.display.set_caption("CodeRunner - Modo Laberinto")

        # Inicializar fuentes
        self.fuente_titulo = pygame.font.Font(None, 48)
        self.fuente_hud = pygame.font.Font(None, 32)
        self.fuente_pequena = pygame.font.Font(None, 24)

        ejecutando = True

        while ejecutando:
            self.reloj.tick(60)

            resultado = self.manejar_eventos()
            if resultado == "salir":
                ejecutando = False

            self._actualizar()
            self._renderizar()

        pygame.quit()
