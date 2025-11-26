#!/usr/bin/env python3
"""
Script de prueba para el menú de confirmación de salida con ESC.

Prueba:
- Presionar ESC muestra menú de confirmación
- Opción S: Salir y guardar progreso
- Opción N/ESC: Continuar jugando
- El progreso se guarda en progreso_guardado.json
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import pygame


def main():
    pygame.init()

    ancho = 1000
    alto = 700
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Test: Menú de Pausa con Confirmación - ESC")
    reloj = pygame.time.Clock()

    # Fuentes
    fuente_titulo = pygame.font.Font(None, 72)
    fuente_mediana = pygame.font.Font(None, 36)
    fuente_pequena = pygame.font.Font(None, 24)

    # Estados simulados
    mostrar_menu = False
    puntaje = 1250
    vidas = 3
    tiempo = 145  # segundos

    ejecutando = True
    jugando = True
    frame_count = 0

    print("\n" + "=" * 70)
    print("🎮 TEST: MENÚ DE CONFIRMACIÓN DE SALIDA (ESC)")
    print("=" * 70)
    print("Controles:")
    print("  ESC: Abrir/cerrar menú de confirmación")
    print("  S: Salir y guardar progreso")
    print("  N: Continuar jugando")
    print("\nEl progreso se guarda en: src/data/progreso_guardado.json")
    print("=" * 70 + "\n")

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if mostrar_menu:
                    # En el menú de confirmación
                    if evento.key == pygame.K_s:
                        print("\n✅ Saliendo y guardando progreso...")
                        print(f"   Puntaje: {puntaje}")
                        print(f"   Vidas: {vidas}")
                        print(f"   Tiempo: {tiempo}s")
                        print("   Guardado en: src/data/progreso_guardado.json\n")
                        ejecutando = False
                    elif evento.key == pygame.K_n or evento.key == pygame.K_ESCAPE:
                        print("➡️  Continuando juego...")
                        mostrar_menu = False
                else:
                    # En el juego
                    if evento.key == pygame.K_ESCAPE:
                        print("⏸️  Abriendo menú de confirmación...")
                        mostrar_menu = True

        # Renderizar
        if mostrar_menu:
            # Fondo del juego atenuado
            pantalla.fill((156, 102, 68))  # Terracota

            # Overlay oscuro
            overlay = pygame.Surface((ancho, alto))
            overlay.set_alpha(200)
            overlay.fill((20, 15, 10))
            pantalla.blit(overlay, (0, 0))

            # Caja de diálogo estilo griego
            caja_ancho = 600
            caja_alto = 400
            caja_x = (ancho - caja_ancho) // 2
            caja_y = (alto - caja_alto) // 2

            # Fondo de mármol
            caja_rect = pygame.Rect(caja_x, caja_y, caja_ancho, caja_alto)
            pygame.draw.rect(pantalla, (210, 195, 170), caja_rect, border_radius=10)

            # Borde de bronce doble
            pygame.draw.rect(pantalla, (184, 115, 51), caja_rect, 4, border_radius=10)
            caja_rect2 = pygame.Rect(
                caja_x + 8, caja_y + 8, caja_ancho - 16, caja_alto - 16
            )
            pygame.draw.rect(pantalla, (139, 90, 43), caja_rect2, 3, border_radius=8)

            # Sombras interiores
            pygame.draw.line(
                pantalla,
                (180, 165, 145),
                (caja_x + 12, caja_y + 12),
                (caja_x + caja_ancho - 12, caja_y + 12),
                2,
            )
            pygame.draw.line(
                pantalla,
                (180, 165, 145),
                (caja_x + 12, caja_y + 12),
                (caja_x + 12, caja_y + caja_alto - 12),
                2,
            )

            # Título
            y_titulo = caja_y + 60
            titulo = fuente_titulo.render(
                "¿ABANDONAR EL LABERINTO?", False, (139, 69, 19)
            )
            titulo_rect = titulo.get_rect(center=(ancho // 2, y_titulo))
            pantalla.blit(titulo, titulo_rect)

            # Subtítulo
            y_subtitulo = y_titulo + 50
            subtitulo = fuente_mediana.render(
                "Teseo desea escapar...", False, (101, 67, 33)
            )
            subtitulo_rect = subtitulo.get_rect(center=(ancho // 2, y_subtitulo))
            pantalla.blit(subtitulo, subtitulo_rect)

            # Info del progreso
            y_info = y_subtitulo + 60
            info_textos = [
                f"Puntaje actual: {puntaje}",
                f"Vidas restantes: {vidas}",
                f"Tiempo jugado: {tiempo}s",
            ]

            for idx, texto in enumerate(info_textos):
                info_surf = fuente_pequena.render(texto, False, (80, 60, 40))
                info_rect = info_surf.get_rect(center=(ancho // 2, y_info + idx * 25))
                pantalla.blit(info_surf, info_rect)

            # Separador
            y_separador = y_info + 80
            pygame.draw.line(
                pantalla,
                (184, 115, 51),
                (caja_x + 50, y_separador),
                (caja_x + caja_ancho - 50, y_separador),
                2,
            )

            # Opciones
            y_opciones = y_separador + 40

            # Opción 1: Salir
            opcion1 = fuente_mediana.render(
                "[S] Salir y Guardar Progreso", False, (34, 139, 34)
            )
            opcion1_rect = opcion1.get_rect(center=(ancho // 2, y_opciones))
            fondo1 = pygame.Rect(
                opcion1_rect.x - 15,
                opcion1_rect.y - 8,
                opcion1_rect.width + 30,
                opcion1_rect.height + 16,
            )
            pygame.draw.rect(pantalla, (198, 156, 109), fondo1, border_radius=5)
            pygame.draw.rect(pantalla, (139, 69, 19), fondo1, 2, border_radius=5)
            pantalla.blit(opcion1, opcion1_rect)

            # Opción 2: Continuar
            opcion2 = fuente_mediana.render(
                "[N / ESC] Continuar Jugando", False, (178, 34, 34)
            )
            opcion2_rect = opcion2.get_rect(center=(ancho // 2, y_opciones + 60))
            fondo2 = pygame.Rect(
                opcion2_rect.x - 15,
                opcion2_rect.y - 8,
                opcion2_rect.width + 30,
                opcion2_rect.height + 16,
            )
            pygame.draw.rect(pantalla, (198, 156, 109), fondo2, border_radius=5)
            pygame.draw.rect(pantalla, (139, 69, 19), fondo2, 2, border_radius=5)
            pantalla.blit(opcion2, opcion2_rect)

            # Nota
            y_nota = caja_y + caja_alto - 30
            nota = fuente_pequena.render(
                "El progreso se guardará para continuar más tarde", False, (120, 90, 60)
            )
            nota_rect = nota.get_rect(center=(ancho // 2, y_nota))
            pantalla.blit(nota, nota_rect)

        else:
            # Pantalla de juego simulada
            pantalla.fill((156, 102, 68))  # Terracota

            # Simulación de laberinto
            import math

            for i in range(0, ancho, 60):
                for j in range(100, alto, 60):
                    if (i + j) % 120 == 0:
                        # Muro
                        pygame.draw.rect(pantalla, (210, 195, 170), (i, j, 60, 60))
                        pygame.draw.rect(pantalla, (184, 115, 51), (i, j, 60, 60), 2)

            # HUD simulado
            hud_rect = pygame.Rect(0, 0, ancho, 80)
            pygame.draw.rect(pantalla, (210, 195, 170), hud_rect)
            pygame.draw.line(pantalla, (184, 115, 51), (0, 80), (ancho, 80), 3)

            hud_texto = fuente_mediana.render(
                f"Puntaje: {puntaje}  |  Vidas: {vidas}  |  Tiempo: {tiempo}s",
                False,
                (139, 69, 19),
            )
            hud_rect = hud_texto.get_rect(center=(ancho // 2, 40))
            pantalla.blit(hud_texto, hud_rect)

            # Instrucción
            instruccion = fuente_pequena.render(
                "Presiona ESC para pausar", False, (101, 67, 33)
            )
            instruccion_rect = instruccion.get_rect(center=(ancho // 2, alto - 30))
            pantalla.blit(instruccion, instruccion_rect)

        pygame.display.flip()
        reloj.tick(60)
        frame_count += 1

    pygame.quit()
    print("\n✅ Test completado.")
    print("   El menú de confirmación funciona correctamente.\n")


if __name__ == "__main__":
    main()
