"""
Sistema de sprites animados para personajes del juego.

Maneja la carga y animación de spritesheets con metadata.
"""

import json
from pathlib import Path

import pygame


class SpriteAnimado:
    """
    Clase para manejar sprites animados desde spritesheets.

    Características:
    - Carga spritesheet con metadata JSON
    - Soporte para múltiples animaciones
    - Control de velocidad de animación
    - Flip horizontal automático
    """

    def __init__(self, spritesheet_path, frame_width=32, frame_height=48):
        """
        Inicializa el sprite animado.

        Args:
            spritesheet_path: Ruta al archivo PNG del spritesheet
            frame_width: Ancho de cada frame individual
            frame_height: Alto de cada frame individual
        """
        # Cargar spritesheet
        try:
            self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
        except pygame.error:
            # Si no hay display configurado, cargar sin convert_alpha
            self.spritesheet = pygame.image.load(spritesheet_path)

        # Dimensiones de frames
        self.frame_width = frame_width
        self.frame_height = frame_height

        # Animación actual
        self.animacion_actual = "idle"
        self.frame_actual = 0
        self.contador_frames = 0
        self.velocidad_animacion = 8  # Frames entre cambios

        # Dirección
        self.flip_horizontal = False

        # Extraer frames del spritesheet
        self._extraer_frames()

    def _extraer_frames(self):
        """Extrae todos los frames del spritesheet."""
        # Theseus spritesheet: 1024x96
        # Estructura: idle(2), run(6), jump(2), slide(2), death(4) = 16 frames
        # Frame size: 64x96 (32x48 base escalado x2)

        ancho_sheet = self.spritesheet.get_width()
        frames_totales = ancho_sheet // self.frame_width

        self.animaciones = {
            "idle": {"frames": [], "inicio": 0, "cantidad": 2},
            "run": {"frames": [], "inicio": 2, "cantidad": 6},
            "jump": {"frames": [], "inicio": 8, "cantidad": 2},
            "slide": {"frames": [], "inicio": 10, "cantidad": 2},
            "death": {"frames": [], "inicio": 12, "cantidad": 4},
        }

        # Extraer cada frame
        for anim_nombre, anim_data in self.animaciones.items():
            inicio = anim_data["inicio"]
            cantidad = anim_data["cantidad"]

            for i in range(cantidad):
                x = (inicio + i) * self.frame_width
                y = 0

                # Crear superficie para el frame
                frame = pygame.Surface(
                    (self.frame_width, self.frame_height), pygame.SRCALPHA
                )
                frame.blit(
                    self.spritesheet,
                    (0, 0),
                    (x, y, self.frame_width, self.frame_height),
                )

                anim_data["frames"].append(frame)

    def cambiar_animacion(self, nombre_animacion):
        """
        Cambia a una animación diferente.

        Args:
            nombre_animacion: Nombre de la animación (idle, run, jump, slide, death)
        """
        if (
            nombre_animacion != self.animacion_actual
            and nombre_animacion in self.animaciones
        ):
            self.animacion_actual = nombre_animacion
            self.frame_actual = 0
            self.contador_frames = 0

    def actualizar(self):
        """Actualiza el frame de animación según el contador."""
        self.contador_frames += 1

        if self.contador_frames >= self.velocidad_animacion:
            self.contador_frames = 0
            anim_data = self.animaciones[self.animacion_actual]
            self.frame_actual = (self.frame_actual + 1) % len(anim_data["frames"])

    def obtener_frame_actual(self):
        """
        Obtiene el frame actual de la animación.

        Returns:
            pygame.Surface: Frame actual con flip aplicado si corresponde
        """
        anim_data = self.animaciones[self.animacion_actual]
        frame = anim_data["frames"][self.frame_actual]

        if self.flip_horizontal:
            return pygame.transform.flip(frame, True, False)
        return frame

    def set_direccion(self, moviendo_derecha):
        """
        Establece la dirección del sprite.

        Args:
            moviendo_derecha: True si se mueve a la derecha, False a la izquierda
        """
        self.flip_horizontal = not moviendo_derecha


