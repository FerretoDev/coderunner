import math  # Para animaciones y cálculos trigonométricos del HUD
import os

import pygame  # Motor de eventos, dibujo y tiempo

from config.config import Colores, ConfigJuego
from jugabilidad.gestores.gestor_dificultad import GestorDificultad
from jugabilidad.gestores.gestor_movimiento import GestorMovimiento
from jugabilidad.gestores.gestor_obsequios import GestorObsequios
from mundo.laberinto import Laberinto
from personajes.computadora import Computadora
from personajes.jugador import Jugador
from servicios.sistema_sonido import SistemaSonido
from utilidades.coordenadas import ConversorCoordenadas


class PantallaJuego:
    """Pantalla principal del juego en modo laberinto, con HUD y dificultad progresiva."""

    def __init__(self, nombre_jugador="Jugador"):
        """Configura pantalla, colores, estados, laberinto, actores y timers."""
        # Configuración de pantalla y reloj
        # Obtener tamaño real de la pantalla actual
        pantalla_actual = pygame.display.get_surface()
        if pantalla_actual:
            self.ANCHO = pantalla_actual.get_width()
            self.ALTO = pantalla_actual.get_height()
        else:
            # Fallback por si acaso
            self.ANCHO = 1200
            self.ALTO = 800

        self.screen = None
        self.reloj = pygame.time.Clock()

        # Estados y métricas de juego
        self.pausado = False
        self.game_over = False
        self.game_over_timer = 0  # Timer para espera en game over
        self.frame_count = 0  # Frames acumulados (útil para animaciones HUD)
        self.tiempo_transcurrido = 0  # En frames; se muestra como mm:ss en HUD
        self.mostrar_distancia = False  # Overlay opcional para depurar
        self.nombre_jugador = nombre_jugador

        # Datos del puntaje final para retornar
        self.puntaje_final = None
        self.nombre_laberinto = None

        # Obsequios con vencimiento (desaparecen y reaparecen)
        self.tiempo_vida_obsequio = ConfigJuego.segundos_a_frames(
            ConfigJuego.SEGUNDOS_VIDA_OBSEQUIO
        )
        self.obsequios_timers = {}  # {(col, fila): frames_restantes}

        # Dificultad progresiva (aumenta velocidad del enemigo cada cierto tiempo)
        self.velocidad_inicial_enemigo = ConfigJuego.VELOCIDAD_INICIAL_ENEMIGO
        self.tiempo_incremento_velocidad = ConfigJuego.segundos_a_frames(
            ConfigJuego.SEGUNDOS_INCREMENTO_VELOCIDAD
        )
        self.incremento_velocidad = ConfigJuego.INCREMENTO_VELOCIDAD

        # Carga del laberinto desde archivo JSON y acceso a la matriz
        # Intenta cargar el laberinto activo, si no existe usa el predeterminado
        from config.config_laberinto import ConfigLaberinto

        ruta_laberinto = ConfigLaberinto.obtener_laberinto_activo()
        if not ruta_laberinto:
            ruta_laberinto = "src/data/laberintos/laberinto1.json"

        self.laberinto = Laberinto(ruta_laberinto)  # Carga mapa, spawns y obsequios
        self.mapa = self.laberinto.laberinto  # Matriz de 0 (libre) y 1 (muro)

        # Ajuste de tamaño de celda para que el laberinto ocupe la mayor área visible
        # Área disponible deja espacio para el HUD y márgenes laterales
        ancho_disponible = self.ANCHO - 40  # 20px a cada lado
        alto_disponible = self.ALTO - 140  # 95px HUD + 45px margen
        tam_por_ancho = ancho_disponible // len(self.mapa[0])  # Celdas por ancho
        tam_por_alto = alto_disponible // len(self.mapa)  # Celdas por alto
        self.tam_celda = min(tam_por_ancho, tam_por_alto)  # Asegura que quepa

        # Offsets para centrar el laberinto en la pantalla
        ancho_laberinto = len(self.mapa[0]) * self.tam_celda
        alto_laberinto = len(self.mapa) * self.tam_celda
        self.offset_x = (self.ANCHO - ancho_laberinto) // 2
        self.offset_y = (
            (self.ALTO - alto_laberinto) // 2
        ) + 50  # Bajar un poco más por el HUD

        # Movimiento por celdas con cooldown (estilo "paso a paso")
        self.movimiento_por_celdas = True  # Si es False, usa movimiento pixel a pixel
        self.teclas_presionadas = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
        }
        self.ultima_tecla_presionada = None
        self.cooldown_movimiento = 0  # Frames que faltan para permitir otra celda
        self.frames_por_movimiento = ConfigJuego.FRAMES_COOLDOWN_MOVIMIENTO

        # Radios de personajes desde config
        radio_jugador = ConfigJuego.RADIO_JUGADOR
        radio_compu = ConfigJuego.RADIO_ENEMIGO

        # Calcular posiciones de spawn usando Laberinto
        pos_x_jugador, pos_y_jugador = self.laberinto.calcular_posicion_spawn(
            self.laberinto.jugador_inicio,
            radio_jugador,
            self.tam_celda,
            self.offset_x,
            self.offset_y,
        )
        pos_x_compu, pos_y_compu = self.laberinto.calcular_posicion_spawn(
            self.laberinto.computadora_inicio,
            radio_compu,
            self.tam_celda,
            self.offset_x,
            self.offset_y,
        )

        # Crear actores
        self.jugador = Jugador(pos_x_jugador, pos_y_jugador, radio_jugador)
        self.computadora = Computadora(
            pos_x_compu, pos_y_compu, radio_compu, self.velocidad_inicial_enemigo
        )

        # Generar muros usando Laberinto
        self.muros = self.laberinto.generar_muros_rect(
            self.tam_celda, self.offset_x, self.offset_y
        )

        # Posiciones previas para deshacer en colisión (modo pixel a pixel)
        self.pos_anterior_x = self.jugador.jugador_principal.x
        self.pos_anterior_y = self.jugador.jugador_principal.y

        # Gestor de movimiento (maneja input, colisiones y movimiento del jugador)
        self.gestor_movimiento = GestorMovimiento(
            self.jugador,
            self.muros,
            self.tam_celda,
            self.offset_x,
            self.offset_y,
            self.mapa,
            self.frames_por_movimiento,
            self.movimiento_por_celdas,
        )

        # Gestor de obsequios (maneja timers, recoleccion y creación)
        self.gestor_obsequios = GestorObsequios(
            self.laberinto, self.tiempo_vida_obsequio
        )

        # Gestor de dificultad progresiva
        self.gestor_dificultad = GestorDificultad(
            intervalo_frames=self.tiempo_incremento_velocidad,
            incremento=self.incremento_velocidad,
        )

        # Sistema de sonido (singleton) y reproducir música de fondo
        self.sistema_sonido = SistemaSonido()
        self.sistema_sonido.reproducir_musica_fondo()

        ruta_imagen_pasillo = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "..",
            "data",
            "pasillos.jpg",
        )
        self.imagen_pasillo = pygame.image.load(ruta_imagen_pasillo).convert_alpha()
        self.imagen_pasillo = pygame.transform.scale(self.imagen_pasillo, (64, 64))

    def _inicializar_timers_obsequios(self):
        """Crea un timer de vida para cada obsequio inicial del laberinto."""
        for posicion in self.laberinto._obsequios.keys():
            self.obsequios_timers[posicion] = self.tiempo_vida_obsequio

    def _verificar_captura(self):
        """Si la computadora alcanza al jugador, resta vida y hace respawn; si sin vidas, game over."""
        if self.computadora.verificar_captura(self.jugador, ConfigJuego.MARGEN_CAPTURA):
            # Reproducir sonido de captura
            self.sistema_sonido.reproducir_captura()

            self.jugador.perder_vida()
            if not self.jugador.esta_vivo():
                self.game_over = True
                self.game_over_timer = ConfigJuego.segundos_a_frames(
                    ConfigJuego.SEGUNDOS_ESPERA_GAME_OVER
                )
                # Guardar datos para retornar al final
                self.puntaje_final = self.jugador.puntaje
                self.nombre_laberinto = self.laberinto.nombre
                return True

            # Respawn usando métodos de los personajes
            self.jugador.respawn()
            self.computadora.respawn()

        return False

    def _actualizar(self):
        """Actualiza movimiento, IA, obsequios, dificultad y tiempo, si no está pausado o en game over."""
        if self.pausado:
            return

        # En game over, solo actualizar el timer de espera
        if self.game_over:
            if self.game_over_timer > 0:
                self.game_over_timer -= 1
            return

        self.frame_count += 1  # Avanza contador de frames

        # Movimiento del jugador
        self.gestor_movimiento.procesar_entrada_teclado()

        # Enemigo persigue con BFS sobre la grilla del laberinto
        self.computadora.perseguir_bfs(
            self.jugador, self.mapa, self.tam_celda, self.offset_x, self.offset_y
        )

        # Timers de obsequios y su reposición al vencer
        self.gestor_obsequios.actualizar()

        # Recolección de obsequios por celda
        self._verificar_recoleccion_obsequios()

        # Verifica captura del jugador
        self._verificar_captura()

        # Escala de dificultad con el tiempo
        self.gestor_dificultad.actualizar_velocidad(
            self.computadora, self.tiempo_transcurrido, self.velocidad_inicial_enemigo
        )

        # Tiempo total transcurrido (en frames)
        self.tiempo_transcurrido += 1

    def _verificar_recoleccion_obsequios(self):
        """Si el jugador pisa una celda con obsequio, suma puntos y reposiciona otro."""
        # Centro actual del jugador en píxeles
        jug_cx, jug_cy = self.jugador.jugador_principal.center
        # Celda donde está parado
        fila, col = ConversorCoordenadas.pixel_a_celda(
            jug_cx, jug_cy, self.tam_celda, self.offset_x, self.offset_y
        )
        posicion_celda = (col, fila)

        # Verificar y recolectar obsequio usando el gestor
        puntos = self.gestor_obsequios.verificar_recoleccion(posicion_celda)
        if puntos > 0:
            # Reproducir sonido de recolección
            self.sistema_sonido.reproducir_obsequio()
            self.jugador.sumar_puntos(puntos)

    def _renderizar(self):
        """Dibuja laberinto, obsequios, actores, overlays y HUD; luego actualiza pantalla."""
        self.screen.fill(Colores.FONDO)

        # Laberinto
        self._dibujar_laberinto()

        # Obsequios animados
        self.laberinto.dibujar_obsequios(
            self.screen, self.frame_count, self.tam_celda, self.offset_x, self.offset_y
        )

        # Actores
        self.jugador.dibujar_jugador_principal(self.screen)
        self.computadora.dibujar_computadora_principal(self.screen)

        # HUD y overlays
        self._dibujar_hud()
        if self.pausado:
            self._dibujar_pausa()
        if self.game_over:
            self._dibujar_game_over()

        pygame.display.flip()  # Presenta el frame

    # funcion irrelevante, eliminar a futuro
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
        """Dibuja el laberinto con estética mitológica griega (Mito de Teseo y el Minotauro)."""
        import math

        for fila in range(len(self.mapa)):
            for col in range(len(self.mapa[0])):
                x = col * self.tam_celda + self.offset_x
                y = fila * self.tam_celda + self.offset_y

                if self.mapa[fila][col] == 1:
                    # === MUROS DE PIEDRA ANTIGUA (ESTILO GRIEGO) ===
                    # Base de mármol/piedra caliza
                    color_base = (210, 195, 170)  # Tono mármol beige
                    pygame.draw.rect(
                        self.screen,
                        color_base,
                        (x, y, self.tam_celda, self.tam_celda),
                    )

                    # Textura de bloques de piedra (vetas y grietas)
                    block_size = self.tam_celda // 3
                    for i in range(3):
                        for j in range(3):
                            bx = x + i * block_size + 1
                            by = y + j * block_size + 1
                            # Variación de color para simular vetas de mármol
                            veta = ((i * 7 + j * 5 + fila * 3 + col * 2) % 15) - 7
                            color_piedra = (
                                min(255, max(0, 210 + veta)),
                                min(255, max(0, 195 + veta)),
                                min(255, max(0, 170 + veta)),
                            )
                            pygame.draw.rect(
                                self.screen,
                                color_piedra,
                                (bx, by, block_size - 2, block_size - 2),
                            )
                            # Líneas de separación entre bloques (mortero)
                            pygame.draw.line(
                                self.screen,
                                (180, 165, 145),
                                (bx, by),
                                (bx + block_size - 2, by),
                                1,
                            )
                            pygame.draw.line(
                                self.screen,
                                (180, 165, 145),
                                (bx, by),
                                (bx, by + block_size - 2),
                                1,
                            )

                    # Borde de bronce/terracota (pilares antiguos)
                    pygame.draw.rect(
                        self.screen,
                        (184, 115, 51),  # Bronce oxidado
                        (x, y, self.tam_celda, self.tam_celda),
                        2,
                    )

                    # Sombra interior para profundidad
                    pygame.draw.line(
                        self.screen,
                        (150, 140, 120),
                        (x + 2, y + 2),
                        (x + self.tam_celda - 2, y + 2),
                        1,
                    )
                    pygame.draw.line(
                        self.screen,
                        (150, 140, 120),
                        (x + 2, y + 2),
                        (x + 2, y + self.tam_celda - 2),
                        1,
                    )
                else:
                    # === PASILLOS CON MOSAICO GRECO-ROMANO ===
                    # Base terracota/arcilla
                    base_terracota = (156, 102, 68)  # Terracota
                    pygame.draw.rect(
                        self.screen,
                        base_terracota,
                        (x, y, self.tam_celda, self.tam_celda),
                    )

                    # Patrón de mosaico (baldosas pequeñas)
                    tile_size = self.tam_celda // 4
                    for tx in range(4):
                        for ty in range(4):
                            tile_x = x + tx * tile_size + 1
                            tile_y = y + ty * tile_size + 1

                            # Variación de color para mosaico (crema/beige/terracota)
                            patron = (tx + ty + fila + col) % 3
                            if patron == 0:
                                tile_color = (198, 156, 109)  # Crema oscuro
                            elif patron == 1:
                                tile_color = (176, 141, 105)  # Beige
                            else:
                                tile_color = (166, 123, 91)  # Terracota claro

                            pygame.draw.rect(
                                self.screen,
                                tile_color,
                                (tile_x, tile_y, tile_size - 2, tile_size - 2),
                            )

                    # Detalle central: símbolo griego ocasional
                    if (fila + col) % 7 == 0:
                        center_x = x + self.tam_celda // 2
                        center_y = y + self.tam_celda // 2
                        # Pequeña cruz griega o meandro
                        pygame.draw.circle(
                            self.screen,
                            (184, 115, 51),  # Bronce
                            (center_x, center_y),
                            2,
                        )

                    # Borde sutil de separación
                    pygame.draw.rect(
                        self.screen,
                        (140, 90, 60),
                        (x, y, self.tam_celda, self.tam_celda),
                        1,
                    )

    def _dibujar_hud(self):
        """Panel superior con nombre, vidas, puntaje, dificultad, tiempo y controles - estilo arcade."""
        # Panel base más alto
        panel_rect = pygame.Rect(0, 0, self.ANCHO, 95)
        pygame.draw.rect(self.screen, (25, 30, 45), panel_rect)

        # Línea superior brillante
        pygame.draw.line(self.screen, (0, 200, 255), (0, 0), (self.ANCHO, 0), 3)

        # Doble línea inferior (estilo arcade)
        pygame.draw.line(self.screen, (0, 200, 255), (0, 93), (self.ANCHO, 93), 2)
        pygame.draw.line(self.screen, (50, 255, 100), (0, 96), (self.ANCHO, 96), 2)

        # === FILA SUPERIOR ===
        # IZQUIERDA: Nombre del jugador
        nombre_texto = f"{self.nombre_jugador}"
        nombre_surf = self.fuente_pequena.render(nombre_texto, False, (255, 255, 255))
        self.screen.blit(nombre_surf, (15, 8))

        # CENTRO: Puntaje con estrella
        x_puntaje = self.ANCHO // 2 - 80
        y_puntaje = 8

        # Caja del puntaje
        puntaje_box = pygame.Rect(x_puntaje - 5, y_puntaje - 3, 160, 28)
        pygame.draw.rect(self.screen, (40, 45, 60), puntaje_box, border_radius=4)
        pygame.draw.rect(self.screen, (255, 220, 60), puntaje_box, 2, border_radius=4)

        # Estrella animada más pequeña
        x_estrella = x_puntaje + 5
        y_estrella_center = y_puntaje + 11
        radio_ext = 8
        radio_int = 3
        puntos_estrella = []
        rotacion = (self.frame_count % 120) * 0.05
        for i in range(10):
            angulo = rotacion + math.pi / 2 + (i * math.pi / 5)
            radio = radio_ext if i % 2 == 0 else radio_int
            px = x_estrella + radio * math.cos(angulo)
            py = y_estrella_center - radio * math.sin(angulo)
            puntos_estrella.append((px, py))
        pygame.draw.polygon(self.screen, (255, 220, 60), puntos_estrella)

        # Texto del puntaje
        puntaje_texto = f"{self.jugador.puntaje:06d}"
        puntaje_surf = self.fuente_pequena.render(puntaje_texto, False, (255, 220, 60))
        self.screen.blit(puntaje_surf, (x_puntaje + 22, y_puntaje + 3))

        # DERECHA: Tiempo
        tiempo_min = self.tiempo_transcurrido // 3600
        tiempo_seg = (self.tiempo_transcurrido % 3600) // 60
        tiempo_texto = f"{tiempo_min:02d}:{tiempo_seg:02d}"
        tiempo_surf = self.fuente_pequena.render(tiempo_texto, False, (200, 230, 255))
        tiempo_rect = tiempo_surf.get_rect(right=self.ANCHO - 15, y=8)
        self.screen.blit(tiempo_surf, tiempo_rect)

        # === FILA INFERIOR ===
        # IZQUIERDA: Vidas con corazones compactos
        x_vidas = 15
        y_vidas = 48
        for i in range(self.jugador.vidas):
            cx = x_vidas + (i * 28)

            # Corazón más pequeño
            pygame.draw.circle(self.screen, (255, 80, 120), (cx + 4, y_vidas + 4), 4)
            pygame.draw.circle(self.screen, (255, 80, 120), (cx + 12, y_vidas + 4), 4)
            puntos = [
                (cx, y_vidas + 5),
                (cx + 16, y_vidas + 5),
                (cx + 8, y_vidas + 15),
            ]
            pygame.draw.polygon(self.screen, (255, 80, 120), puntos)
            # Brillo
            pygame.draw.circle(self.screen, (255, 150, 180), (cx + 6, y_vidas + 2), 2)

        # CENTRO: Dificultad con barra
        x_dif = self.ANCHO // 2 - 70
        y_dif = 50
        nivel_dificultad = self.computadora.velocidad / self.velocidad_inicial_enemigo

        # Texto de dificultad
        dif_texto = f"Nivel {nivel_dificultad:.1f}x"
        dif_surf = self.fuente_pequena.render(dif_texto, False, (255, 100, 100))
        self.screen.blit(dif_surf, (x_dif, y_dif))

        # Barra de progreso debajo del texto
        barra_ancho = 120
        barra_alto = 8
        barra_x = x_dif
        barra_y = y_dif + 20

        # Fondo de la barra
        pygame.draw.rect(
            self.screen,
            (40, 40, 50),
            (barra_x, barra_y, barra_ancho, barra_alto),
            border_radius=4,
        )

        # Relleno según dificultad (máximo 3x)
        progreso = min(1.0, (nivel_dificultad - 1.0) / 2.0)
        relleno_ancho = int(barra_ancho * progreso)

        # Color según nivel
        if nivel_dificultad < 1.5:
            color_barra = (50, 255, 100)  # Verde
        elif nivel_dificultad < 2.0:
            color_barra = (255, 220, 60)  # Amarillo
        else:
            color_barra = (255, 80, 120)  # Rojo

        if relleno_ancho > 0:
            pygame.draw.rect(
                self.screen,
                color_barra,
                (barra_x, barra_y, relleno_ancho, barra_alto),
                border_radius=4,
            )

        # Borde de la barra
        pygame.draw.rect(
            self.screen,
            (100, 100, 120),
            (barra_x, barra_y, barra_ancho, barra_alto),
            1,
            border_radius=4,
        )

        # DERECHA: Controles compactos
        controles_texto = "WASD: Mover  P: Pausa  ESC: Salir"
        controles_surf = self.fuente_pequena.render(
            controles_texto, False, (120, 140, 160)
        )
        controles_rect = controles_surf.get_rect(right=self.ANCHO - 15, y=70)
        self.screen.blit(controles_surf, controles_rect)

    def _dibujar_pausa(self):
        """Overlay translúcido y texto de pausa con estilo arcade."""
        # Overlay oscuro
        overlay = pygame.Surface((self.ANCHO, self.ALTO))
        overlay.set_alpha(200)
        overlay.fill((15, 20, 35))
        self.screen.blit(overlay, (0, 0))

        # Caja central con efecto neón
        caja_ancho = 500
        caja_alto = 250
        caja_x = (self.ANCHO - caja_ancho) // 2
        caja_y = (self.ALTO - caja_alto) // 2

        caja_rect = pygame.Rect(caja_x, caja_y, caja_ancho, caja_alto)
        pygame.draw.rect(self.screen, (30, 35, 50), caja_rect, border_radius=15)

        # Triple borde brillante (efecto neón)
        pygame.draw.rect(self.screen, (0, 200, 255), caja_rect, 4, border_radius=15)
        caja_rect2 = pygame.Rect(caja_x - 3, caja_y - 3, caja_ancho + 6, caja_alto + 6)
        pygame.draw.rect(self.screen, (0, 150, 200), caja_rect2, 2, border_radius=15)
        caja_rect3 = pygame.Rect(
            caja_x - 6, caja_y - 6, caja_ancho + 12, caja_alto + 12
        )
        pygame.draw.rect(self.screen, (0, 100, 150), caja_rect3, 1, border_radius=15)

        # Título PAUSA con triple sombra
        y_titulo = caja_y + 60
        # Sombra 3
        titulo_s3 = self.fuente_titulo.render("PAUSA", False, (20, 30, 50))
        titulo_s3_rect = titulo_s3.get_rect(center=(self.ANCHO // 2 + 4, y_titulo + 4))
        self.screen.blit(titulo_s3, titulo_s3_rect)
        # Sombra 2
        titulo_s2 = self.fuente_titulo.render("PAUSA", False, (0, 200, 255))
        titulo_s2_rect = titulo_s2.get_rect(center=(self.ANCHO // 2 + 2, y_titulo + 2))
        self.screen.blit(titulo_s2, titulo_s2_rect)
        # Texto principal
        titulo = self.fuente_titulo.render("PAUSA", False, (255, 255, 255))
        titulo_rect = titulo.get_rect(center=(self.ANCHO // 2, y_titulo))
        self.screen.blit(titulo, titulo_rect)

        # Línea decorativa
        linea_y = y_titulo + 50
        pygame.draw.line(
            self.screen,
            (0, 200, 255),
            (self.ANCHO // 2 - 150, linea_y),
            (self.ANCHO // 2 + 150, linea_y),
            2,
        )

        # Instrucciones con icono
        y_instruccion = linea_y + 40
        instruccion = self.fuente_hud.render(
            "Presiona P para continuar", False, (100, 255, 100)
        )
        instruccion_rect = instruccion.get_rect(center=(self.ANCHO // 2, y_instruccion))
        self.screen.blit(instruccion, instruccion_rect)

        # Tip adicional
        tip = self.fuente_pequena.render(
            "ESC para salir al menú", False, (150, 170, 200)
        )
        tip_rect = tip.get_rect(center=(self.ANCHO // 2, y_instruccion + 35))
        self.screen.blit(tip, tip_rect)

    def _dibujar_game_over(self):
        """Overlay de game over mostrando las métricas finales de la partida."""
        if not hasattr(self, "_musica_pausada"):
            # Detener la música al llegar a game over
            self.sistema_sonido.pausar_musica()
            self._musica_pausada = True

        overlay = pygame.Surface((self.ANCHO, self.ALTO))
        overlay.set_alpha(200)
        overlay.fill(Colores.OVERLAY_OSCURO)
        self.screen.blit(overlay, (0, 0))

        # Caja para mostrar información
        caja_rect = pygame.Rect(self.ANCHO // 2 - 350, 100, 700, 450)
        pygame.draw.rect(self.screen, (40, 40, 60), caja_rect, border_radius=15)
        pygame.draw.rect(self.screen, Colores.VIDAS, caja_rect, 3, border_radius=15)

        titulo = self.fuente_titulo.render("GAME OVER", True, Colores.VIDAS)
        titulo_rect = titulo.get_rect(center=(self.ANCHO // 2, 140))
        self.screen.blit(titulo, titulo_rect)

        # Información de la partida actual
        y_info = 200
        puntaje = self.fuente_hud.render(
            f"Tu Puntaje: {self.jugador.puntaje}", True, Colores.PUNTAJE
        )
        puntaje_rect = puntaje.get_rect(center=(self.ANCHO // 2, y_info))
        self.screen.blit(puntaje, puntaje_rect)

        tiempo_segundos = self.tiempo_transcurrido // 60
        # Calcular dificultad
        nivel_dificultad = self.computadora.velocidad / self.velocidad_inicial_enemigo
        tiempo_texto = self.fuente_pequena.render(
            f"Tiempo: {tiempo_segundos} segundos | Dificultad: {nivel_dificultad:.1f}x",
            True,
            Colores.TEXTO_SECUNDARIO,
        )
        tiempo_rect = tiempo_texto.get_rect(center=(self.ANCHO // 2, y_info + 40))
        self.screen.blit(tiempo_texto, tiempo_rect)

        # Mensaje indicando que el puntaje será guardado
        mensaje = self.fuente_pequena.render(
            "Tu puntaje ha sido guardado", True, (150, 200, 150)
        )
        mensaje_rect = mensaje.get_rect(center=(self.ANCHO // 2, y_info + 100))
        self.screen.blit(mensaje, mensaje_rect)

        # Mostrar mensaje según si puede salir o no
        y_instruccion = 500
        if self.game_over_timer > 0:
            segundos_restantes = ConfigJuego.frames_a_segundos(self.game_over_timer) + 1
            instruccion = self.fuente_pequena.render(
                f"Espera {segundos_restantes} segundos...",
                True,
                Colores.TEXTO_SECUNDARIO,
            )
        else:
            instruccion = self.fuente_pequena.render(
                "Presiona cualquier tecla para volver al menú", True, (100, 255, 100)
            )
        instruccion_rect = instruccion.get_rect(center=(self.ANCHO // 2, y_instruccion))
        self.screen.blit(instruccion, instruccion_rect)

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
                    # Pausar/reanudar música según el estado
                    if self.pausado:
                        self.sistema_sonido.pausar_musica()
                    else:
                        self.sistema_sonido.reanudar_musica()
                if evento.key == pygame.K_d:
                    self.mostrar_distancia = not self.mostrar_distancia
                if evento.key == pygame.K_m:
                    self.movimiento_por_celdas = not self.movimiento_por_celdas
                    modo = "Celdas" if self.movimiento_por_celdas else "Píxeles"
                    print(f"Modo de movimiento cambiado a: {modo}")
                if evento.key == pygame.K_u:
                    # Alternar música de fondo
                    self.sistema_sonido.alternar_musica()
                    estado = (
                        "activada"
                        if self.sistema_sonido.musica_activa
                        else "desactivada"
                    )
                    print(f"Música {estado}")

                # En game over, cualquier tecla (menos 'p') sale SOLO si pasaron los 5 segundos
                if (
                    self.game_over
                    and evento.key != pygame.K_p
                    and self.game_over_timer == 0
                ):
                    return "salir"

        return None  # No hay acción global

    def ejecutar(self):
        """Crea la ventana, inicializa fuentes y corre el loop hasta salir.

        Retorna:
            dict | None: Datos del puntaje {'nombre': str, 'puntaje': int, 'laberinto': str} si hubo game over, None si salió antes
        """
        if not pygame.get_init():
            pygame.init()

        self.screen = pygame.display.set_mode((self.ANCHO, self.ALTO))
        pygame.display.set_caption(ConfigJuego.TITULO + " - Modo Laberinto")

        # Fuentes para títulos y HUD desde GestorFuentes
        from interfaz.gestor_fuentes import GestorFuentes

        fuentes = GestorFuentes()
        self.fuente_titulo = fuentes.hud_titulo
        self.fuente_hud = fuentes.hud_normal
        self.fuente_pequena = fuentes.hud_pequeño

        ejecutando = True
        while ejecutando:
            self.reloj.tick(ConfigJuego.FPS)  # Usar FPS de config
            resultado = self.manejar_eventos()
            if resultado == "salir":
                ejecutando = False

            self._actualizar()
            self._renderizar()

        # Detener la música al salir
        self.sistema_sonido.detener_musica()

        # Retornar datos del puntaje si hubo game over
        if self.game_over and self.puntaje_final is not None:
            return {
                "nombre": self.nombre_jugador,
                "puntaje": self.puntaje_final,
                "laberinto": self.nombre_laberinto,
            }
        return None
