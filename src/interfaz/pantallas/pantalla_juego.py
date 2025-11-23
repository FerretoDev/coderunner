import math  # Para calcular distancias y ángulos
import os

import pygame  # Motor de eventos, dibujo y tiempo

from personajes.computadora import Computadora
from personajes.jugador import Jugador
from mundo.laberinto import Laberinto
from servicios.sistema_sonido import SistemaSonido

from config.config import Colores, ConfigJuego
from utilidades.coordenadas import ConversorCoordenadas
from jugabilidad.gestores.gestor_dificultad import GestorDificultad
from jugabilidad.gestores.gestor_movimiento import GestorMovimiento
from jugabilidad.gestores.gestor_obsequios import GestorObsequios


class PantallaJuego:
    """Pantalla principal del juego en modo laberinto, con HUD y dificultad progresiva."""

    def __init__(self, nombre_jugador="Jugador"):
        """Configura pantalla, colores, estados, laberinto, actores y timers."""
        # Configuración de pantalla y reloj usando config centralizada
        self.ANCHO = ConfigJuego.ANCHO_VENTANA
        self.ALTO = ConfigJuego.ALTO_VENTANA
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
            ruta_laberinto = "src/data/laberintos/laberinto3.json"

        self.laberinto = Laberinto(ruta_laberinto)  # Carga mapa, spawns y obsequios
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

        # Muros como Rects para colisiones rápidas
        self.muros = self._generar_muros()

        # Radios de personajes desde config
        radio_jugador = ConfigJuego.RADIO_JUGADOR
        radio_compu = ConfigJuego.RADIO_ENEMIGO

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

        # Radio de captura con holgura configurada
        if (
            distancia
            < self.jugador.radio + self.computadora.radio + ConfigJuego.MARGEN_CAPTURA
        ):
            # Reproducir sonido de captura
            self.sistema_sonido.reproducir_captura()

            self.jugador.perder_vida()
            if not self.jugador.esta_vivo():
                self.game_over = True
                self.game_over_timer = ConfigJuego.segundos_a_frames(
                    ConfigJuego.SEGUNDOS_ESPERA_GAME_OVER
                )
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
        """Dibuja cada celda como pared o piso con borde tenue para guiar al jugador."""
        for fila in range(len(self.mapa)):
            for col in range(len(self.mapa[0])):
                x = col * self.tam_celda + self.offset_x
                y = fila * self.tam_celda + self.offset_y

                if self.mapa[fila][col] == 1:
                    pygame.draw.rect(
                        self.screen,
                        Colores.PARED,
                        (x, y, self.tam_celda, self.tam_celda),
                    )
                else:
                    self.screen.blit(self.imagen_pasillo, (x, y))
                    pygame.draw.rect(
                        self.screen,
                        Colores.BORDE_CELDA,
                        (x, y, self.tam_celda, self.tam_celda),
                        1,
                    )

    def _dibujar_hud(self):
        """Panel superior con nombre, vidas, puntaje, dificultad, tiempo y controles."""
        # Panel base y línea inferior
        panel_rect = pygame.Rect(0, 0, self.ANCHO, 80)
        pygame.draw.rect(self.screen, Colores.HUD_FONDO, panel_rect)
        pygame.draw.line(self.screen, Colores.ACENTO, (0, 80), (self.ANCHO, 80), 2)

        # Nombre del jugador
        nombre_surf = self.fuente_pequena.render(
            f"Jugador: {self.nombre_jugador}", True, Colores.TEXTO
        )
        self.screen.blit(nombre_surf, (20, 15))

        # Vidas dibujadas como corazones simples
        x_vidas = 20
        y_vidas = 45
        for i in range(self.jugador.vidas):  # Usando property en vez de _vidas
            cx = x_vidas + (i * 35)
            pygame.draw.circle(self.screen, Colores.VIDAS, (cx + 5, y_vidas + 5), 5)
            pygame.draw.circle(self.screen, Colores.VIDAS, (cx + 15, y_vidas + 5), 5)
            puntos = [
                (cx, y_vidas + 6),
                (cx + 20, y_vidas + 6),
                (cx + 10, y_vidas + 18),
            ]
            pygame.draw.polygon(self.screen, Colores.VIDAS, puntos)

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
        pygame.draw.polygon(self.screen, Colores.PUNTAJE, puntos_estrella)

        puntaje_surf = self.fuente_hud.render(
            f"{self.jugador.puntaje}", True, Colores.PUNTAJE  # Usando property
        )
        self.screen.blit(puntaje_surf, (x_puntaje + 20, y_puntaje))

        # Dificultad relativa (velocidad / velocidad inicial)
        nivel_dificultad = self.computadora.velocidad / self.velocidad_inicial_enemigo
        dificultad_surf = self.fuente_pequena.render(
            f"Dificultad: {nivel_dificultad:.1f}x", True, Colores.ENEMIGO
        )
        self.screen.blit(dificultad_surf, (400, 15))

        # Tiempo en mm:ss
        tiempo_min = self.tiempo_transcurrido // 3600
        tiempo_seg = (self.tiempo_transcurrido % 3600) // 60
        tiempo_surf = self.fuente_pequena.render(
            f"Tiempo: {tiempo_min:02d}:{tiempo_seg:02d}", True, Colores.TEXTO
        )
        self.screen.blit(tiempo_surf, (400, 45))

        # Controles de ayuda al usuario
        controles_surf = self.fuente_pequena.render(
            "WASD/Flechas: Mover | P: Pausa | U: Música | ESC: Salir",
            True,
            Colores.TEXTO_SECUNDARIO,
        )
        controles_rect = controles_surf.get_rect(right=self.ANCHO - 20, centery=40)
        self.screen.blit(controles_surf, controles_rect)

    def _dibujar_pausa(self):
        """Overlay translúcido y texto de pausa."""
        overlay = pygame.Surface((self.ANCHO, self.ALTO))
        overlay.set_alpha(180)
        overlay.fill(Colores.OVERLAY_OSCURO)
        self.screen.blit(overlay, (0, 0))

        titulo = self.fuente_titulo.render("PAUSA", True, Colores.TEXTO)
        titulo_rect = titulo.get_rect(center=(self.ANCHO // 2, self.ALTO // 2 - 50))
        self.screen.blit(titulo, titulo_rect)

        instruccion = self.fuente_hud.render(
            "Presiona P para continuar", True, Colores.TEXTO_SECUNDARIO
        )
        instruccion_rect = instruccion.get_rect(
            center=(self.ANCHO // 2, self.ALTO // 2 + 30)
        )
        self.screen.blit(instruccion, instruccion_rect)

    def _dibujar_game_over(self):
        """Overlay de game over, guarda puntaje una vez y muestra métricas finales con ranking."""
        if not hasattr(self, "_puntaje_guardado"):
            # Detener la música al llegar a game over
            self.sistema_sonido.pausar_musica()
            self._guardar_en_salon_fama()
            self._puntaje_guardado = True

        overlay = pygame.Surface((self.ANCHO, self.ALTO))
        overlay.set_alpha(200)
        overlay.fill(Colores.OVERLAY_OSCURO)
        self.screen.blit(overlay, (0, 0))

        # Caja más grande para incluir el ranking
        caja_rect = pygame.Rect(self.ANCHO // 2 - 350, 30, 700, self.ALTO - 60)
        pygame.draw.rect(self.screen, (40, 40, 60), caja_rect, border_radius=15)
        pygame.draw.rect(self.screen, Colores.VIDAS, caja_rect, 3, border_radius=15)

        titulo = self.fuente_titulo.render("GAME OVER", True, Colores.VIDAS)
        titulo_rect = titulo.get_rect(center=(self.ANCHO // 2, 70))
        self.screen.blit(titulo, titulo_rect)

        # Información de la partida actual
        y_info = 120
        puntaje = self.fuente_hud.render(
            f"Tu Puntaje: {self.jugador.puntaje}", True, Colores.PUNTAJE
        )
        puntaje_rect = puntaje.get_rect(center=(self.ANCHO // 2, y_info))
        self.screen.blit(puntaje, puntaje_rect)

        tiempo_segundos = self.tiempo_transcurrido // 60
        tiempo_texto = self.fuente_pequena.render(
            f"Tiempo: {tiempo_segundos} segundos | Dificultad: {self.computadora.velocidad:.1f}x",
            True,
            Colores.TEXTO_SECUNDARIO,
        )
        tiempo_rect = tiempo_texto.get_rect(center=(self.ANCHO // 2, y_info + 40))
        self.screen.blit(tiempo_texto, tiempo_rect)

        # Línea separadora
        pygame.draw.line(
            self.screen,
            (100, 100, 120),
            (self.ANCHO // 2 - 300, y_info + 75),
            (self.ANCHO // 2 + 300, y_info + 75),
            2,
        )

        # Título del ranking
        ranking_titulo = self.fuente_hud.render(
            "Top 5 Mejores Puntajes", True, (255, 215, 0)
        )
        ranking_titulo_rect = ranking_titulo.get_rect(
            center=(self.ANCHO // 2, y_info + 100)
        )
        self.screen.blit(ranking_titulo, ranking_titulo_rect)

        # Obtener y mostrar el ranking
        from mundo.salon_fama import SalonFama

        salon = SalonFama()
        registros = salon.mostrar_mejores(limite=5)

        y_ranking = y_info + 145
        if registros:
            # Encabezados
            encabezado = self.fuente_pequena.render(
                "#    Jugador              Puntaje", True, (150, 150, 150)
            )
            self.screen.blit(encabezado, (self.ANCHO // 2 - 250, y_ranking))
            y_ranking += 30

            # Mostrar cada registro
            for i, reg in enumerate(registros, 1):
                # Color especial para el top 3
                if i == 1:
                    color = (255, 215, 0)  # Oro
                    emoji = "1."
                elif i == 2:
                    color = (192, 192, 192)  # Plata
                    emoji = "2."
                elif i == 3:
                    color = (205, 127, 50)  # Bronce
                    emoji = "3."
                else:
                    color = (200, 200, 220)
                    emoji = f"{i}."

                # Destacar el puntaje actual del jugador
                nombre_completo = reg["nombre_jugador"]
                nombre = nombre_completo[:15]  # Limitar longitud del nombre
                if (
                    nombre_completo == self.nombre_jugador
                    and reg["puntaje"] == self.jugador.puntaje
                ):
                    # Es el registro recién agregado
                    nombre = f"► {nombre}"  # Marcar con flecha
                    color = Colores.PUNTAJE  # Usar color de puntaje

                texto = f"{emoji} {i}  {nombre:<18} {reg['puntaje']:>6} pts"
                registro_surface = self.fuente_pequena.render(texto, True, color)
                self.screen.blit(registro_surface, (self.ANCHO // 2 - 250, y_ranking))
                y_ranking += 35
        else:
            sin_registros = self.fuente_pequena.render(
                "No hay registros todavía", True, (150, 150, 150)
            )
            sin_registros_rect = sin_registros.get_rect(
                center=(self.ANCHO // 2, y_ranking + 50)
            )
            self.screen.blit(sin_registros, sin_registros_rect)

        # Mostrar mensaje según si puede salir o no
        y_instruccion = self.ALTO - 60
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

    def _guardar_en_salon_fama(self):
        """Crea un registro y lo guarda en el salón de la fama."""
        from mundo.registro import Registro
        from mundo.salon_fama import SalonFama

        salon = SalonFama()
        registro = Registro(
            nombre_jugador=self.nombre_jugador,
            puntaje=self.jugador._puntaje,
            laberinto=self.laberinto.nombre,
        )
        salon.guardar_puntaje(registro)
        print(f"Puntaje guardado en el Salón de la Fama: {self.jugador.puntaje} puntos")

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
        """Crea la ventana, inicializa fuentes y corre el loop hasta salir."""
        if not pygame.get_init():
            pygame.init()

        self.screen = pygame.display.set_mode((self.ANCHO, self.ALTO))
        pygame.display.set_caption(ConfigJuego.TITULO + " - Modo Laberinto")

        # Fuentes para títulos y HUD
        self.fuente_titulo = pygame.font.Font(None, 48)
        self.fuente_hud = pygame.font.Font(None, 32)
        self.fuente_pequena = pygame.font.Font(None, 24)

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

        # No se cierra pygame aquí para retornar al menú sin destruir el contexto
        # pygame.quit()