class SpriteTheseusRunner:
    """
    Sprite específico para Theseus (jugador).

    Usa el spritesheet theseus_spritesheet.png (1024x96, frames 64x96)
    """

    def __init__(self, escala=1):
        """
        Inicializa el sprite de Theseus.

        Args:
            escala: Factor de escala (1 = 64x96, 0.5 = 32x48)
        """
        ruta = Path("src/assets/imagenes/theseus_spritesheet.png")
        self.sprite = SpriteAnimado(str(ruta), frame_width=64, frame_height=96)

        # Aplicar escala si es necesario
        self.escala = escala
        if escala != 1:
            self._reescalar_frames()

    def _reescalar_frames(self):
        """Reescala todos los frames del sprite."""
        nuevo_ancho = int(self.sprite.frame_width * self.escala)
        nuevo_alto = int(self.sprite.frame_height * self.escala)

        for anim_data in self.sprite.animaciones.values():
            frames_reescalados = []
            for frame in anim_data["frames"]:
                frame_reescalado = pygame.transform.scale(
                    frame, (nuevo_ancho, nuevo_alto)
                )
                frames_reescalados.append(frame_reescalado)
            anim_data["frames"] = frames_reescalados

        self.sprite.frame_width = nuevo_ancho
        self.sprite.frame_height = nuevo_alto

    def actualizar(
        self, moviendo=False, saltando=False, muriendo=False, direccion_derecha=True
    ):
        """
        Actualiza la animación de Theseus según su estado.

        Args:
            moviendo: True si está corriendo
            saltando: True si está saltando
            muriendo: True si está muriendo
            direccion_derecha: True si mira a la derecha
        """
        # Determinar animación
        if muriendo:
            self.sprite.cambiar_animacion("death")
        elif saltando:
            self.sprite.cambiar_animacion("jump")
        elif moviendo:
            self.sprite.cambiar_animacion("run")
        else:
            self.sprite.cambiar_animacion("idle")

        # Actualizar dirección
        self.sprite.set_direccion(direccion_derecha)

        # Actualizar frame
        self.sprite.actualizar()

    def dibujar(self, surface, x, y):
        """
        Dibuja el sprite en la superficie.

        Args:
            surface: pygame.Surface donde dibujar
            x: Posición X (centrada)
            y: Posición Y (centrada)
        """
        frame = self.sprite.obtener_frame_actual()
        rect = frame.get_rect(center=(x, y))
        surface.blit(frame, rect)


class SpriteMinotaurRunner:
    """
    Sprite específico para Minotauro (enemigo).

    Usa el spritesheet minotaur_spritesheet.png (1824x96, frames 96x96)
    """

    def __init__(self, escala=1):
        """
        Inicializa el sprite del Minotauro.

        Args:
            escala: Factor de escala (1 = 96x96, 0.5 = 48x48)
        """
        ruta = Path("src/assets/imagenes/minotaur_spritesheet.png")
        self.sprite = SpriteAnimado(str(ruta), frame_width=96, frame_height=96)

        # Estructura del Minotauro: idle(3), walk(6), attack(5), hurt(2), death(3)
        self.sprite.animaciones = {
            "idle": {"frames": [], "inicio": 0, "cantidad": 3},
            "walk": {"frames": [], "inicio": 3, "cantidad": 6},
            "attack": {"frames": [], "inicio": 9, "cantidad": 5},
            "hurt": {"frames": [], "inicio": 14, "cantidad": 2},
            "death": {"frames": [], "inicio": 16, "cantidad": 3},
        }

        # Re-extraer frames con la estructura correcta
        self.sprite._extraer_frames()

        # Aplicar escala
        self.escala = escala
        if escala != 1:
            self._reescalar_frames()

    def _reescalar_frames(self):
        """Reescala todos los frames del sprite."""
        nuevo_ancho = int(self.sprite.frame_width * self.escala)
        nuevo_alto = int(self.sprite.frame_height * self.escala)

        for anim_data in self.sprite.animaciones.values():
            frames_reescalados = []
            for frame in anim_data["frames"]:
                frame_reescalado = pygame.transform.scale(
                    frame, (nuevo_ancho, nuevo_alto)
                )
                frames_reescalados.append(frame_reescalado)
            anim_data["frames"] = frames_reescalados

        self.sprite.frame_width = nuevo_ancho
        self.sprite.frame_height = nuevo_alto

    def actualizar(
        self,
        moviendo=False,
        atacando=False,
        herido=False,
        muriendo=False,
        direccion_derecha=True,
    ):
        """
        Actualiza la animación del Minotauro según su estado.

        Args:
            moviendo: True si está caminando
            atacando: True si está atacando
            herido: True si fue golpeado
            muriendo: True si está muriendo
            direccion_derecha: True si mira a la derecha
        """
        # Determinar animación
        if muriendo:
            self.sprite.cambiar_animacion("death")
        elif herido:
            self.sprite.cambiar_animacion("hurt")
        elif atacando:
            self.sprite.cambiar_animacion("attack")
        elif moviendo:
            self.sprite.cambiar_animacion("walk")
        else:
            self.sprite.cambiar_animacion("idle")

        # Actualizar dirección
        self.sprite.set_direccion(direccion_derecha)

        # Actualizar frame
        self.sprite.actualizar()

    def dibujar(self, surface, x, y):
        """
        Dibuja el sprite en la superficie.

        Args:
            surface: pygame.Surface donde dibujar
            x: Posición X (centrada)
            y: Posición Y (centrada)
        """
        frame = self.sprite.obtener_frame_actual()
        rect = frame.get_rect(center=(x, y))
        surface.blit(frame, rect)
