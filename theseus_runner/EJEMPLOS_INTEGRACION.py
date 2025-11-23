"""
Ejemplos de código para integrar los assets generados en tu juego.
"""

import pygame
import json
from pathlib import Path


# ==================================================
# EJEMPLO 1: Cargar y usar sprites animados
# ==================================================


class AnimatedSprite(pygame.sprite.Sprite):
    """Sprite animado con soporte para metadata JSON."""

    def __init__(self, spritesheet_path, meta_path, pos=(0, 0)):
        super().__init__()

        # Cargar spritesheet
        self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()

        # Cargar metadata
        with open(meta_path) as f:
            self.meta = json.load(f)

        # Estado
        self.current_animation = None
        self.current_frame = 0
        self.frame_time = 0
        self.image = None
        self.rect = None
        self.pos = pos

    def set_animation(self, name):
        """Cambia a una nueva animación."""
        if name == self.current_animation:
            return

        if name in self.meta["animations"]:
            self.current_animation = name
            self.current_frame = 0
            self.frame_time = 0
            self._update_image()

    def _update_image(self):
        """Actualiza la imagen del sprite desde el frame actual."""
        anim = self.meta["animations"][self.current_animation]
        frame_data = anim["frames"][self.current_frame]

        # Extraer frame del spritesheet
        rect = pygame.Rect(
            frame_data["x"], frame_data["y"], frame_data["w"], frame_data["h"]
        )
        self.image = self.spritesheet.subsurface(rect)

        if not self.rect:
            self.rect = self.image.get_rect()
            self.rect.topleft = self.pos

    def update(self, dt):
        """Actualiza la animación (dt en milisegundos)."""
        if not self.current_animation:
            return

        anim = self.meta["animations"][self.current_animation]
        frame_data = anim["frames"][self.current_frame]

        self.frame_time += dt

        # Cambiar frame si es necesario
        if self.frame_time >= frame_data["duration"]:
            self.frame_time = 0
            self.current_frame += 1

            # Loop o detener
            if self.current_frame >= len(anim["frames"]):
                if anim["loop"]:
                    self.current_frame = 0
                else:
                    self.current_frame = len(anim["frames"]) - 1

            self._update_image()


# Uso:
# theseus = AnimatedSprite('assets/sprites/theseus_spritesheet.png',
#                          'assets/meta/theseus.json',
#                          pos=(100, 200))
# theseus.set_animation('run')


# ==================================================
# EJEMPLO 2: Sistema de parallax con fondos
# ==================================================


class ParallaxBackground:
    """Fondo con efecto parallax de múltiples capas."""

    def __init__(self, screen_width):
        self.screen_width = screen_width

        # Cargar metadata
        with open("assets/meta/backgrounds.json") as f:
            meta = json.load(f)

        # Cargar capas
        self.layers = []
        for layer_data in meta["layers"]:
            img = pygame.image.load(
                f'assets/backgrounds/{layer_data["file"]}'
            ).convert_alpha()
            speed = layer_data["speed"]
            self.layers.append({"image": img, "speed": speed, "x": 0})

    def update(self, camera_dx):
        """Actualiza la posición de las capas según el movimiento de cámara."""
        for layer in self.layers:
            layer["x"] -= camera_dx * layer["speed"]

            # Wrap around
            if layer["x"] <= -layer["image"].get_width():
                layer["x"] = 0
            elif layer["x"] >= layer["image"].get_width():
                layer["x"] = 0

    def draw(self, screen):
        """Dibuja todas las capas."""
        for layer in self.layers:
            width = layer["image"].get_width()
            x = layer["x"]

            # Dibujar dos veces para seamless loop
            screen.blit(layer["image"], (x, 0))
            if x + width < self.screen_width:
                screen.blit(layer["image"], (x + width, 0))
            if x > 0:
                screen.blit(layer["image"], (x - width, 0))


# ==================================================
# EJEMPLO 3: Tilemap desde tileset
# ==================================================


class TileMap:
    """Mapa de tiles basado en el tileset generado."""

    def __init__(self, tile_size=16):
        self.tile_size = tile_size

        # Cargar tileset
        tileset_file = f"assets/tiles/tileset_{tile_size}x{tile_size}.png"
        self.tileset = pygame.image.load(tileset_file).convert_alpha()

        # Cargar metadata
        with open("assets/meta/tilesets.json") as f:
            meta = json.load(f)

        self.tiles_meta = meta[f"{tile_size}x{tile_size}"]["tiles"]

        # Crear diccionario de tiles por ID
        self.tiles = {}
        for tile_data in self.tiles_meta:
            tile_id = tile_data["id"]
            rect = pygame.Rect(
                tile_data["x"], tile_data["y"], tile_data["w"], tile_data["h"]
            )
            self.tiles[tile_id] = self.tileset.subsurface(rect)

    def draw_map(self, screen, tile_grid):
        """Dibuja un grid de tiles.

        tile_grid: lista 2D de IDs de tiles
        Ejemplo:
        [
            ['wall', 'wall', 'wall'],
            ['wall', 'floor_0', 'wall'],
            ['wall', 'wall', 'wall']
        ]
        """
        for row_idx, row in enumerate(tile_grid):
            for col_idx, tile_id in enumerate(row):
                if tile_id in self.tiles:
                    x = col_idx * self.tile_size
                    y = row_idx * self.tile_size
                    screen.blit(self.tiles[tile_id], (x, y))


# ==================================================
# EJEMPLO 4: Sistema de partículas
# ==================================================


