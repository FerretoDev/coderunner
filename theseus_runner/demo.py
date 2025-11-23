"""
Demo de Theseus Runner mostrando todos los assets generados.
Ejecuta primero: python generate_all.py
"""

import pygame
import json
import sys
from pathlib import Path


class AnimatedSprite(pygame.sprite.Sprite):
    """Sprite animado que carga desde spritesheet + metadata JSON."""

    def __init__(self, spritesheet_path, meta_path):
        super().__init__()
        self.spritesheet = pygame.image.load(spritesheet_path)

        with open(meta_path) as f:
            self.meta = json.load(f)

        self.current_animation = None
        self.current_frame = 0
        self.frame_time = 0
        self.image = None
        self.rect = None

    def set_animation(self, name):
        """Cambia la animación actual."""
        if name in self.meta["animations"]:
            self.current_animation = name
            self.current_frame = 0
            self.frame_time = 0
            self._update_image()

    def _update_image(self):
        """Actualiza la imagen del sprite desde el frame actual."""
        if not self.current_animation:
            return

        anim = self.meta["animations"][self.current_animation]
        frame_data = anim["frames"][self.current_frame]

        rect = pygame.Rect(
            frame_data["x"], frame_data["y"], frame_data["w"], frame_data["h"]
        )
        self.image = self.spritesheet.subsurface(rect)

        if not self.rect:
            self.rect = self.image.get_rect()

    def update(self, dt):
        """Actualiza la animación."""
        if not self.current_animation:
            return

        anim = self.meta["animations"][self.current_animation]
        frame_data = anim["frames"][self.current_frame]

        self.frame_time += dt

        if self.frame_time >= frame_data["duration"]:
            self.frame_time = 0
            self.current_frame += 1

            if self.current_frame >= len(anim["frames"]):
                if anim["loop"]:
                    self.current_frame = 0
                else:
                    self.current_frame = len(anim["frames"]) - 1

            self._update_image()


def main():
    """Ejecuta la demo."""
    pygame.init()

    # Configuración
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Theseus Runner - Demo de Assets")
    clock = pygame.time.Clock()

    # Verificar assets
    assets_dir = Path("assets")
    if not assets_dir.exists():
        print("ERROR: Directorio 'assets/' no encontrado.")
        print("Ejecuta primero: python generate_all.py")
        return

    # Cargar backgrounds
    try:
        bg_layers = [
            pygame.image.load("assets/backgrounds/bg_layer1.png"),
            pygame.image.load("assets/backgrounds/bg_layer2.png"),
            pygame.image.load("assets/backgrounds/bg_layer3.png"),
        ]
        bg_scroll = [0, 0, 0]
        bg_speeds = [0.2, 0.5, 0.8]
    except FileNotFoundError:
        print("Fondos no encontrados. Generando con fondo negro.")
        bg_layers = None

    # Cargar Theseus
    try:
        theseus = AnimatedSprite(
            "assets/sprites/theseus_spritesheet.png", "assets/meta/theseus.json"
        )
        theseus.set_animation("idle")
        theseus.rect.center = (200, SCREEN_HEIGHT // 2)
    except FileNotFoundError:
        print("ERROR: Theseus spritesheet no encontrado")
        return

    # Cargar Minotauro
    try:
        minotaur = AnimatedSprite(
            "assets/sprites/minotaur_spritesheet.png", "assets/meta/minotaur.json"
        )
        minotaur.set_animation("idle")
        minotaur.rect.center = (600, SCREEN_HEIGHT // 2)
    except FileNotFoundError:
        print("Minotauro no encontrado (opcional)")
        minotaur = None

    # Cargar UI
    try:
        font_img = pygame.image.load("assets/fonts/font_16px.png")
        with open("assets/meta/font_16px.json") as f:
            font_meta = json.load(f)
    except FileNotFoundError:
        font_img = None
        font_meta = None

    # Cargar audio
    try:
        pygame.mixer.music.load("assets/audio/music/bgm_loop.wav")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        sfx_jump = pygame.mixer.Sound("assets/audio/sfx/jump.wav")
        sfx_coin = pygame.mixer.Sound("assets/audio/sfx/coin.wav")
    except (FileNotFoundError, pygame.error):
        print("Audio no disponible")
        sfx_jump = None
        sfx_coin = None

    # Estado
    current_theseus_anim = 0
    theseus_anims = ["idle", "run", "jump", "slide", "death"]

    # Loop principal
    running = True
    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # Espacio: cambiar animación de Theseus
                if event.key == pygame.K_SPACE:
                    current_theseus_anim = (current_theseus_anim + 1) % len(
                        theseus_anims
                    )
                    theseus.set_animation(theseus_anims[current_theseus_anim])
                    if sfx_jump:
                        sfx_jump.play()

                # C: sonido de moneda
                elif event.key == pygame.K_c and sfx_coin:
                    sfx_coin.play()

                # M: cambiar animación del Minotauro
                elif event.key == pygame.K_m and minotaur:
                    minotaur_anims = ["idle", "walk", "charge", "roar"]
                    current = minotaur.current_animation
                    idx = (
                        minotaur_anims.index(current)
                        if current in minotaur_anims
                        else 0
                    )
                    next_idx = (idx + 1) % len(minotaur_anims)
                    minotaur.set_animation(minotaur_anims[next_idx])

        # Actualizar parallax
        if bg_layers:
            for i in range(len(bg_scroll)):
                bg_scroll[i] = (bg_scroll[i] + bg_speeds[i]) % bg_layers[i].get_width()

        # Actualizar sprites
        theseus.update(dt)
        if minotaur:
            minotaur.update(dt)

        # Renderizar
        screen.fill((20, 12, 28))  # Color de fondo oscuro

        # Dibujar parallax
        if bg_layers:
            for i, layer in enumerate(bg_layers):
                x_offset = -bg_scroll[i]
                screen.blit(layer, (x_offset, 0))
                if x_offset + layer.get_width() < SCREEN_WIDTH:
                    screen.blit(layer, (x_offset + layer.get_width(), 0))

        # Dibujar sprites
        screen.blit(theseus.image, theseus.rect)
        if minotaur:
            screen.blit(minotaur.image, minotaur.rect)

        # UI de texto (instrucciones)
        if font_img and font_meta:
            # Usar fuente del sistema temporalmente para instrucciones
            pass

        # Fuente del sistema para instrucciones
        font = pygame.font.Font(None, 24)
        instructions = [
            "ESPACIO: Cambiar animacion de Theseus",
            "M: Cambiar animacion del Minotauro",
            "C: Sonido de moneda",
            f"Animacion actual: {theseus.current_animation}",
        ]

        y = 10
        for text in instructions:
            surf = font.render(text, True, (255, 255, 255))
            screen.blit(surf, (10, y))
            y += 30

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
