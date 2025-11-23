#!/usr/bin/env python3
"""
Script de prueba para verificar el sistema de música del juego.
"""

import pygame
import time
import os
import sys

# Agregar la carpeta src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from models.sistema_sonido import SistemaSonido


def test_sistema_musica():
    """Prueba el sistema de música del juego"""
    print("=" * 60)
    print("PRUEBA DEL SISTEMA DE MÚSICA")
    print("=" * 60)

    # Inicializar pygame
    pygame.init()

    # Crear instancia del sistema de sonido
    print("\n1. Creando sistema de sonido...")
    sistema = SistemaSonido()

    if not sistema.mixer_disponible:
        print("❌ El mixer de pygame no está disponible")
        return

    print("✓ Sistema de sonido inicializado correctamente")

    # Verificar que el archivo de música existe
    ruta_musica = os.path.join(
        os.path.dirname(__file__), "src", "data", "MusicaPerrona.mp3"
    )

    print(f"\n2. Verificando archivo de música: {ruta_musica}")
    if os.path.exists(ruta_musica):
        print(f"✓ Archivo encontrado")
    else:
        print(f"❌ Archivo NO encontrado")
        return

    # Reproducir música
    print("\n3. Reproduciendo música de fondo...")
    sistema.reproducir_musica_fondo()
    print("✓ Música iniciada (debería estar sonando)")
    print("  Esperando 3 segundos...")
    time.sleep(3)

    # Probar pausa
    print("\n4. Pausando música...")
    sistema.pausar_musica()
    print("✓ Música pausada")
    print("  Esperando 2 segundos...")
    time.sleep(2)

    # Reanudar
    print("\n5. Reanudando música...")
    sistema.reanudar_musica()
    print("✓ Música reanudada")
    print("  Esperando 3 segundos...")
    time.sleep(3)

    # Ajustar volumen
    print("\n6. Ajustando volumen a 0.2...")
    sistema.ajustar_volumen_musica(0.2)
    print("✓ Volumen ajustado (más bajo)")
    print("  Esperando 2 segundos...")
    time.sleep(2)

    # Subir volumen
    print("\n7. Ajustando volumen a 0.8...")
    sistema.ajustar_volumen_musica(0.8)
    print("✓ Volumen ajustado (más alto)")
    print("  Esperando 2 segundos...")
    time.sleep(2)

    # Alternar música
    print("\n8. Alternando música (desactivar)...")
    sistema.alternar_musica()
    print(f"✓ Música {'activa' if sistema.musica_activa else 'inactiva'}")
    print("  Esperando 2 segundos...")
    time.sleep(2)

    # Alternar música de nuevo
    print("\n9. Alternando música (activar)...")
    sistema.alternar_musica()
    print(f"✓ Música {'activa' if sistema.musica_activa else 'inactiva'}")
    print("  Esperando 2 segundos...")
    time.sleep(2)

    # Detener música
    print("\n10. Deteniendo música...")
    sistema.detener_musica()
    print("✓ Música detenida")

    # Probar singleton
    print("\n11. Probando patrón singleton...")
    sistema2 = SistemaSonido()
    if sistema is sistema2:
        print("✓ Singleton funciona correctamente (misma instancia)")
    else:
        print("❌ Singleton NO funciona (instancias diferentes)")

    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
    print("=" * 60)

    pygame.quit()


if __name__ == "__main__":
    test_sistema_musica()