class ParticleSystem:
    """Sistema simple de partículas usando los sprites generados."""

    def __init__(self):
        # Cargar spritesheet de partículas
        self.spritesheet = pygame.image.load(
            "assets/particles/particles.png"
        ).convert_alpha()

        # Cargar metadata
        with open("assets/meta/particles.json") as f:
            meta = json.load(f)

        # Extraer frames de cada tipo
        self.particle_types = {}
        for effect_name, effect_data in meta["particles"].items():
            frames = []
            for frame_data in effect_data["frames"]:
                rect = pygame.Rect(
                    frame_data["x"], frame_data["y"], frame_data["w"], frame_data["h"]
                )
                frames.append(self.spritesheet.subsurface(rect))
            self.particle_types[effect_name] = frames

        self.particles = []

    def emit(self, effect_type, pos, velocity, lifetime=1000):
        """Emite una nueva partícula."""
        if effect_type in self.particle_types:
            import random

            frames = self.particle_types[effect_type]
            frame = random.choice(frames)

            self.particles.append(
                {
                    "image": frame,
                    "pos": list(pos),
                    "velocity": list(velocity),
                    "lifetime": lifetime,
                    "age": 0,
                }
            )

    def update(self, dt):
        """Actualiza todas las partículas."""
        for particle in self.particles[:]:
            particle["age"] += dt

            # Mover
            particle["pos"][0] += particle["velocity"][0] * (dt / 1000)
            particle["pos"][1] += particle["velocity"][1] * (dt / 1000)

            # Remover si expiró
            if particle["age"] >= particle["lifetime"]:
                self.particles.remove(particle)

    def draw(self, screen):
        """Dibuja todas las partículas."""
        for particle in self.particles:
            screen.blit(particle["image"], particle["pos"])


# ==================================================
# EJEMPLO 5: UI con botones
# ==================================================


class Button:
    """Botón de UI usando los sprites generados."""

    # Cargar spritesheet de botones (hacer una vez)
    _button_sheet = None
    _button_meta = None

    @classmethod
    def _load_assets(cls):
        if cls._button_sheet is None:
            cls._button_sheet = pygame.image.load(
                "assets/ui/buttons.png"
            ).convert_alpha()
            with open("assets/meta/ui.json") as f:
                cls._button_meta = json.load(f)["buttons"]

    def __init__(self, x, y, text, callback):
        Button._load_assets()

        self.rect = pygame.Rect(
            x, y, Button._button_meta["width"], Button._button_meta["height"]
        )
        self.text = text
        self.callback = callback
        self.state = "normal"

        # Extraer estados
        self.states = {}
        width = Button._button_meta["width"]
        for i, state_name in enumerate(Button._button_meta["states"]):
            rect = pygame.Rect(i * width, 0, width, Button._button_meta["height"])
            self.states[state_name] = Button._button_sheet.subsurface(rect)

    def handle_event(self, event):
        """Maneja eventos de mouse."""
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.state = "hover"
            else:
                self.state = "normal"

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.state = "pressed"

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos) and self.state == "pressed":
                self.callback()
                self.state = "hover"

    def draw(self, screen, font=None):
        """Dibuja el botón."""
        # Dibujar sprite del botón
        screen.blit(self.states[self.state], self.rect)

        # Dibujar texto (si hay fuente)
        if font:
            text_surf = font.render(self.text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)


# ==================================================
# EJEMPLO 6: Gestión de audio
# ==================================================


class AudioManager:
    """Gestor centralizado de audio."""

    def __init__(self):
        pygame.mixer.init()

        # Cargar metadata
        with open("assets/meta/audio.json") as f:
            self.meta = json.load(f)

        # Cargar efectos de sonido
        self.sfx = {}
        for name, path in self.meta["sfx"].items():
            self.sfx[name] = pygame.mixer.Sound(f"assets/{path}")

        # Música
        self.current_music = None

    def play_sfx(self, name, volume=1.0):
        """Reproduce un efecto de sonido."""
        if name in self.sfx:
            self.sfx[name].set_volume(volume)
            self.sfx[name].play()

    def play_music(self, name, volume=0.5, loops=-1):
        """Reproduce música de fondo."""
        if name in self.meta["music"]:
            if self.current_music != name:
                pygame.mixer.music.load(f'assets/{self.meta["music"][name]}')
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(loops)
                self.current_music = name

    def stop_music(self):
        """Detiene la música."""
        pygame.mixer.music.stop()
        self.current_music = None


# ==================================================
# EJEMPLO COMPLETO: Mini juego
# ==================================================


def example_game():
    """Ejemplo completo de integración."""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # Crear componentes
    player = AnimatedSprite(
        "assets/sprites/theseus_spritesheet.png",
        "assets/meta/theseus.json",
        pos=(100, 400),
    )
    player.set_animation("idle")

    background = ParallaxBackground(800)
    particles = ParticleSystem()
    audio = AudioManager()

    # Reproducir música
    audio.play_music("bgm_loop", volume=0.3)

    # Loop del juego
    running = True
    camera_speed = 2

    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.set_animation("jump")
                    audio.play_sfx("jump", volume=0.5)

                    # Emitir partículas de polvo
                    particles.emit(
                        "dust", player.rect.midbottom, velocity=(-50, -30), lifetime=500
                    )

        # Actualizar
        background.update(camera_speed)
        player.update(dt)
        particles.update(dt)

        # Dibujar
        screen.fill((0, 0, 0))
        background.draw(screen)
        screen.blit(player.image, player.rect)
        particles.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    print("Estos son ejemplos de código.")
    print("Descomenta 'example_game()' al final para ejecutar el mini-juego.")
    # example_game()
