"""
Generador de assets de audio (música chiptune y efectos de sonido).
Genera archivos WAV de 8-bit usando síntesis básica.
"""

import wave
import struct
import math
import json
from pathlib import Path


def generate_square_wave(frequency, duration, sample_rate=22050, volume=0.3):
    """Genera onda cuadrada (sonido 8-bit)."""
    num_samples = int(sample_rate * duration)
    samples = []

    for i in range(num_samples):
        t = i / sample_rate
        value = volume if math.sin(2 * math.pi * frequency * t) > 0 else -volume
        samples.append(int(value * 32767))

    return samples


def generate_noise(duration, sample_rate=22050, volume=0.2):
    """Genera ruido blanco."""
    import random

    random.seed(42)
    num_samples = int(sample_rate * duration)
    return [int(random.uniform(-volume, volume) * 32767) for _ in range(num_samples)]


def save_wav(filename, samples, sample_rate=22050):
    """Guarda samples como archivo WAV."""
    with wave.open(str(filename), "w") as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)

        for sample in samples:
            wav_file.writeframes(struct.pack("h", sample))


def generate_jump_sound(output_file):
    """Genera sonido de salto (frecuencia ascendente)."""
    samples = []
    for freq in range(200, 400, 20):
        samples.extend(generate_square_wave(freq, 0.02))
    save_wav(output_file, samples)


def generate_coin_sound(output_file):
    """Genera sonido de moneda (tono alegre)."""
    samples = []
    for freq in [523, 659, 784]:  # Do, Mi, Sol
        samples.extend(generate_square_wave(freq, 0.05))
    save_wav(output_file, samples)


def generate_hit_sound(output_file):
    """Genera sonido de golpe."""
    samples = generate_noise(0.1)
    save_wav(output_file, samples)


def generate_death_sound(output_file):
    """Genera sonido de muerte (frecuencia descendente)."""
    samples = []
    for freq in range(300, 100, -10):
        samples.extend(generate_square_wave(freq, 0.02))
    save_wav(output_file, samples)


def generate_victory_sound(output_file):
    """Genera sonido de victoria (fanfarria)."""
    samples = []
    notes = [523, 659, 784, 1047]  # Do, Mi, Sol, Do alto
    for freq in notes:
        samples.extend(generate_square_wave(freq, 0.15))
    save_wav(output_file, samples)


def generate_bgm_loop(output_file):
    """Genera loop de música de fondo simple."""
    samples = []
    # Secuencia de notas en bucle
    melody = [
        (330, 0.3),
        (330, 0.3),
        (349, 0.3),
        (392, 0.6),
        (349, 0.3),
        (330, 0.3),
        (294, 0.6),
        (262, 0.6),
    ]

    for freq, duration in melody:
        samples.extend(generate_square_wave(freq, duration))

    save_wav(output_file, samples)


def generate_audio_assets(scale=1, palette_name="default", output_dir="assets"):
    """Genera todos los assets de audio."""
    output_path = Path(output_dir)
    (output_path / "audio" / "sfx").mkdir(parents=True, exist_ok=True)
    (output_path / "audio" / "music").mkdir(parents=True, exist_ok=True)
    (output_path / "meta").mkdir(exist_ok=True)

    sfx_files = {
        "jump": "audio/sfx/jump.wav",
        "coin": "audio/sfx/coin.wav",
        "hit": "audio/sfx/hit.wav",
        "death": "audio/sfx/death.wav",
        "victory": "audio/sfx/victory.wav",
    }

    generate_jump_sound(output_path / sfx_files["jump"])
    generate_coin_sound(output_path / sfx_files["coin"])
    generate_hit_sound(output_path / sfx_files["hit"])
    generate_death_sound(output_path / sfx_files["death"])
    generate_victory_sound(output_path / sfx_files["victory"])

    music_files = {"bgm_loop": "audio/music/bgm_loop.wav"}

    generate_bgm_loop(output_path / music_files["bgm_loop"])

    meta = {"sfx": sfx_files, "music": music_files}

    with open(output_path / "meta" / "audio.json", "w") as f:
        json.dump(meta, f, indent=2)

    print(f"✓ Audio generado: {len(sfx_files)} SFX + {len(music_files)} música")
    print(f"  - SFX: {', '.join(sfx_files.keys())}")
    print(f"  - Música: {', '.join(music_files.keys())}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, default=1)
    parser.add_argument("--palette", default="default")
    parser.add_argument("--out", default="assets")
    args = parser.parse_args()

    generate_audio_assets(args.scale, args.palette, args.out)
