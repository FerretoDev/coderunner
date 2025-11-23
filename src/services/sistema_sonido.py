import os
import pygame


class SistemaSonido:
    """Sistema de sonido singleton para el juego con música y efectos"""

    _instancia = None
    _inicializado = False

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(SistemaSonido, cls).__new__(cls)
        return cls._instancia

    def __init__(self):
        # Solo inicializar una vez (patrón singleton)
        if SistemaSonido._inicializado:
            return

        SistemaSonido._inicializado = True

        # Inicializar el mixer de pygame
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.mixer_disponible = True
        except pygame.error as e:
            print(f"No se pudo inicializar el sistema de audio: {e}")
            self.mixer_disponible = False
            return

        # Estado del sistema de sonido
        self.sonidos_activos = True
        self.musica_activa = True
        self.volumen_musica = 0.4
        self.volumen_efectos = 0.6

        # Efectos de sonido (se cargarán bajo demanda)
        self.sonido_movimiento = None
        self.sonido_captura = None
        self.sonido_obsequio = None

    def reproducir_musica_fondo(self):
        """Reproduce la música de fondo del juego en loop"""
        if not self.mixer_disponible or not self.musica_activa:
            return

        try:
            # Buscar el archivo de música
            ruta_musica = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "..",
                "data",
                "MusicaPerrona.mp3",
            )

            if not os.path.exists(ruta_musica):
                print(
                    f"Advertencia: No se encontró el archivo de música en {ruta_musica}"
                )
                return

            pygame.mixer.music.load(ruta_musica)
            pygame.mixer.music.set_volume(self.volumen_musica)
            pygame.mixer.music.play(-1)  # -1 = loop infinito
        except pygame.error as e:
            print(f"Error al cargar la música: {e}")

    def pausar_musica(self):
        """Pausa la música de fondo"""
        if not self.mixer_disponible:
            return
        pygame.mixer.music.pause()

    def reanudar_musica(self):
        """Reanuda la música de fondo"""
        if not self.mixer_disponible:
            return
        pygame.mixer.music.unpause()

    def detener_musica(self):
        """Detiene completamente la música de fondo"""
        if not self.mixer_disponible:
            return
        pygame.mixer.music.stop()

    def ajustar_volumen_musica(self, volumen):
        """Ajusta el volumen de la música (0.0 a 1.0)"""
        if not self.mixer_disponible:
            return
        self.volumen_musica = max(0.0, min(1.0, volumen))
        pygame.mixer.music.set_volume(self.volumen_musica)

    def reproducir_movimiento(self):
        """Reproduce efecto de sonido de movimiento"""
        if self.sonidos_activos and self.mixer_disponible:
            # Placeholder - se puede agregar un sonido real aquí
            pass

    def reproducir_captura(self):
        """Reproduce efecto de sonido cuando el jugador es capturado"""
        if self.sonidos_activos and self.mixer_disponible:
            # Placeholder - se puede agregar un sonido real aquí
            pass

    def reproducir_obsequio(self):
        """Reproduce efecto de sonido cuando se recolecta un obsequio"""
        if self.sonidos_activos and self.mixer_disponible:
            # Placeholder - se puede agregar un sonido real aquí
            pass

    def alternar_musica(self):
        """Activa/desactiva la música de fondo"""
        self.musica_activa = not self.musica_activa
        if self.musica_activa:
            self.reanudar_musica()
        else:
            self.pausar_musica()

    def alternar_sonidos(self):
        """Activa/desactiva los efectos de sonido"""
        self.sonidos_activos = not self.sonidos_activos

    def desactivar_sonidos(self):
        """Desactiva todos los sonidos del sistema"""
        self.sonidos_activos = False
        self.musica_activa = False
        self.pausar_musica()
