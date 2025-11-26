#!/usr/bin/env python3
"""
Script de prueba para verificar el movimiento suave con interpolación.

Verifica que:
- El jugador se mueva suavemente entre celdas
- La interpolación funcione correctamente
- No haya movimiento "trabado"
"""

import os
import sys

# Añadir src al path para poder importar
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import pygame

from config.config import ConfigJuego
from jugabilidad.gestores.gestor_movimiento import GestorMovimiento
from mundo.laberinto import Laberinto
from personajes.jugador import Jugador


def main():
    pygame.init()

    # Configuración
    ancho = 800
    alto = 600
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Test: Movimiento Suave")
    reloj = pygame.time.Clock()

    # Crear laberinto simple para pruebas
    mapa_prueba = [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ]

    tam_celda = 64
    offset_x = 100
    offset_y = 100

    # Crear jugador
    pos_inicial_x = offset_x + tam_celda
    pos_inicial_y = offset_y + tam_celda
    jugador = Jugador(pos_inicial_x, pos_inicial_y, tam_celda)

    # Crear muros
    muros = []
    for fila_idx, fila in enumerate(mapa_prueba):
        for col_idx, celda in enumerate(fila):
            if celda == 1:
                x = offset_x + col_idx * tam_celda
                y = offset_y + fila_idx * tam_celda
                muros.append(pygame.Rect(x, y, tam_celda, tam_celda))

    # Crear gestor de movimiento
    gestor_mov = GestorMovimiento(
        jugador=jugador,
        muros=muros,
        tam_celda=tam_celda,
        offset_x=offset_x,
        offset_y=offset_y,
        mapa=mapa_prueba,
        frames_cooldown=8,
        movimiento_por_celdas=True,
    )

    # Fuente para info
    fuente = pygame.font.Font(None, 24)

    ejecutando = True
    frame_count = 0

    print("\n" + "=" * 60)
    print("TEST: MOVIMIENTO SUAVE CON INTERPOLACIÓN")
    print("=" * 60)
    print("Usa WASD o flechas para mover al jugador")
    print("Observa que el movimiento sea suave entre celdas")
    print("Presiona ESC para salir")
    print("=" * 60 + "\n")

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False

        # Procesar movimiento
        gestor_mov.procesar_entrada_teclado()

        # Renderizar
        pantalla.fill((10, 10, 20))  # Fondo oscuro

        # Dibujar grid de fondo
        for fila_idx in range(len(mapa_prueba)):
            for col_idx in range(len(mapa_prueba[0])):
                x = offset_x + col_idx * tam_celda
                y = offset_y + fila_idx * tam_celda

                if mapa_prueba[fila_idx][col_idx] == 1:
                    # Muro con estilo neon
                    pygame.draw.rect(
                        pantalla, (40, 40, 60), (x, y, tam_celda, tam_celda)
                    )
                    pygame.draw.rect(
                        pantalla, (0, 200, 255), (x, y, tam_celda, tam_celda), 2
                    )
                else:
                    # Suelo con punto central
                    centro_x = x + tam_celda // 2
                    centro_y = y + tam_celda // 2
                    pygame.draw.circle(pantalla, (50, 50, 70), (centro_x, centro_y), 3)

        # Dibujar jugador (esfera cyan pulsante)
        jugador.dibujar_jugador_principal(pantalla, frame_count)

        # Info en pantalla
        info_textos = [
            f"FPS: {int(reloj.get_fps())}",
            f"Posición: ({jugador.jugador_principal.x}, {jugador.jugador_principal.y})",
            f"Puntos: {jugador.puntos}",
            f"Interpolando: {gestor_mov.interpolando}",
            f"Cooldown: {gestor_mov.cooldown_actual}",
        ]

        if gestor_mov.interpolando:
            progreso = (
                gestor_mov.frames_interpolacion
                / gestor_mov.frames_totales_interpolacion
            )
            info_textos.append(f"Progreso interp: {progreso*100:.1f}%")

        for idx, texto in enumerate(info_textos):
            superficie_texto = fuente.render(texto, True, (0, 255, 200))
            pantalla.blit(superficie_texto, (10, 10 + idx * 25))

        # Instrucciones
        instrucciones = fuente.render(
            "Usa WASD o flechas - ESC para salir", True, (150, 150, 150)
        )
        pantalla.blit(instrucciones, (ancho - 350, alto - 30))

        pygame.display.flip()
        reloj.tick(60)
        frame_count += 1

    pygame.quit()
    print("\nTest completado. El movimiento debería verse suave y fluido.")


if __name__ == "__main__":
    main()
