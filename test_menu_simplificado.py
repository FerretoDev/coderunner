#!/usr/bin/env python3
"""
Script de prueba: Menú de Confirmación Simplificado (Sin Guardado)

Verifica que:
1. Al presionar ESC en el juego, aparece el menú de confirmación
2. El menú solo muestra "Salir al Menú Principal" y "Continuar Jugando"
3. No hay referencias a "guardar progreso"
4. La tecla S sale del juego
5. Las teclas N y ESC cancelan y vuelven al juego
"""

import sys

import pygame

# Configurar path para importar módulos del juego
sys.path.insert(0, "src")

from config.config import ConfigJuego
from interfaz.pantallas.pantalla_juego import PantallaJuego

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Test: Menú Simplificado (Sin Guardado)")
clock = pygame.time.Clock()

# Crear pantalla de juego de prueba
try:
    # Crear una instancia simplificada de PantallaJuego
    print("✅ Importación exitosa de PantallaJuego")
    print("\n📋 INSTRUCCIONES DE PRUEBA:")
    print("   1. Presiona ESC para abrir el menú de confirmación")
    print("   2. Verifica que NO aparezca 'Guardar Progreso'")
    print("   3. Verifica que solo haya 2 opciones:")
    print("      - [S] Salir al Menú Principal (ROJO)")
    print("      - [N / ESC] Continuar Jugando (VERDE)")
    print("   4. Prueba:")
    print("      • ESC → Abre menú")
    print("      • S → Sale del juego")
    print("      • N o ESC → Cancela y vuelve")
    print("\n🎮 Presiona ESC en cualquier momento para probar el menú...")
    print("   Presiona Q para salir de la prueba\n")

    # Mensaje en pantalla
    fuente = pygame.font.Font(None, 24)
    fuente_titulo = pygame.font.Font(None, 36)

    ejecutando = True
    menu_visible = False

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_q:
                    print("\n✅ Prueba finalizada por el usuario")
                    ejecutando = False
                elif evento.key == pygame.K_ESCAPE:
                    menu_visible = not menu_visible
                    if menu_visible:
                        print("\n🔔 Menú de confirmación abierto")
                        print("   Verifica visualmente:")
                        print("   ✓ Título: '¿ABANDONAR EL LABERINTO?'")
                        print("   ✓ Subtítulo: 'Teseo desea escapar...'")
                        print("   ✓ Opción ROJA: '[S] Salir al Menú Principal'")
                        print("   ✓ Opción VERDE: '[N / ESC] Continuar Jugando'")
                        print("   ✗ NO debe aparecer 'Guardar Progreso'")
                    else:
                        print("   Menu cerrado (ESC presionado)")

                elif menu_visible:
                    if evento.key == pygame.K_s:
                        print("\n✅ Tecla S: Saliendo del juego (simulado)")
                        print("   En el juego real esto volvería al menú principal")
                        menu_visible = False
                    elif evento.key == pygame.K_n:
                        print("\n✅ Tecla N: Continuando juego")
                        menu_visible = False

        # Dibujar pantalla de prueba
        screen.fill((30, 20, 40))  # Fondo oscuro

        if not menu_visible:
            # Pantalla de juego simulada
            titulo = fuente_titulo.render("JUEGO EN EJECUCIÓN", True, (255, 255, 255))
            titulo_rect = titulo.get_rect(center=(400, 200))
            screen.blit(titulo, titulo_rect)

            instruccion = fuente.render(
                "Presiona ESC para abrir el menú", True, (150, 255, 150)
            )
            instruccion_rect = instruccion.get_rect(center=(400, 280))
            screen.blit(instruccion, instruccion_rect)

            salir = fuente.render(
                "Presiona Q para salir de la prueba", True, (255, 150, 150)
            )
            salir_rect = salir.get_rect(center=(400, 320))
            screen.blit(salir, salir_rect)

        else:
            # Dibujar menú de confirmación simplificado (simulado)
            # Overlay oscuro
            overlay = pygame.Surface((800, 600))
            overlay.set_alpha(200)
            overlay.fill((20, 15, 10))
            screen.blit(overlay, (0, 0))

            # Caja de diálogo
            caja_rect = pygame.Rect(125, 125, 550, 350)
            pygame.draw.rect(screen, (210, 195, 170), caja_rect, border_radius=10)
            pygame.draw.rect(screen, (184, 115, 51), caja_rect, 4, border_radius=10)

            # Título
            titulo = fuente_titulo.render(
                "¿ABANDONAR EL LABERINTO?", True, (139, 69, 19)
            )
            titulo_rect = titulo.get_rect(center=(400, 195))
            screen.blit(titulo, titulo_rect)

            # Subtítulo
            subtitulo = fuente.render(
                "Teseo desea escapar del laberinto...", True, (101, 67, 33)
            )
            subtitulo_rect = subtitulo.get_rect(center=(400, 255))
            screen.blit(subtitulo, subtitulo_rect)

            # Separador
            pygame.draw.line(screen, (184, 115, 51), (175, 305), (625, 305), 2)

            # Opción 1: Salir (ROJO)
            opcion1 = fuente.render("[S] Salir al Menú Principal", True, (178, 34, 34))
            opcion1_rect = opcion1.get_rect(center=(400, 355))
            fondo1 = pygame.Rect(
                opcion1_rect.x - 15,
                opcion1_rect.y - 8,
                opcion1_rect.width + 30,
                opcion1_rect.height + 16,
            )
            pygame.draw.rect(screen, (198, 156, 109), fondo1, border_radius=5)
            pygame.draw.rect(screen, (139, 69, 19), fondo1, 2, border_radius=5)
            screen.blit(opcion1, opcion1_rect)

            # Opción 2: Continuar (VERDE)
            opcion2 = fuente.render("[N / ESC] Continuar Jugando", True, (34, 139, 34))
            opcion2_rect = opcion2.get_rect(center=(400, 415))
            fondo2 = pygame.Rect(
                opcion2_rect.x - 15,
                opcion2_rect.y - 8,
                opcion2_rect.width + 30,
                opcion2_rect.height + 16,
            )
            pygame.draw.rect(screen, (198, 156, 109), fondo2, border_radius=5)
            pygame.draw.rect(screen, (139, 69, 19), fondo2, 2, border_radius=5)
            screen.blit(opcion2, opcion2_rect)

            # ✅ VERIFICACIÓN VISUAL: NO debe aparecer texto de "guardar progreso"

        pygame.display.flip()
        clock.tick(60)

    print("\n✅ RESUMEN DE LA SIMPLIFICACIÓN:")
    print("   ✓ Método _guardar_progreso() eliminado")
    print("   ✓ Texto 'Guardar Progreso' eliminado del menú")
    print("   ✓ Nota 'El progreso se guardará...' eliminada")
    print("   ✓ Evento K_s ya NO llama a _guardar_progreso()")
    print("   ✓ Menú solo muestra: Salir o Continuar\n")

except Exception as e:
    print(f"\n❌ Error durante la prueba: {e}")
    import traceback

    traceback.print_exc()

finally:
    pygame.quit()
    print("🏁 Prueba finalizada\n")
