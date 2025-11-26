#!/usr/bin/env python3
"""
Script de prueba para la estética mitológica griega del laberinto.

Tema: Mito de Teseo y el Minotauro
- Muros: Piedra antigua / mármol griego
- Pasillos: Mosaico greco-romano terracota
- Obsequios: Hilo de Ariadna (ovillo dorado)
- Paleta: Bronce, oro, terracota, mármol
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import pygame

from mundo.laberinto import Laberinto


def main():
    pygame.init()

    ancho = 900
    alto = 700
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Test: Estética Mitológica Griega - Laberinto de Teseo")
    reloj = pygame.time.Clock()

    # Crear laberinto de prueba (mapa pequeño para visualización)
    mapa_mitologico = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    tam_celda = 60
    offset_x = 80
    offset_y = 120

    # Posiciones de ovillos de hilo (Hilo de Ariadna)
    posiciones_hilo = [(2, 2), (7, 2), (4, 4), (2, 7), (7, 7)]

    fuente_titulo = pygame.font.Font(None, 48)
    fuente_info = pygame.font.Font(None, 24)
    fuente_subtitulo = pygame.font.Font(None, 28)

    ejecutando = True
    frame_count = 0

    print("\n" + "=" * 70)
    print("🏛️  TEST: ESTÉTICA MITOLÓGICA GRIEGA - LABERINTO DE TESEO")
    print("=" * 70)
    print("Elementos visuales:")
    print("  🏺 Muros: Piedra antigua / mármol griego con vetas")
    print("  🎨 Pasillos: Mosaico greco-romano terracota")
    print("  🧵 Obsequios: Hilo de Ariadna (ovillo dorado resplandeciente)")
    print("  🎭 Paleta: Bronce, oro, terracota, mármol")
    print("\nPresiona ESC para salir")
    print("=" * 70 + "\n")

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False

        # Fondo color pergamino antiguo
        pantalla.fill((240, 230, 210))

        # === TÍTULO ===
        titulo = fuente_titulo.render(
            "ΛΑΒΥΡΙΝΘΟΣ", True, (139, 69, 19)
        )  # LABERINTO en griego
        titulo_rect = titulo.get_rect(center=(ancho // 2, 40))
        pantalla.blit(titulo, titulo_rect)

        subtitulo = fuente_subtitulo.render(
            "El Laberinto de Teseo", True, (101, 67, 33)
        )
        subtitulo_rect = subtitulo.get_rect(center=(ancho // 2, 75))
        pantalla.blit(subtitulo, subtitulo_rect)

        # === DIBUJAR LABERINTO ===
        import math

        for fila in range(len(mapa_mitologico)):
            for col in range(len(mapa_mitologico[0])):
                x = col * tam_celda + offset_x
                y = fila * tam_celda + offset_y

                if mapa_mitologico[fila][col] == 1:
                    # === MUROS DE PIEDRA ANTIGUA ===
                    color_base = (210, 195, 170)
                    pygame.draw.rect(pantalla, color_base, (x, y, tam_celda, tam_celda))

                    # Textura de bloques
                    block_size = tam_celda // 3
                    for i in range(3):
                        for j in range(3):
                            bx = x + i * block_size + 1
                            by = y + j * block_size + 1
                            veta = ((i * 7 + j * 5 + fila * 3 + col * 2) % 15) - 7
                            color_piedra = (
                                min(255, max(0, 210 + veta)),
                                min(255, max(0, 195 + veta)),
                                min(255, max(0, 170 + veta)),
                            )
                            pygame.draw.rect(
                                pantalla,
                                color_piedra,
                                (bx, by, block_size - 2, block_size - 2),
                            )
                            pygame.draw.line(
                                pantalla,
                                (180, 165, 145),
                                (bx, by),
                                (bx + block_size - 2, by),
                                1,
                            )
                            pygame.draw.line(
                                pantalla,
                                (180, 165, 145),
                                (bx, by),
                                (bx, by + block_size - 2),
                                1,
                            )

                    # Borde de bronce
                    pygame.draw.rect(
                        pantalla, (184, 115, 51), (x, y, tam_celda, tam_celda), 2
                    )

                    # Sombras
                    pygame.draw.line(
                        pantalla,
                        (150, 140, 120),
                        (x + 2, y + 2),
                        (x + tam_celda - 2, y + 2),
                        1,
                    )
                    pygame.draw.line(
                        pantalla,
                        (150, 140, 120),
                        (x + 2, y + 2),
                        (x + 2, y + tam_celda - 2),
                        1,
                    )
                else:
                    # === MOSAICO GRECO-ROMANO ===
                    base_terracota = (156, 102, 68)
                    pygame.draw.rect(
                        pantalla, base_terracota, (x, y, tam_celda, tam_celda)
                    )

                    # Baldosas de mosaico
                    tile_size = tam_celda // 4
                    for tx in range(4):
                        for ty in range(4):
                            tile_x = x + tx * tile_size + 1
                            tile_y = y + ty * tile_size + 1

                            patron = (tx + ty + fila + col) % 3
                            if patron == 0:
                                tile_color = (198, 156, 109)
                            elif patron == 1:
                                tile_color = (176, 141, 105)
                            else:
                                tile_color = (166, 123, 91)

                            pygame.draw.rect(
                                pantalla,
                                tile_color,
                                (tile_x, tile_y, tile_size - 2, tile_size - 2),
                            )

                    # Símbolo griego ocasional
                    if (fila + col) % 7 == 0:
                        center_x = x + tam_celda // 2
                        center_y = y + tam_celda // 2
                        pygame.draw.circle(
                            pantalla, (184, 115, 51), (center_x, center_y), 2
                        )

                    # Borde
                    pygame.draw.rect(
                        pantalla, (140, 90, 60), (x, y, tam_celda, tam_celda), 1
                    )

        # === DIBUJAR HILOS DE ARIADNA ===
        for pos in posiciones_hilo:
            col, fila = pos
            cx = col * tam_celda + tam_celda // 2 + offset_x
            cy = fila * tam_celda + tam_celda // 2 + offset_y

            # Pulsación
            pulso_brillo = abs(math.sin(frame_count * 0.08)) * 0.3 + 0.7
            pulso_tamano = abs(math.sin(frame_count * 0.06)) * 2
            radio_ovillo = 14 + pulso_tamano

            # Aura dorada
            for r in range(5, 0, -1):
                intensidad = int(255 * pulso_brillo * (r / 5.0))
                color_aura = (intensidad, int(intensidad * 0.84), 0)
                pygame.draw.circle(
                    pantalla, color_aura, (cx, cy), int(radio_ovillo + r * 3), 1
                )

            # Ovillo base
            pygame.draw.circle(pantalla, (218, 165, 32), (cx, cy), int(radio_ovillo))

            # Líneas de hilo
            num_lineas = 8
            for i in range(num_lineas):
                angulo = (frame_count * 0.03 + i * (2 * math.pi / num_lineas)) % (
                    2 * math.pi
                )
                inicio_x = cx + (radio_ovillo - 4) * math.cos(angulo)
                inicio_y = cy + (radio_ovillo - 4) * math.sin(angulo)
                fin_x = cx + (radio_ovillo - 9) * math.cos(angulo + 0.5)
                fin_y = cy + (radio_ovillo - 9) * math.sin(angulo + 0.5)
                pygame.draw.line(
                    pantalla,
                    (184, 134, 11),
                    (int(inicio_x), int(inicio_y)),
                    (int(fin_x), int(fin_y)),
                    2,
                )

            # Borde brillante
            color_brillo = (
                int(255 * pulso_brillo),
                int(215 * pulso_brillo),
                int(100 * pulso_brillo),
            )
            pygame.draw.circle(pantalla, color_brillo, (cx, cy), int(radio_ovillo), 2)

            # Destello
            pygame.draw.circle(pantalla, (255, 235, 150), (cx - 2, cy - 2), 3)
            pygame.draw.circle(pantalla, (255, 255, 200), (cx - 2, cy - 2), 1)

        # === LEYENDA ===
        leyenda_y = alto - 80
        leyenda_textos = [
            "🏺 Muros: Mármol griego antiguo",
            "🎨 Suelo: Mosaico terracota",
            "🧵 Hilo de Ariadna: Guía dorada",
        ]

        for idx, texto in enumerate(leyenda_textos):
            surf = fuente_info.render(texto, True, (101, 67, 33))
            pantalla.blit(surf, (20, leyenda_y + idx * 25))

        # Info técnica
        fps_text = fuente_info.render(
            f"FPS: {int(reloj.get_fps())}", True, (139, 69, 19)
        )
        pantalla.blit(fps_text, (ancho - 120, alto - 30))

        pygame.display.flip()
        reloj.tick(60)
        frame_count += 1

    pygame.quit()
    print("\n✅ Test completado. La estética mitológica griega está implementada.")
    print("   El laberinto refleja el mito de Teseo y el Minotauro.\n")


if __name__ == "__main__":
    main()
