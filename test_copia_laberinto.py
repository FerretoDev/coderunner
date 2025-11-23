#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de copia de laberintos externos.
"""

import os
import sys
import tempfile
import json
import shutil

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from models.administrador import Administrador


def crear_laberinto_temporal():
    """Crea un archivo de laberinto temporal fuera de src/"""
    laberinto_test = {
        "nombre": "Laberinto Externo de Prueba",
        "mapa": [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1],
        ],
        "inicio_jugador": {"col": 1, "fila": 1},
        "inicio_computadora": {"col": 3, "fila": 3},
        "obsequios": [],
    }

    # Crear archivo temporal
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as f:
        json.dump(laberinto_test, f, indent=2)
        return f.name


def main():
    print("=" * 60)
    print("PRUEBA: Carga de Laberinto Externo")
    print("=" * 60)

    admin = Administrador("test")

    # Crear laberinto temporal
    print("\n1. Creando laberinto temporal fuera de src/...")
    ruta_temporal = crear_laberinto_temporal()
    print(f"   ✓ Creado en: {ruta_temporal}")

    # Intentar cargar el laberinto
    print("\n2. Cargando laberinto externo...")
    laberinto, mensaje = admin.cargar_laberinto(ruta_temporal, copiar_externo=True)

    if laberinto:
        print(f"   ✓ {mensaje}")

        # Verificar que se copió
        print("\n3. Verificando copia en src/data/laberintos/...")
        archivos = os.listdir("src/data/laberintos")
        archivos_recientes = [
            f for f in archivos if "laberinto_externo_de_prueba" in f.lower()
        ]

        if archivos_recientes:
            print(f"   ✓ Archivo copiado: {archivos_recientes[-1]}")
        else:
            print("   ⚠ No se encontró el archivo copiado")

        # Verificar configuración
        print("\n4. Verificando configuración de laberinto activo...")
        ruta_activa = Administrador.obtener_laberinto_activo()
        if ruta_activa:
            print(f"   ✓ Laberinto activo: {ruta_activa}")
            print(f"   ✓ Archivo existe: {os.path.exists(ruta_activa)}")
        else:
            print("   ⚠ No se guardó el laberinto activo")

    else:
        print(f"   ✗ Error: {mensaje}")

    # Limpiar archivo temporal
    print("\n5. Limpiando archivo temporal...")
    try:
        os.unlink(ruta_temporal)
        print("   ✓ Archivo temporal eliminado")
    except:
        pass

    print("\n" + "=" * 60)
    print("PRUEBA COMPLETADA")
    print("=" * 60)


if __name__ == "__main__":
    main()
