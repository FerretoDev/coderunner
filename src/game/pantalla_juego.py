import math

import pygame

from models.computadora import Computadora
from models.jugador import Jugador
from models.laberinto import Laberinto
from models.sistema_sonido import SistemaSonido


class PantallaJuego:
    """Pantalla principal del juego con interfaz mejorada"""

    ANCHO = 1200
    ALTO = 800
    TAM_CELDA = 32

    # Diccionario de colores predefinidos para la interfaz del juego en rgb
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
        # self.victoria = False  # Ya no se usa, el juego es infinito
        self.frame_count = 0
        self.tiempo_transcurrido = 0
        self.mostrar_distancia = False
        self.nombre_jugador = nombre_jugador

        # Timer para Game Over (esperar 5 segundos antes de permitir salir)
        self.game_over_timer = 0
        self.game_over_espera = 300  # 5 segundos a 60 FPS

        # Sistema de obsequios con tiempo límite
        self.tiempo_vida_obsequio = 600  # 10 segundos a 60 FPS
        self.obsequios_timers = {}  # {(col, fila): frames_restantes}

        # Sistema de dificultad progresiva
        self.velocidad_inicial_enemigo = 1.5
        self.tiempo_incremento_velocidad = 600  # Cada 10 segundos aumenta velocidad
        self.incremento_velocidad = 0.2  # Cuánto aumenta cada vez

        # Cargar laberinto desde JSON
        self.laberinto = Laberinto("laberinto1.json")
        self.mapa = self.laberinto.laberinto

        # Calcular el tamaño de celda óptimo para que el laberinto ocupe más pantalla
        # Laberinto: 16 columnas x 9 filas
        # Área disponible: ANCHO x (ALTO - 80 para HUD)
        ancho_disponible = self.ANCHO - 40  # Margen de 20px a cada lado
        alto_disponible = self.ALTO - 120  # 80px HUD + 40px margen

        tam_por_ancho = ancho_disponible // len(self.mapa[0])
        tam_por_alto = alto_disponible // len(self.mapa)

        # Usar el menor para que quepa todo
        self.tam_celda = min(tam_por_ancho, tam_por_alto)

        # Calcular offset para centrar el laberinto
        ancho_laberinto = len(self.mapa[0]) * self.tam_celda
        alto_laberinto = len(self.mapa) * self.tam_celda

        self.offset_x = (self.ANCHO - ancho_laberinto) // 2
        self.offset_y = (
            (self.ALTO - alto_laberinto) // 2
        ) + 40  # +40 para bajar un poco del HUD

        # Sistema de movimiento por celdas
        self.movimiento_por_celdas = True
        self.teclas_presionadas = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
        }
        self.ultima_tecla_presionada = None

        # Sistema de cooldown para movimiento continuo por celdas
        self.cooldown_movimiento = 0  # Frames restantes antes de poder moverse
        self.frames_por_movimiento = (
            8  # Cooldown entre movimientos (ajustable para velocidad)
        )

        # Crear muros
        self.muros = self._generar_muros()

        # Crear personajes usando las posiciones del laberinto JSON
        # Radio visual más pequeño que el tamaño del rect para mejor colisión
        radio_jugador = 12
        radio_compu = 12

        # Calcular posición centrada usando las posiciones del JSON + offset
        celda_jugador_x, celda_jugador_y = self.laberinto.jugador_inicio
        pos_x_jugador = (
            celda_jugador_x * self.tam_celda
            + (self.tam_celda - radio_jugador * 2) // 2
            + self.offset_x
        )
        pos_y_jugador = (
            celda_jugador_y * self.tam_celda
            + (self.tam_celda - radio_jugador * 2) // 2
            + self.offset_y
        )

        # Calcular posición centrada para la computadora
        celda_compu_x, celda_compu_y = self.laberinto.computadora_inicio
        pos_x_compu = (
            celda_compu_x * self.tam_celda
            + (self.tam_celda - radio_compu * 2) // 2
            + self.offset_x
        )
        pos_y_compu = (
            celda_compu_y * self.tam_celda
            + (self.tam_celda - radio_compu * 2) // 2
            + self.offset_y
        )

        self.jugador = Jugador(pos_x_jugador, pos_y_jugador, radio_jugador)
        self.computadora = Computadora(
            pos_x_compu,
            pos_y_compu,
            radio_compu,
            self.velocidad_inicial_enemigo,
        )

        # Guardar posiciones iniciales para respawn
        self.jugador_spawn_x = pos_x_jugador
        self.jugador_spawn_y = pos_y_jugador
        self.computadora_spawn_x = pos_x_compu
        self.computadora_spawn_y = pos_y_compu

        # Posiciones anteriores para revertir movimientos
        self.pos_anterior_x = self.jugador.jugador_principal.x
        self.pos_anterior_y = self.jugador.jugador_principal.y

        # Inicializar timers de obsequios
        self._inicializar_timers_obsequios()

        #Musica Perrona
        musica_perrona = SistemaSonido()
        musica_perrona.musica_perrona()


    def _inicializar_timers_obsequios(self):
        """Inicializa los timers para cada obsequio activo"""
        for posicion in self.laberinto._obsequios.keys():
            self.obsequios_timers[posicion] = self.tiempo_vida_obsequio

    def _generar_muros(self):
        """Genera rectángulos de colisión desde el mapa"""
        muros = []
        for fila in range(len(self.mapa)):
            for col in range(len(self.mapa[0])):
                if self.mapa[fila][col] == 1:
                    x = col * self.tam_celda + self.offset_x
                    y = fila * self.tam_celda + self.offset_y
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
            # Verificar que no se salga del límite superior del laberinto
            if nueva_y >= self.offset_y:
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
            # Verificar que no se salga del límite inferior del laberinto
            limite_y_max = self.offset_y + (len(self.mapa) * self.tam_celda)
            if nueva_y + self.jugador.jugador_principal.height <= limite_y_max:
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
            # Verificar que no se salga del límite izquierdo del laberinto
            if nueva_x >= self.offset_x:
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
            # Verificar que no se salga del límite derecho del laberinto
            limite_x_max = self.offset_x + (len(self.mapa[0]) * self.tam_celda)
            if nueva_x + self.jugador.jugador_principal.width <= limite_x_max:
                temp_rect = pygame.Rect(
                    nueva_x,
                    self.jugador.jugador_principal.y,
                    self.jugador.jugador_principal.width,
                    self.jugador.jugador_principal.height,
                )
                if not any(temp_rect.colliderect(muro) for muro in self.muros):
                    self.jugador.jugador_principal.x = nueva_x

    def _procesar_eventos_teclado(self):
        """Procesa los eventos de teclado para movimiento por celdas con cooldown"""
        # Reducir el cooldown en cada frame
        if self.cooldown_movimiento > 0:
            self.cooldown_movimiento -= 1
            return

        keys = pygame.key.get_pressed()

        # Detectar tecla presionada y mover si el cooldown llegó a 0
        # Soporta tanto flechas como WASD
        tecla_actual = None
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            tecla_actual = "up"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            tecla_actual = "down"
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            tecla_actual = "left"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            tecla_actual = "right"

        # Mover si hay una tecla presionada y el cooldown está en 0
        if tecla_actual:
            self._mover_jugador_por_celdas(tecla_actual)
            # Activar cooldown después del movimiento
            self.cooldown_movimiento = self.frames_por_movimiento

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
        # Si está en game over, solo incrementar el timer
        if self.game_over:
            if self.game_over_timer < self.game_over_espera:
                self.game_over_timer += 1
            return

        if self.pausado:
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

            # Aplicar límites del mapa considerando los offsets
            # El jugador puede moverse desde offset hasta offset + tamaño_laberinto
            limite_x_min = self.offset_x
            limite_x_max = (
                self.offset_x
                + (len(self.mapa[0]) * self.tam_celda)
                - self.jugador.jugador_principal.width
            )
            limite_y_min = self.offset_y
            limite_y_max = (
                self.offset_y
                + (len(self.mapa) * self.tam_celda)
                - self.jugador.jugador_principal.height
            )

            self.jugador.jugador_principal.x = max(
                limite_x_min, min(self.jugador.jugador_principal.x, limite_x_max)
            )
            self.jugador.jugador_principal.y = max(
                limite_y_min, min(self.jugador.jugador_principal.y, limite_y_max)
            )

            # Verificar colisiones del jugador
            if not self._detectar_colisiones():
                self._revertir_posicion()

        # Perseguir al jugador usando BFS sobre el grid
        self.computadora.perseguir_bfs(
            self.jugador, self.mapa, self.tam_celda, self.offset_x, self.offset_y
        )

        # Actualizar timers de obsequios
        self._actualizar_timers_obsequios()

        # Verificar recolección de obsequios
        self._verificar_recoleccion_obsequios()

        # Verificar captura
        self._verificar_captura()

        # Aumentar dificultad progresivamente
        self._aumentar_dificultad()

        # Actualizar tiempo
        self.tiempo_transcurrido += 1

    def _verificar_recoleccion_obsequios(self):
        """Verifica si el jugador recolecta un obsequio"""
        # Obtener la celda actual del jugador considerando los offsets
        jug_cx, jug_cy = self.jugador.jugador_principal.center

        # Restar offsets para obtener coordenadas relativas al laberinto
        x_rel = jug_cx - self.offset_x
        y_rel = jug_cy - self.offset_y

        celda_x = x_rel // self.tam_celda
        celda_y = y_rel // self.tam_celda
        posicion_celda = (celda_x, celda_y)

        # Verificar si hay un obsequio en esta celda
        puntos = self.laberinto.recolectar_obsequio(posicion_celda)
        if puntos > 0:
            self.jugador.sumar_puntos(puntos)
            # Eliminar el timer de este obsequio
            if posicion_celda in self.obsequios_timers:
                del self.obsequios_timers[posicion_celda]
            # Crear nuevo obsequio en otra posición
            self._crear_nuevo_obsequio()

    def _actualizar_timers_obsequios(self):
        """Actualiza los timers de los obsequios y los reposiciona si expiran"""
        obsequios_expirados = []

        for posicion, tiempo_restante in self.obsequios_timers.items():
            self.obsequios_timers[posicion] = tiempo_restante - 1

            if self.obsequios_timers[posicion] <= 0:
                obsequios_expirados.append(posicion)

        # Eliminar obsequios expirados y crear nuevos
        for posicion in obsequios_expirados:
            # Eliminar el obsequio del laberinto
            if posicion in self.laberinto._obsequios:
                valor = self.laberinto._obsequios[posicion].valor
                del self.laberinto._obsequios[posicion]
                del self.obsequios_timers[posicion]
                # Crear nuevo obsequio con el mismo valor
                self._crear_nuevo_obsequio(valor)

    def _crear_nuevo_obsequio(self, valor=10):
        """Crea un nuevo obsequio en una posición aleatoria válida"""
        import random

        from models.obsequio import Obsequio

        # Obtener posiciones válidas (celdas que no son paredes ni tienen obsequios)
        posiciones_validas = []
        for fila in range(len(self.mapa)):
            for col in range(len(self.mapa[0])):
                posicion = (col, fila)
                # Verificar que no sea pared, no tenga obsequio, y no sea posición de spawn
                if (
                    self.mapa[fila][col] == 0
                    and posicion not in self.laberinto._obsequios
                    and posicion != tuple(self.laberinto.jugador_inicio)
                    and posicion != tuple(self.laberinto.computadora_inicio)
                ):
                    posiciones_validas.append(posicion)

        if posiciones_validas:
            nueva_posicion = random.choice(posiciones_validas)
            # Crear nuevo obsequio
            self.laberinto._obsequios[nueva_posicion] = Obsequio(nueva_posicion, valor)
            # Inicializar su timer
            self.obsequios_timers[nueva_posicion] = self.tiempo_vida_obsequio

    def _aumentar_dificultad(self):
        """Aumenta la velocidad del enemigo progresivamente"""
        # Cada cierto tiempo, aumentar la velocidad
        if (
            self.tiempo_transcurrido % self.tiempo_incremento_velocidad == 0
            and self.tiempo_transcurrido > 0
        ):
            self.computadora.velocidad += self.incremento_velocidad
            # print(
            #    f"¡Dificultad aumentada! Velocidad enemigo: {self.computadora.velocidad:.2f}"
            # )

    def _renderizar(self):
        """Renderiza todo el juego"""
        self.screen.fill(self.COLORES["fondo"])

        # Dibujar laberinto
        self._dibujar_laberinto()

        # Dibujar obsequios con animación
        self.laberinto.dibujar_obsequios(
            self.screen, self.frame_count, self.tam_celda, self.offset_x, self.offset_y
        )

        # Dibujar personajes
        self.jugador.dibujar_jugador_principal(self.screen)
        self.computadora.dibujar_computadora_principal(self.screen)

        # Debug: dibujar distancia
        # if self.mostrar_distancia:
        # self._dibujar_linea_distancia()

        # Dibujar HUD
        self._dibujar_hud()

        # Overlays
        if self.pausado:
            self._dibujar_pausa()

        # Overlays
        if self.pausado:
            self._dibujar_pausa()

        if self.game_over:
            self._dibujar_game_over()

        # No hay pantalla de victoria, el juego es infinito
        # if self.victoria:
        #     self._dibujar_victoria()

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
                x = col * self.tam_celda + self.offset_x
                y = fila * self.tam_celda + self.offset_y

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
        pygame.draw.rect(
            self.screen,
            self.COLORES["hud_fondo"],
            panel_rect,
        )
        pygame.draw.line(
            self.screen, self.COLORES["acento"], (0, 80), (self.ANCHO, 80), 2
        )

        # Nombre
        nombre_surf = self.fuente_pequena.render(
            f"Jugador: {self.nombre_jugador}", True, self.COLORES["texto"]
        )
        self.screen.blit(nombre_surf, (20, 15))

        # Vidas (dibujar corazones como iconos)
        x_vidas = 20
        y_vidas = 45
        for i in range(self.jugador._vidas):
            # Dibujar un corazón simple con pygame
            corazon_x = x_vidas + (i * 35)
            # Dibujar dos círculos arriba
            pygame.draw.circle(
                self.screen, self.COLORES["vidas"], (corazon_x + 5, y_vidas + 5), 5
            )
            pygame.draw.circle(
                self.screen, self.COLORES["vidas"], (corazon_x + 15, y_vidas + 5), 5
            )
            # Dibujar triángulo abajo
            puntos = [
                (corazon_x, y_vidas + 6),
                (corazon_x + 20, y_vidas + 6),
                (corazon_x + 10, y_vidas + 18),
            ]
            pygame.draw.polygon(self.screen, self.COLORES["vidas"], puntos)

        # Puntaje con estrella dibujada
        x_puntaje = 200
        y_puntaje = 45

        # Dibujar estrella
        import math

        radio_ext = 12
        radio_int = 5
        puntos_estrella = []
        for i in range(10):
            angulo = math.pi / 2 + (i * math.pi / 5)
            radio = radio_ext if i % 2 == 0 else radio_int
            px = x_puntaje + radio * math.cos(angulo)
            py = y_puntaje + 10 - radio * math.sin(angulo)
            puntos_estrella.append((px, py))
        pygame.draw.polygon(self.screen, self.COLORES["puntaje"], puntos_estrella)

        # Texto del puntaje
        puntaje_surf = self.fuente_hud.render(
            f"{self.jugador._puntaje}", True, self.COLORES["puntaje"]
        )
        self.screen.blit(puntaje_surf, (x_puntaje + 20, y_puntaje))

        # Velocidad del enemigo (nivel de dificultad)
        nivel_dificultad = self.computadora.velocidad / self.velocidad_inicial_enemigo
        dificultad_surf = self.fuente_pequena.render(
            f"Dificultad: {nivel_dificultad:.1f}x", True, (255, 100, 100)
        )
        self.screen.blit(dificultad_surf, (400, 15))

        # Tiempo
        tiempo_min = self.tiempo_transcurrido // 3600
        tiempo_seg = (self.tiempo_transcurrido % 3600) // 60
        tiempo_surf = self.fuente_pequena.render(
            f"Tiempo: {tiempo_min:02d}:{tiempo_seg:02d}", True, self.COLORES["texto"]
        )
        self.screen.blit(tiempo_surf, (400, 45))

        # Controles
        controles_surf = self.fuente_pequena.render(
            "WASD/Flechas: Mover | P: Pausa | ESC: Salir", True, (150, 150, 150)
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
        """Dibuja overlay de game over y guarda en salón de la fama"""
        # Guardar puntaje en el salón de la fama (solo una vez)
        if not hasattr(self, "_puntaje_guardado"):
            self._guardar_en_salon_fama()
            self._puntaje_guardado = True

        overlay = pygame.Surface((self.ANCHO, self.ALTO))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        caja_rect = pygame.Rect(self.ANCHO // 2 - 300, self.ALTO // 2 - 200, 600, 400)
        pygame.draw.rect(self.screen, (40, 40, 60), caja_rect, border_radius=15)
        pygame.draw.rect(
            self.screen, self.COLORES["vidas"], caja_rect, 3, border_radius=15
        )

        titulo = self.fuente_titulo.render("GAME OVER", True, self.COLORES["vidas"])
        titulo_rect = titulo.get_rect(center=(self.ANCHO // 2, self.ALTO // 2 - 120))
        self.screen.blit(titulo, titulo_rect)

        puntaje = self.fuente_hud.render(
            f"Puntaje Final: {self.jugador._puntaje}", True, self.COLORES["puntaje"]
        )
        puntaje_rect = puntaje.get_rect(center=(self.ANCHO // 2, self.ALTO // 2 - 40))
        self.screen.blit(puntaje, puntaje_rect)

        # Mostrar tiempo jugado
        tiempo_segundos = self.tiempo_transcurrido // 60
        tiempo_texto = self.fuente_pequena.render(
            f"Tiempo: {tiempo_segundos} segundos", True, (200, 200, 200)
        )
        tiempo_rect = tiempo_texto.get_rect(
            center=(self.ANCHO // 2, self.ALTO // 2 + 10)
        )
        self.screen.blit(tiempo_texto, tiempo_rect)

        # Mostrar velocidad final del enemigo (calculado como multiplicador)
        nivel_dificultad_final = (
            self.computadora.velocidad / self.velocidad_inicial_enemigo
        )
        velocidad_texto = self.fuente_pequena.render(
            f"Nivel de dificultad: {nivel_dificultad_final:.1f}x",
            True,
            (200, 200, 200),
        )
        velocidad_rect = velocidad_texto.get_rect(
            center=(self.ANCHO // 2, self.ALTO // 2 + 50)
        )
        self.screen.blit(velocidad_texto, velocidad_rect)

        # Mostrar mensaje dependiendo del timer
        segundos_restantes = max(
            0, (self.game_over_espera - self.game_over_timer) // 60
        )
        if self.game_over_timer < self.game_over_espera:
            # Aún en espera
            instruccion = self.fuente_pequena.render(
                f"Espera {segundos_restantes + 1} segundos...",
                True,
                (255, 150, 150),
            )
        else:
            # Ya puede salir
            instruccion = self.fuente_pequena.render(
                "Presiona cualquier tecla para volver", True, (150, 255, 150)
            )
        instruccion_rect = instruccion.get_rect(
            center=(self.ANCHO // 2, self.ALTO // 2 + 120)
        )
        self.screen.blit(instruccion, instruccion_rect)

    def _guardar_en_salon_fama(self):
        """Guarda el puntaje del jugador en el salón de la fama"""
        from models.registro import Registro
        from models.salon_fama import SalonFama

        salon = SalonFama()

        # Crear registro con los parámetros correctos
        registro = Registro(
            nombre_jugador=self.nombre_jugador,
            puntaje=self.jugador._puntaje,
            laberinto=self.laberinto.nombre,
        )

        salon.guardar_puntaje(registro)
        # print(
        #    f"Puntaje guardado en el Salón de la Fama: {self.jugador._puntaje} puntos"
        # )

    def _dibujar_victoria(self):
        """Dibuja overlay de victoria"""
        overlay = pygame.Surface((self.ANCHO, self.ALTO))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        caja_rect = pygame.Rect(self.ANCHO // 2 - 300, self.ALTO // 2 - 150, 600, 300)
        pygame.draw.rect(self.screen, (40, 60, 40), caja_rect, border_radius=15)
        pygame.draw.rect(self.screen, (100, 255, 100), caja_rect, 3, border_radius=15)

        titulo = self.fuente_titulo.render("¡VICTORIA!", True, (100, 255, 100))
        titulo_rect = titulo.get_rect(center=(self.ANCHO // 2, self.ALTO // 2 - 80))
        self.screen.blit(titulo, titulo_rect)

        mensaje = self.fuente_hud.render(
            "¡Todos los obsequios recolectados!", True, (255, 215, 0)
        )
        mensaje_rect = mensaje.get_rect(center=(self.ANCHO // 2, self.ALTO // 2 - 30))
        self.screen.blit(mensaje, mensaje_rect)

        puntaje = self.fuente_hud.render(
            f"Puntaje Final: {self.jugador._puntaje}", True, self.COLORES["puntaje"]
        )
        puntaje_rect = puntaje.get_rect(center=(self.ANCHO // 2, self.ALTO // 2 + 20))
        self.screen.blit(puntaje, puntaje_rect)

        tiempo_min = self.tiempo_transcurrido // 3600
        tiempo_seg = (self.tiempo_transcurrido % 3600) // 60
        tiempo = self.fuente_pequena.render(
            f"Tiempo: {tiempo_min:02d}:{tiempo_seg:02d}", True, (200, 200, 200)
        )
        tiempo_rect = tiempo.get_rect(center=(self.ANCHO // 2, self.ALTO // 2 + 60))
        self.screen.blit(tiempo, tiempo_rect)

        instruccion = self.fuente_pequena.render(
            "Presiona cualquier tecla para volver", True, (150, 150, 150)
        )
        instruccion_rect = instruccion.get_rect(
            center=(self.ANCHO // 2, self.ALTO // 2 + 100)
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

                # Salir cuando termina el juego (solo si han pasado 5 segundos)
                if (
                    self.game_over
                    and evento.key != pygame.K_p
                    and self.game_over_timer >= self.game_over_espera
                ):
                    return "salir"

        return None

    def ejecutar(self):
        """Loop principal del juego"""
        # Inicializar pygame si no está inicializado
        if not pygame.get_init():
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

        # No cerrar pygame, solo regresar al menú
        # pygame.quit() <- REMOVIDO
