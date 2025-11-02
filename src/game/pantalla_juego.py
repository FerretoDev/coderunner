import math  # Para calcular distancias y ángulos
import os

import pygame  # Motor de eventos, dibujo y tiempo

from models.computadora import Computadora
from models.jugador import Jugador
from models.laberinto import Laberinto
from models.sistema_sonido import SistemaSonido


class PantallaJuego:
    """Pantalla principal del juego en modo laberinto, con HUD y dificultad progresiva."""

    ANCHO = 1200  # Tamaño de ventana por defecto (ancho)
    ALTO = 800  # Tamaño de ventana por defecto (alto)
    TAM_CELDA = 32  # Tamaño base de celda (se recalcula para ajustar al área visible)

    # Diccionario de colores predefinidos para la interfaz del juego en rgb
    # COLORES = {
    #    "fondo": (20, 20, 30),
    #    "hud_fondo": (30, 30, 50),
    #    "texto": (255, 255, 255),
    #    "vidas": (255, 100, 100),
    #    "puntaje": (255, 215, 0),
    #    "acento": (0, 150, 255),
    #    "pared": (50, 50, 70),
    #    "piso": (180, 180, 200),
    #    "jugador": (0, 150, 255),
    #    "enemigo": (255, 50, 50),
    #    "obsequio": (255, 215, 0),
    # }

    def __init__(self, nombre_jugador="Jugador"):
        """Configura pantalla, colores, estados, laberinto, actores y timers."""
        # Configuración de pantalla y reloj
        self.ANCHO = 1200
        self.ALTO = 800
        self.screen = None
        self.reloj = pygame.time.Clock()

        # Colores con un esquema ligeramente distinto para esta pantalla
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

        # Estados y métricas de juego
        self.pausado = False
        self.game_over = False
        self.frame_count = 0  # Frames acumulados (útil para animaciones HUD)
        self.tiempo_transcurrido = 0  # En frames; se muestra como mm:ss en HUD
        self.mostrar_distancia = False  # Overlay opcional para depurar
        self.nombre_jugador = nombre_jugador

        # Obsequios con vencimiento (desaparecen y reaparecen)
        self.tiempo_vida_obsequio = 600  # 10s a 60 FPS
        self.obsequios_timers = {}  # {(col, fila): frames_restantes}

        # Dificultad progresiva (aumenta velocidad del enemigo cada cierto tiempo)
        self.velocidad_inicial_enemigo = 1.5
        self.tiempo_incremento_velocidad = 600  # Cada 10s
        self.incremento_velocidad = 0.2  # Aumento por escalón

        # Carga del laberinto desde archivo JSON y acceso a la matriz
        self.laberinto = Laberinto("laberinto1.json")  # Carga mapa, spawns y obsequios
        self.mapa = self.laberinto.laberinto  # Matriz de 0 (libre) y 1 (muro)

        # Ajuste de tamaño de celda para que el laberinto ocupe la mayor área visible
        # Área disponible deja espacio para el HUD y márgenes laterales
        ancho_disponible = self.ANCHO - 40  # 20px a cada lado
        alto_disponible = self.ALTO - 120  # 80px HUD + 40px margen
        tam_por_ancho = ancho_disponible // len(self.mapa[0])  # Celdas por ancho
        tam_por_alto = alto_disponible // len(self.mapa)  # Celdas por alto
        self.tam_celda = min(tam_por_ancho, tam_por_alto)  # Asegura que quepa

        # Offsets para centrar el laberinto en la pantalla
        ancho_laberinto = len(self.mapa[0]) * self.tam_celda
        alto_laberinto = len(self.mapa) * self.tam_celda
        self.offset_x = (self.ANCHO - ancho_laberinto) // 2
        self.offset_y = (
            (self.ALTO - alto_laberinto) // 2
        ) + 40  # Bajar un poco por el HUD

        # Movimiento por celdas con cooldown (estilo “paso a paso”)
        self.movimiento_por_celdas = True  # Si es False, usa movimiento pixel a pixel
        self.teclas_presionadas = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
        }
        self.ultima_tecla_presionada = None
        self.cooldown_movimiento = 0  # Frames que faltan para permitir otra celda
        self.frames_por_movimiento = 8  # Ajusta la “velocidad” del paso

        # Muros como Rects para colisiones rápidas
        self.muros = self._generar_muros()

        # Radios menores al rect para colisiones más amigables
        radio_jugador = 12
        radio_compu = 12

        # Posiciones de spawn leídas del JSON y convertidas a píxeles + offset
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

        # Crear actores
        self.jugador = Jugador(pos_x_jugador, pos_y_jugador, radio_jugador)
        self.computadora = Computadora(
            pos_x_compu, pos_y_compu, radio_compu, self.velocidad_inicial_enemigo
        )

        # Guardar spawns para respawn al ser capturado
        self.jugador_spawn_x = pos_x_jugador
        self.jugador_spawn_y = pos_y_jugador
        self.computadora_spawn_x = pos_x_compu
        self.computadora_spawn_y = pos_y_compu

        # Posiciones previas para deshacer en colisión (modo pixel a pixel)
        self.pos_anterior_x = self.jugador.jugador_principal.x
        self.pos_anterior_y = self.jugador.jugador_principal.y

        # Timers iniciales de obsequios activos
        self._inicializar_timers_obsequios()

        # Musica Perrona
        musica_perrona = SistemaSonido()
        musica_perrona.musica_perrona()

        ruta_imagen_pasillo = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "data", "pasillos.jpg"
        )
        self.imagen_pasillo = pygame.image.load(ruta_imagen_pasillo).convert_alpha()
        self.imagen_pasillo = pygame.transform.scale(self.imagen_pasillo, (64, 64))

    def _inicializar_timers_obsequios(self):
        """Crea un timer de vida para cada obsequio inicial del laberinto."""
        for posicion in self.laberinto._obsequios.keys():
            self.obsequios_timers[posicion] = self.tiempo_vida_obsequio

    def _generar_muros(self):
        """Convierte cada celda de muro en un Rect para colisiones rápidas."""
        muros = []
        for fila in range(len(self.mapa)):
            for col in range(len(self.mapa[0])):
                if self.mapa[fila][col] == 1:  # 1 = pared
                    x = col * self.tam_celda + self.offset_x
                    y = fila * self.tam_celda + self.offset_y
                    rect = pygame.Rect(x, y, self.tam_celda, self.tam_celda)
                    muros.append(rect)
        return muros

        # return self.laberinto.obtener_rectangulos()

    def _guardar_posicion_anterior(self):
        """Recuerda la posición actual del jugador para poder deshacer."""
        self.pos_anterior_x = self.jugador.jugador_principal.x
        self.pos_anterior_y = self.jugador.jugador_principal.y

    def _revertir_posicion(self):
        """Devuelve al jugador a la posición previa después de chocar."""
        self.jugador.jugador_principal.x = self.pos_anterior_x
        self.jugador.jugador_principal.y = self.pos_anterior_y

    def _detectar_colisiones(self):
        """Devuelve False si el jugador está chocando con algún muro."""
        for muro in self.muros:
            if self.jugador.jugador_principal.colliderect(muro):
                return False
        return True

    def _mover_jugador_por_celdas(self, direccion):
        """Desplaza al jugador exactamente una celda si no hay muro ni sale del área."""
        if direccion == "up":
            nueva_y = self.jugador.jugador_principal.y - self.tam_celda
            if nueva_y >= self.offset_y:  # Límite superior
                temp_rect = pygame.Rect(
                    self.jugador.jugador_principal.x,
                    nueva_y,
                    self.jugador.jugador_principal.width,
                    self.jugador.jugador_principal.height,
                )
                if not any(temp_rect.colliderect(m) for m in self.muros):
                    self.jugador.jugador_principal.y = nueva_y

        elif direccion == "down":
            nueva_y = self.jugador.jugador_principal.y + self.tam_celda
            limite_y_max = self.offset_y + (len(self.mapa) * self.tam_celda)
            if nueva_y + self.jugador.jugador_principal.height <= limite_y_max:
                temp_rect = pygame.Rect(
                    self.jugador.jugador_principal.x,
                    nueva_y,
                    self.jugador.jugador_principal.width,
                    self.jugador.jugador_principal.height,
                )
                if not any(temp_rect.colliderect(m) for m in self.muros):
                    self.jugador.jugador_principal.y = nueva_y

        elif direccion == "left":
            nueva_x = self.jugador.jugador_principal.x - self.tam_celda
            if nueva_x >= self.offset_x:  # Límite izquierdo
                temp_rect = pygame.Rect(
                    nueva_x,
                    self.jugador.jugador_principal.y,
                    self.jugador.jugador_principal.width,
                    self.jugador.jugador_principal.height,
                )
                if not any(temp_rect.colliderect(m) for m in self.muros):
                    self.jugador.jugador_principal.x = nueva_x

        elif direccion == "right":
            nueva_x = self.jugador.jugador_principal.x + self.tam_celda
            limite_x_max = self.offset_x + (len(self.mapa[0]) * self.tam_celda)
            if nueva_x + self.jugador.jugador_principal.width <= limite_x_max:
                temp_rect = pygame.Rect(
                    nueva_x,
                    self.jugador.jugador_principal.y,
                    self.jugador.jugador_principal.width,
                    self.jugador.jugador_principal.height,
                )
                if not any(temp_rect.colliderect(m) for m in self.muros):
                    self.jugador.jugador_principal.x = nueva_x

    def _procesar_eventos_teclado(self):
        """Manejo de movimiento por celdas con cooldown para no avanzar varias de golpe."""
        if self.cooldown_movimiento > 0:  # Aún en espera
            self.cooldown_movimiento -= 1
            return

        keys = pygame.key.get_pressed()  # Estado de flechas

        tecla_actual = None
        if keys[pygame.K_UP]:
            tecla_actual = "up"
        elif keys[pygame.K_DOWN]:
            tecla_actual = "down"
        elif keys[pygame.K_LEFT]:
            tecla_actual = "left"
        elif keys[pygame.K_RIGHT]:
            tecla_actual = "right"

        if tecla_actual:  # Mueve una celda y activa cooldown
            self._mover_jugador_por_celdas(tecla_actual)
            self.cooldown_movimiento = self.frames_por_movimiento

        self.ultima_tecla_presionada = tecla_actual  # Útil para depurar

    def _verificar_captura(self):
        """Si la computadora alcanza al jugador, resta vida y hace respawn; si sin vidas, game over."""
        dx = (
            self.jugador.jugador_principal.centerx
            - self.computadora.computadora_principal.centerx
        )
        dy = (
            self.jugador.jugador_principal.centery
            - self.computadora.computadora_principal.centery
        )
        distancia = math.sqrt(dx**2 + dy**2)

        # Radio de captura con holgura de 5 px
        if distancia < self.jugador.radio + self.computadora.radio + 5:
            self.jugador.perder_vida()
            if not self.jugador.esta_vivo():
                self.game_over = True
                return True

            # Respawn en los puntos iniciales
            self.jugador.jugador_principal.x = self.jugador_spawn_x
            self.jugador.jugador_principal.y = self.jugador_spawn_y
            self.computadora.computadora_principal.x = self.computadora_spawn_x
            self.computadora.computadora_principal.y = self.computadora_spawn_y

            # Limpia camino de BFS para que recalcule desde cero
            self.computadora._bfs_camino = None

        return False

    def _actualizar(self):
        """Actualiza movimiento, IA, obsequios, dificultad y tiempo, si no está pausado o en game over."""
        if self.pausado or self.game_over:
            return

        self.frame_count += 1  # Avanza contador de frames

        # Movimiento del jugador
        if self.movimiento_por_celdas:
            self._procesar_eventos_teclado()
        else:
            # Modo “legacy”: movimiento suave pixel a pixel con límites y colisión
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

            # Aplica límites según el área del laberinto (considera offset y tamaño del rect)
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

            # Si chocó, deshacer al punto anterior
            if not self._detectar_colisiones():
                self._revertir_posicion()

        # Enemigo persigue con BFS sobre la grilla del laberinto
        self.computadora.perseguir_bfs(
            self.jugador, self.mapa, self.tam_celda, self.offset_x, self.offset_y
        )

        # Timers de obsequios y su reposición al vencer
        self._actualizar_timers_obsequios()

        # Recolección de obsequios por celda
        self._verificar_recoleccion_obsequios()

        # Verifica captura del jugador
        self._verificar_captura()

        # Escala de dificultad con el tiempo
        self._aumentar_dificultad()

        # Tiempo total transcurrido (en frames)
        self.tiempo_transcurrido += 1

    def _verificar_recoleccion_obsequios(self):
        """Si el jugador pisa una celda con obsequio, suma puntos y reposiciona otro."""
        # Centro actual del jugador en píxeles
        jug_cx, jug_cy = self.jugador.jugador_principal.center
        # Coordenadas relativas al laberinto (quitando offsets)
        x_rel = jug_cx - self.offset_x
        y_rel = jug_cy - self.offset_y
        # Celda donde está parado
        celda_x = x_rel // self.tam_celda
        celda_y = y_rel // self.tam_celda
        posicion_celda = (celda_x, celda_y)

        # Si hay obsequio en esta celda, súmalo y renueva el objeto
        puntos = self.laberinto.recolectar_obsequio(posicion_celda)
        if puntos > 0:
            self.jugador.sumar_puntos(puntos)
            if posicion_celda in self.obsequios_timers:
                del self.obsequios_timers[posicion_celda]
            self._crear_nuevo_obsequio()  # Reponer en otra celda vacía

    def _actualizar_timers_obsequios(self):
        """Resta 1 frame a cada timer; si expira, quita el obsequio y crea otro."""
        obsequios_expirados = []
        for posicion, tiempo_restante in self.obsequios_timers.items():
            self.obsequios_timers[posicion] = tiempo_restante - 1
            if self.obsequios_timers[posicion] <= 0:
                obsequios_expirados.append(posicion)

        for posicion in obsequios_expirados:
            if posicion in self.laberinto._obsequios:
                valor = self.laberinto._obsequios[
                    posicion
                ].valor  # Mantén el mismo valor
                del self.laberinto._obsequios[posicion]
                del self.obsequios_timers[posicion]
                self._crear_nuevo_obsequio(valor)  # Reponer con ese valor

    def _crear_nuevo_obsequio(self, valor=10):
        """Coloca un obsequio en una celda libre aleatoria que no sea spawn ni muro."""
        import random

        from models.obsequio import Obsequio

        posiciones_validas = []
        for fila in range(len(self.mapa)):
            for col in range(len(self.mapa[0])):
                posicion = (col, fila)
                if (
                    self.mapa[fila][col] == 0
                    and posicion not in self.laberinto._obsequios
                    and posicion != tuple(self.laberinto.jugador_inicio)
                    and posicion != tuple(self.laberinto.computadora_inicio)
                ):
                    posiciones_validas.append(posicion)

        if posiciones_validas:
            nueva_posicion = random.choice(posiciones_validas)
            self.laberinto._obsequios[nueva_posicion] = Obsequio(nueva_posicion, valor)
            self.obsequios_timers[nueva_posicion] = self.tiempo_vida_obsequio

    def _aumentar_dificultad(self):
        """Cada cierto tiempo incrementa la velocidad del enemigo."""
        if (
            self.tiempo_transcurrido % self.tiempo_incremento_velocidad == 0
            and self.tiempo_transcurrido > 0
        ):
            self.computadora.velocidad += self.incremento_velocidad

    def _renderizar(self):
        """Dibuja laberinto, obsequios, actores, overlays y HUD; luego actualiza pantalla."""
        self.screen.fill(self.COLORES["fondo"])

        # Laberinto
        self._dibujar_laberinto()

        # Obsequios animados
        self.laberinto.dibujar_obsequios(
            self.screen, self.frame_count, self.tam_celda, self.offset_x, self.offset_y
        )

        # Actores
        self.jugador.dibujar_jugador_principal(self.screen)
        self.computadora.dibujar_computadora_principal(self.screen)

        # Debug opcional
        if self.mostrar_distancia:
            self._dibujar_linea_distancia()

        # HUD y overlays
        self._dibujar_hud()
        if self.pausado:
            self._dibujar_pausa()
        if self.game_over:
            self._dibujar_game_over()

        pygame.display.flip()  # Presenta el frame

    def _dibujar_linea_distancia(self):
        """Para depurar: línea entre jugador y enemigo y texto con distancia."""
        pos_jugador = self.jugador.jugador_principal.center
        pos_enemigo = self.computadora.computadora_principal.center
        pygame.draw.line(self.screen, (255, 100, 100), pos_jugador, pos_enemigo, 1)

        dx = pos_enemigo[0] - pos_jugador[0]
        dy = pos_enemigo[1] - pos_jugador[1]
        distancia = math.sqrt(dx**2 + dy**2)

        dist_texto = self.fuente_pequena.render(
            f"Dist: {int(distancia)}", True, (255, 255, 255)
        )
        self.screen.blit(dist_texto, (pos_jugador[0] + 20, pos_jugador[1] - 20))

    def _dibujar_laberinto(self):
        """Dibuja cada celda como pared o piso con borde tenue para guiar al jugador."""
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
                    # pygame.draw.rect(
                    #    self.screen,
                    #    self.COLORES["piso"],
                    #   (x, y, self.tam_celda, self.tam_celda),
                    # )
                    self.screen.blit(self.imagen_pasillo, (x, y))

                    pygame.draw.rect(
                        self.screen,
                        (100, 100, 120),
                        (x, y, self.tam_celda, self.tam_celda),
                        1,
                    )

    def _dibujar_hud(self):
        """Panel superior con nombre, vidas, puntaje, dificultad, tiempo y controles."""
        # Panel base y línea inferior
        panel_rect = pygame.Rect(0, 0, self.ANCHO, 80)
        pygame.draw.rect(self.screen, self.COLORES["hud_fondo"], panel_rect)
        pygame.draw.line(
            self.screen, self.COLORES["acento"], (0, 80), (self.ANCHO, 80), 2
        )

        # Nombre del jugador
        nombre_surf = self.fuente_pequena.render(
            f"Jugador: {self.nombre_jugador}", True, self.COLORES["texto"]
        )
        self.screen.blit(nombre_surf, (20, 15))

        # Vidas dibujadas como corazones simples
        x_vidas = 20
        y_vidas = 45
        for i in range(self.jugador._vidas):
            cx = x_vidas + (i * 35)
            pygame.draw.circle(
                self.screen, self.COLORES["vidas"], (cx + 5, y_vidas + 5), 5
            )
            pygame.draw.circle(
                self.screen, self.COLORES["vidas"], (cx + 15, y_vidas + 5), 5
            )
            puntos = [
                (cx, y_vidas + 6),
                (cx + 20, y_vidas + 6),
                (cx + 10, y_vidas + 18),
            ]
            pygame.draw.polygon(self.screen, self.COLORES["vidas"], puntos)

        # Puntaje con estrella dibujada a mano
        x_puntaje = 200
        y_puntaje = 45
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

        puntaje_surf = self.fuente_hud.render(
            f"{self.jugador._puntaje}", True, self.COLORES["puntaje"]
        )
        self.screen.blit(puntaje_surf, (x_puntaje + 20, y_puntaje))

        # Dificultad relativa (velocidad / velocidad inicial)
        nivel_dificultad = self.computadora.velocidad / self.velocidad_inicial_enemigo
        dificultad_surf = self.fuente_pequena.render(
            f"Dificultad: {nivel_dificultad:.1f}x", True, (255, 100, 100)
        )
        self.screen.blit(dificultad_surf, (400, 15))

        # Tiempo en mm:ss
        tiempo_min = self.tiempo_transcurrido // 3600
        tiempo_seg = (self.tiempo_transcurrido % 3600) // 60
        tiempo_surf = self.fuente_pequena.render(
            f"Tiempo: {tiempo_min:02d}:{tiempo_seg:02d}", True, self.COLORES["texto"]
        )
        self.screen.blit(tiempo_surf, (400, 45))

        # Controles de ayuda al usuario
        controles_surf = self.fuente_pequena.render(
            "Flechas: Mover | P: Pausa | ESC: Salir | D: Debug", True, (150, 150, 150)
        )
        controles_rect = controles_surf.get_rect(right=self.ANCHO - 20, centery=40)
        self.screen.blit(controles_surf, controles_rect)

    def _dibujar_pausa(self):
        """Overlay translúcido y texto de pausa."""
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
        """Overlay de game over, guarda puntaje una vez y muestra métricas finales."""
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

        tiempo_segundos = self.tiempo_transcurrido // 60
        tiempo_texto = self.fuente_pequena.render(
            f"Tiempo: {tiempo_segundos} segundos", True, (200, 200, 200)
        )
        tiempo_rect = tiempo_texto.get_rect(
            center=(self.ANCHO // 2, self.ALTO // 2 + 10)
        )
        self.screen.blit(tiempo_texto, tiempo_rect)

        velocidad_texto = self.fuente_pequena.render(
            f"Nivel de dificultad: {self.computadora.velocidad:.1f}x",
            True,
            (200, 200, 200),
        )
        velocidad_rect = velocidad_texto.get_rect(
            center=(self.ANCHO // 2, self.ALTO // 2 + 50)
        )
        self.screen.blit(velocidad_texto, velocidad_rect)

        instruccion = self.fuente_pequena.render(
            "Presiona cualquier tecla para volver", True, (150, 150, 150)
        )
        instruccion_rect = instruccion.get_rect(
            center=(self.ANCHO // 2, self.ALTO // 2 + 120)
        )
        self.screen.blit(instruccion, instruccion_rect)

    def _guardar_en_salon_fama(self):
        """Crea un registro y lo guarda en el salón de la fama."""
        from models.registro import Registro
        from models.salon_fama import SalonFama

        salon = SalonFama()
        registro = Registro(
            nombre_jugador=self.nombre_jugador,
            puntaje=self.jugador._puntaje,
            laberinto=self.laberinto.nombre,
        )
        salon.guardar_puntaje(registro)
        print(
            f"Puntaje guardado en el Salón de la Fama: {self.jugador._puntaje} puntos"
        )

    def _dibujar_victoria(self):
        """Overlay de victoria (no se usa en modo infinito, se deja por si se activa)."""
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
        """Lee eventos de ventana y teclado; maneja pausa, debug, modo de movimiento y salida."""
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

                # En game over, cualquier tecla (menos 'p') sale
                if self.game_over and evento.key != pygame.K_p:
                    return "salir"

        return None  # No hay acción global

    def ejecutar(self):
        """Crea la ventana, inicializa fuentes y corre el loop hasta salir."""
        if not pygame.get_init():
            pygame.init()

        self.screen = pygame.display.set_mode((self.ANCHO, self.ALTO))
        pygame.display.set_caption("CodeRunner - Modo Laberinto")

        # Fuentes para títulos y HUD
        self.fuente_titulo = pygame.font.Font(None, 48)
        self.fuente_hud = pygame.font.Font(None, 32)
        self.fuente_pequena = pygame.font.Font(None, 24)

        ejecutando = True
        while ejecutando:
            self.reloj.tick(60)  # 60 FPS
            resultado = self.manejar_eventos()
            if resultado == "salir":
                ejecutando = False

            self._actualizar()
            self._renderizar()

        # No se cierra pygame aquí para retornar al menú sin destruir el contexto
        # pygame.quit()
